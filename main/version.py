# The version is defined in /pathways-backend/main/__init__.py


def get_version_string():
    return __import__('main').__version__


def get_version_info():
    return __import__('main').__version_info__
