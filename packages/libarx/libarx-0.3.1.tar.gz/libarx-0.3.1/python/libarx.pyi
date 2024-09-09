class Arx:
    """
    An Arx archive.
    From an arx archive, you can access the entries in it.

    # Accessing entrie is arx archive:

    You can either:

    ## Directly use `arx.get_entry("foo/bar/file.ext")` if you know the path of the entry.

    > arx = libarx.Arx("archive.arx")
    > entry = arx.get_entry("foo/bar/file.ext")

    ## Iterate on the archive

    > arx = libarx.Arx("archive.arx")
    > for entry in arx:
    >     ...

    Arx archives contain a tree structure, so iterating on the archive will loop only on top level
    entries. You will have to iterate on Directory entries to walk the tree structure.
    """

    def __init__(self, path: str) -> "Arx":
        """
        Open an arx archive.

        :param name: the path of the archive to open
        :return: The opened arx archive
        """

    def get_entry(self, path: str) -> Entry:
        """
        Get the entry for the given path.

        :param path: the path of the entry
        :return: the entry
        """

    def get_content(self, content_address: ContentAddress) -> bytes:
        """
        Get the content for the given content address.

        Content address can be obtained from a file Entry.

        :param content_address: The content address
        :return: The content.
        """

    def extract(self, extract_path: str):
        """
        Extract the whole archive into `extract_path`.

        :param extract_path: To where extract the archive.
        """
