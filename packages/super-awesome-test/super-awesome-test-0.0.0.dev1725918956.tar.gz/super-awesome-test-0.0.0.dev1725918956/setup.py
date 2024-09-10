import time
from setuptools import setup
ts = int(time.time())
setup(
    name='super-awesome-test',
    description='Placeholder to prevent dependency confusion',
    version=f"0.0.0dev{ts}",
    py_modules=['module']
)