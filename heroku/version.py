# The Python runtime version Heroku will use is defined in /pathways-backend/heroku/__init__.py

def get_python_runtime_version_string():
    return __import__('heroku').__python_runtime_version__
