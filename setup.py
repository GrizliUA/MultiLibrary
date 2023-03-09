from setuptools import setup, find_packages

setup(
    name='department-app',
    version='1.0',
    author='Maksym Struk',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)