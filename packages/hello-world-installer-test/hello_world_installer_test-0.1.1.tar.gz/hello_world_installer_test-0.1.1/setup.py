from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        print("Hello World!")
        install.run(self)

setup(
    name="hello_world_installer_test",
    version="0.1.1",  # Increment the version number
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
    },
    # ... other setup parameters ...
)