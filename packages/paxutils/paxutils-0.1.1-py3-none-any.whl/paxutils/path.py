import pathlib
import requests
from typing_extensions import Self

PAX_SERVER_URL = 'https://pax.ulaval.ca'

class Path(pathlib.Path):
    """This class behaves has a PAX replacement for the standard `pathlib.Path`.

    If {course} exists and if the specified path is relative, it adds a path prefix:
    1. `../fichiers/` if this relative folder exists locally;
    2. `/pax/shared/{course}/` else if this absolute path exists locally;
    3. or an absolute writeable `/tmp/pax/{course}/` prefix otherwise.

    Moreover, if the path does not exist, it tries to download it from the PAX server.

    Otherwise, it behaves as a standard pathlib path.
    """
    _flavour = type(pathlib.Path())._flavour

    def __new__(cls, *paths, course: str=None):
        # make sure course is uppercase
        course = course.upper() if course is not None else course

        if course and not pathlib.Path(*paths).is_absolute():
            # check for local sibling 'fichiers' folder
            if pathlib.Path('../fichiers').is_dir():
                # use local relative file path prefix
                self = super(Path, cls).__new__(cls, '../fichiers', *paths)
                self._path_index = 2

            elif pathlib.Path('/pax/shared', course, *paths).exists():
                # use local absolute shared prefix
                self = super(Path, cls).__new__(cls, '/pax/shared', course, *paths)
                self._path_index = 4

            else:
                # use local writeable temp prefix
                self = super(Path, cls).__new__(cls, '/tmp/pax', course, *paths)
                self._path_index = 4

        else:
            # assume normal pathlib behavior
            self = super(Path, cls).__new__(cls, *paths)
            self._path_index = 0

        # memorize course argument
        self._course = course

        return self

    def __truediv__(self, path) -> Self:
        # check existence of index and course attributes, because some pathlib methods
        # (e.g. absolute) create new paths without calling the __new__ operator
        if not hasattr(self, '_path_index'):
            self._path_index = 0
        if not hasattr(self, '_course'):
            self._course = None

        # apply concatenation operator
        return Path(*self.parts[self._path_index:], path, course=self._course)

    def __rtruediv__(self, path) -> Self:
        # check existence of index and course attributes, because some pathlib methods
        # (e.g. absolute) create new paths without calling the __new__ operator
        if not hasattr(self, '_path_index'):
            self._path_index = 0
        if not hasattr(self, '_course'):
            self._course = None

        # apply reverse concatenation operator
        return Path(path, *self.parts[self._path_index:], course=self._course)

    def fetch_from_pax(self) -> bool:
        # check existence of index and course attributes, because some pathlib methods
        # (e.g. absolute) create new paths without calling the __new__ operator
        if not hasattr(self, '_path_index'):
            self._path_index = 0
        if not hasattr(self, '_course'):
            self._course = None

        # fetch base user path (without prefix)
        user_path = pathlib.Path(*self.parts[self._path_index:])

        if self._course and not self.exists() and not user_path.is_absolute():
            # fetch file content from PAX server
            r = requests.get(f'{PAX_SERVER_URL}/static/{self._course}/fichiers/{str(user_path)}')

            if r.status_code == 200:
                # make sure parent exists
                self.parent.mkdir(parents=True, exist_ok=True)

                # write downloaded content to local file
                self.write_bytes(r.content)

                return True

        return False


if __name__ == '__main__':
    print(Path('toto').absolute()/'tata')
    print(Path('toto', course='GLO-1901'))
    print(Path('reseau.py', course='GIF-U015'))
    print(Path('/pax/shared', course='GLO-1901'))
