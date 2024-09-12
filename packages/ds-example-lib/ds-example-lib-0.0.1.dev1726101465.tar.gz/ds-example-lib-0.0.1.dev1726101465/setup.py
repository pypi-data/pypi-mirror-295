import time
from setuptools import setup
ts = int(time.time())
setup(
    name='ds-example-lib',
    description='Placeholder for internal package',
    version=f"0.0.1dev{ts}",
)