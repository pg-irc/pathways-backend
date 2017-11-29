from django.utils.translation import ugettext_lazy as _
import argparse
import functools
import os

DIR_MODE_FLAGS = {
    'r': os.R_OK,
    'w': os.W_OK,
    'x': os.X_OK
}

def argparse_path_type(file_type=None, mode=''):
    mode_flags = set(DIR_MODE_FLAGS[k] for k in mode)
    return functools.partial(
        _path_type_fn, file_type=file_type, mode_flags=mode_flags
    )

def _path_type_fn(path, file_type=None, mode_flags=set()):
    full_path = os.path.abspath(path)

    if os.path.exists(full_path):
        if file_type == 'file' and not os.path.isfile(full_path):
            msg = _("The path {} must be a file").format(path)
            raise argparse.ArgumentTypeError(msg)
        elif file_type == 'dir' and not os.path.isdir(full_path):
            msg = _("The path {} must be a directory").format(path)
            raise argparse.ArgumentTypeError(msg)
        elif os.R_OK in mode_flags and not os.access(full_path, os.R_OK):
            msg = _("The directory {} must be readable").format(path)
            raise argparse.ArgumentTypeError(msg)
        elif os.W_OK in mode_flags and not os.access(full_path, os.W_OK):
            msg = _("The directory {} must be writable").format(path)
            raise argparse.ArgumentTypeError(msg)
        elif os.X_OK in mode_flags and not os.access(full_path, os.X_OK):
            msg = _("The directory {} must be executable").format(path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return full_path
    else:
        try:
            os.makedirs(full_path)
        except OSError as e:
            msg = _("The directory {} does not exist").format(path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return full_path
