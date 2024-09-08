from setuptools import setup, find_packages
from setuptools.command.install import install
from hello_world_installer_test.main import print_hello_world

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        print_hello_world()

setup(
    name="hello_world_installer_test",
    version="0.1.0",
    packages=find_packages(),
    author="Your Name",
    author_email="your.email@example.com",
    description="A package that prints 'Hello World' during installation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hello_world_installer_test",
    cmdclass={
        'install': CustomInstallCommand,
    },
)