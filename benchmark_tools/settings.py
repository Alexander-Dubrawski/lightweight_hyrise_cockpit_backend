"""Module for loading environment variables.
Variables that should not be commited can be stored in a .env file:
```
FOO=BAR
EX=AMPLE
```
Set those variables in the .env file, load them here,
and import the variables from this module.
"""
from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BACKEND_HOST: str = getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT: str = getenv("BACKEND_PORT", "8000")
