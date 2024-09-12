import time
from setuptools import setup
ts = int(time.time())
setup(
    name='audit-client',
    description='Placeholder for internal package',
    version=f"0.0.1dev{ts}",
)