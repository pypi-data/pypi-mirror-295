import shutil
from setuptools import find_packages, setup
from setuptools.command.install_scripts import install_scripts


class InstallScripts(install_scripts):
    def run(self):
        install_scripts.run(self)

        # Rename some script files
        for script in self.get_outputs():
            if script.endswith(".py") or script.endswith(".sh"):
                dest = script[:-3]
            else:
                continue
            print("moving %s to %s" % (script, dest))
            shutil.move(script, dest)


setup(
    name='mini_max_swing',
    version='0.0.1',
    description='httpgenerator or rpcgenerator distpackage',
    author='xingyun',
    author_email='xingyun1@minimaxi.com',
    include_package_data=True,
    url='https://gitlab.xaminim.com/qa/swing',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['.gitignore', 'bin']),
    python_requires='>=3.9',
    package_data={
        'swing': ['py.typed', '*.pyi', '**/*.py', '**/*.ini', '*/conf.ini'],
    },
    scripts=['swing/swing_bin/generator.py'],
    cmdclass={
        "install_scripts": InstallScripts
    },
    entry_points={
        'console_scripts': [
            'mini_max_swing = swing_bin.generator:swing',
        ],
    },

)