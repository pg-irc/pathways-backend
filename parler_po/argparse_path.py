from django.utils.translation import ugettext_lazy as _
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

def _path_type_fn(path, file_type=None, mode_flags=set()):
    full_path = os.path.abspath(path)

    if os.path.exists(full_path):
        if file_type == 'file' and not os.path.isfile(full_path):
            raise argparse.ArgumentTypeError(
                _("The path {} must be a file").format(path)
            )
        elif file_type == 'dir' and not os.path.isdir(full_path):
            raise argparse.ArgumentTypeError(
                _("The path {} must be a directory").format(path)
            )
        elif os.R_OK in mode_flags and not os.access(full_path, os.R_OK):
            raise argparse.ArgumentTypeError(
                _("The path {} must be readable").format(path)
            )
        elif os.W_OK in mode_flags and not os.access(full_path, os.W_OK):
            raise argparse.ArgumentTypeError(
                _("The path {} must be writable").format(path)
            )
        elif os.X_OK in mode_flags and not os.access(full_path, os.X_OK):
            raise argparse.ArgumentTypeError(
                _("The path {} must be executable").format(path)
            )
        else:
            return full_path
    else:
        try:
            os.makedirs(full_path)
        except OSError as e:
            raise argparse.ArgumentTypeError(
                _("The path {} does not exist").format(path)
            )
        else:
            return full_path
