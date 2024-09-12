from abc import abstractmethod
from typing import Any, Dict, Optional, Union

from fake import BaseStorage
from pathy import Pathy

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "CloudStorage",
    "PathyFileSystemStorage",
)

DEFAULT_ROOT_PATH = "tmp"
DEFAULT_REL_PATH = "tmp"


class CloudStorage(BaseStorage):
    """File storage class using Pathy for path handling.

    Usage example:

    .. code-block:: python

        from fake import FAKER
        from fakepy.pathy_storage import PathyFileSystemStorage

        storage = PathyStorage()
        docx_file = FAKER.docx_file(storage=storage)

    Initialization with params:

    .. code-block:: python

        from fake import FAKER
        from fakepy.pathy_storage import PathyFileSystemStorage

        storage = PathyFileSystemStorage()
        docx_file = storage.generate_filename(prefix="zzz_", extension="docx")
        storage.write_bytes(docx_file, FAKER.docx())
    """

    bucket_name: str
    bucket: Pathy
    credentials: Dict[str, str]
    schema: Optional[str] = None

    def __init__(
        self: "CloudStorage",
        bucket_name: str,
        root_path: Optional[str] = DEFAULT_ROOT_PATH,
        rel_path: Optional[str] = DEFAULT_REL_PATH,
        credentials: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> None:
        """
        :param bucket_name: Bucket name.
        :param root_path: Path of your files root directory (e.g., Django's
            `settings.MEDIA_ROOT`).
        :param rel_path: Relative path (from root directory).
        :param credentials: Dictionary of credentials.
        :param *args:
        :param **kwargs:
        :raises: NotImplementedError
        """
        if self.schema is None:
            raise Exception("The `schema` property should the set!")
        self.bucket_name = bucket_name
        self.root_path = root_path or ""
        self.rel_path = rel_path or ""
        self.cache_dir = None
        credentials = credentials or {}

        if credentials:
            self.authenticate(**credentials)

        self.bucket = Pathy(f"{self.schema}://{self.bucket_name}")
        # If bucket does not exist, create
        if not self.bucket.exists():
            self.bucket.mkdir(exist_ok=True)

        super().__init__(*args, **kwargs)

    @abstractmethod
    def authenticate(self, *args, **kwargs):
        raise NotImplementedError("Method authenticate is not implemented!")

    def generate_filename(
        self: "CloudStorage",
        extension: str,
        prefix: Optional[str] = None,
        basename: Optional[str] = None,
    ) -> Pathy:
        """Generate filename."""
        if not extension:
            raise Exception("Extension shall be given!")

        if not basename:
            basename = self.generate_basename(prefix)

        return (
            self.bucket
            / self.root_path
            / self.rel_path
            / f"{basename}.{extension}"
        )

    def write_text(
        self: "CloudStorage",
        filename: Pathy,
        data: str,
        encoding: Optional[str] = None,
    ) -> int:
        """Write text."""
        file = self.bucket / self.root_path / self.rel_path / filename
        return file.write_text(data, encoding)

    def write_bytes(
        self: "CloudStorage",
        filename: Pathy,
        data: bytes,
    ) -> int:
        """Write bytes."""
        file = self.bucket / self.root_path / self.rel_path / filename
        return file.write_bytes(data)

    def exists(self: "CloudStorage", filename: Union[Pathy, str]) -> bool:
        """Check if file exists."""
        if isinstance(filename, str):
            filename = self.bucket / self.root_path / filename
        return filename.exists()

    def relpath(self: "CloudStorage", filename: Pathy) -> str:
        """Return relative path."""
        return str(filename.relative_to(self.bucket / self.root_path))

    def abspath(self: "CloudStorage", filename: Pathy) -> str:
        """Return absolute path."""
        return filename.as_uri()

    def unlink(self: "CloudStorage", filename: Union[Pathy, str]) -> None:
        """Delete the file."""
        if isinstance(filename, str):
            filename = self.bucket / self.root_path / filename
        filename.unlink()


class PathyFileSystemStorage(CloudStorage):
    """Pathy FileSystem Storage.

    Usage example:

    .. code-block:: python

        from fakepy.pathy_storage.cloud import PathyFileSystemStorage

        storage = PathyFileSystemStorage(bucket_name="artur-testing-1")
        file = storage.generate_filename(prefix="zzz_", extension="txt")
        storage.write_text(file, "Lorem ipsum")
        storage.write_bytes(file, b"Lorem ipsum")
    """

    schema: str = "file"

    def authenticate(self: "PathyFileSystemStorage", **kwargs) -> None:
        """Authenticate. Does nothing."""
