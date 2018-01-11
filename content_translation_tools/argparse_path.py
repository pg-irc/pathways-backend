from django.utils.translation import ugettext_lazy as _
from pathlib import Path
import argparse
import functools
import os

DIR_MODE_FLAGS = {
    'r': os.R_OK,
    'w': os.W_OK,
    'x': os.X_OK
}

class ArgparsePathType(object):
    def __init__(self, file_type=None, mode=''):
        self._file_type = file_type
        self._mode = mode

    def __call__(self, *args):
        mode_flags = set(DIR_MODE_FLAGS[k] for k in self._mode)
        return _path_type_fn(
            *args, file_type=self._file_type, mode_flags=mode_flags
        )

def _path_type_fn(path_str, file_type=None, mode_flags=set()):
    path = Path(path_str)

    if path.exists():
        if file_type == 'file' and not path.is_file():
            raise argparse.ArgumentTypeError(
                _("The path {} must be a file").format(path)
            )
        elif file_type == 'dir' and not path.is_dir():
            raise argparse.ArgumentTypeError(
                _("The path {} must be a directory").format(path)
            )
        elif os.R_OK in mode_flags and not os.access(path, os.R_OK):
            raise argparse.ArgumentTypeError(
                _("The path {} must be readable").format(path)
            )
        elif os.W_OK in mode_flags and not os.access(path, os.W_OK):
            raise argparse.ArgumentTypeError(
                _("The path {} must be writable").format(path)
            )
        elif os.X_OK in mode_flags and not os.access(path, os.X_OK):
            raise argparse.ArgumentTypeError(
                _("The path {} must be executable").format(path)
            )
        else:
            return path
    else:
        try:
            path.mkdir(parents=True)
        except FileNotFoundError as error:
            raise argparse.ArgumentTypeError(
                _("Error creating {}: {}").format(path, error)
            )
        else:
            return path
