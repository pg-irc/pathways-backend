from django.utils.translation import ugettext_lazy as _
import argparse
import functools
import os

DIR_MODE_FLAGS = {
    'r': os.R_OK,
    'w': os.W_OK,
    'x': os.X_OK
}

def argparse_dir_type(mode=''):
    mode_flags = set(DIR_MODE_FLAGS[k] for k in mode)
    return functools.partial(_dir_type_fn, mode_flags=mode_flags)

def _dir_type_fn(dir_name, mode_flags=set()):
    dir_path = os.path.abspath(dir_name)

    if os.path.exists(dir_path):
        if not os.path.isdir(dir_path):
            msg = _("The path {} must be a directory").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        elif os.R_OK in mode_flags and not os.access(dir_path, os.R_OK):
            msg = _("The directory {} must be readable").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        elif os.W_OK in mode_flags and not os.access(dir_path, os.W_OK):
            msg = _("The directory {} must be writable").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        elif os.X_OK in mode_flags and not os.access(dir_path, os.X_OK):
            msg = _("The directory {} must be executable").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return dir_path
    else:
        try:
            os.makedirs(dir_path)
        except OSError as e:
            msg = _("The directory {} does not exist").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return dir_path
