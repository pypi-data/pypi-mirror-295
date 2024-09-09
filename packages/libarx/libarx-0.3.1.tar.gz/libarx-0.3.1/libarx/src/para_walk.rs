use std::sync::Arc;

use super::common::*;
use super::Arx;
use clap::error::ContextKind;
use jbk::reader::Range;

/// A parallel Operator.
/// Like a Operator but `on_file` and `on_link` will be called in a separated thread.
pub trait ParaOperator<Context, Builder>
where
    Context: Clone + Send,
    Builder: FullBuilderTrait,
{
    fn on_start(&self, context: &mut Context) -> jbk::Result<()>;
    fn on_stop(&self, context: &mut Context) -> jbk::Result<()>;
    fn on_directory_enter(
        &self,
        context: &mut Context,
        entry: &<Builder::Entry as EntryDef>::Dir,
    ) -> jbk::Result<(Context, bool)>;
    fn on_directory_exit(
        &self,
        context: &mut Context,
        entry: &<Builder::Entry as EntryDef>::Dir,
    ) -> jbk::Result<()>;
    fn on_file(
        &self,
        context: Context,
        entry: <Builder::Entry as EntryDef>::File,
    ) -> jbk::Result<()>;
    fn on_link(
        &self,
        context: Context,
        entry: <Builder::Entry as EntryDef>::Link,
    ) -> jbk::Result<()>;
}

pub struct ParaWalker<'a, Context> {
    arx: &'a Arx,
    context: Context,
}

impl<'a, Context> ParaWalker<'a, Context>
where
    Context: Clone + Send + 'static,
{
    pub fn new(arx: &'a Arx, context: Context) -> Self {
        Self { arx, context }
    }

    pub fn run<B, O>(&mut self, op: Arc<O>) -> jbk::Result<()>
    where
        B: FullBuilderTrait + Sync + Send + 'static,
        O: Operator<Context, B> + Sync + Send + 'static,
        <B::Entry as EntryDef>::File: Sync + 'static,
    {
        let builder = Arc::new(RealBuilder::<B>::new(&self.arx.properties));

        op.on_start(&mut self.context)?;
        let context = self.context.clone();
        rayon::scope(|s| {
            Self::_run(s, context, &self.arx.root_index, &builder, op.clone()).unwrap();
        });
        op.on_stop(&mut self.context)
    }

    fn _run<'scope, 'builder, R: Range, B, O>(
        scope: &'scope rayon::Scope<'builder>,
        context: Context,
        range: &R,
        builder: &'builder RealBuilder<B>,
        op: Arc<O>,
    ) -> jbk::Result<()>
    where
        B: FullBuilderTrait + Sync + Send + 'static,
        O: Operator<Context, B> + Sync + Send + 'static,
        <B::Entry as EntryDef>::File: Sync + 'static,
        'builder: 'scope,
    {
        let read_entry = ReadEntry::new(range, builder);
        let entries: Vec<_> = read_entry
            .map(|e| e.map(|e| (e, context.clone())))
            .collect::<jbk::Result<Vec<_>>>()?;
        entries.into_iter().try_for_each(move |(entry, context)| {
            let op = Arc::clone(&op);
            match entry {
                Entry::File(e) => scope.spawn(move |scope| op.on_file(context, e).unwrap()),
                Entry::Link(e) => op.on_link(context, e)?,
                Entry::Dir(range, e) => {
                    let (new_context, run_dir) = op.on_directory_enter(context, &e).unwrap();
                    if run_dir {
                        Self::_run(scope, new_context.clone(), &range, builder, op.clone())
                            .unwrap();
                    }
                    op.on_directory_exit(new_context, &e).unwrap();
                }
            };
            Ok::<(), jbk::Error>(())
        })?;
        Ok(())
    }
}
