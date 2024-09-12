import os
from dotenv import dotenv_values

_magma_user_dir: str = os.path.join(os.path.expanduser('~'), '.magma')
os.makedirs(_magma_user_dir, exist_ok=True)

_default_config = {
    'TYPE': 'production',
    'DEBUG': False,
    'DATABASE_DRIVER': 'sqlite',
    'DATABASE_LOCATION': _magma_user_dir
}


def env_local(filename: str = '.env.local'):
    _env_local = os.path.join(os.getcwd(), filename)
    return _env_local


def env(filename: str = '.env'):
    _env = os.path.join(os.getcwd(), filename)
    return _env


config = {
    **_default_config,
    **dotenv_values(env_local()),
    **dotenv_values(env())
}
