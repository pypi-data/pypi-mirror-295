import shutil
from setuptools import find_packages, setup
from setuptools.command.install_scripts import install_scripts

VERSION = '1.1.6'

REQUIRES = [
    'allure-pytest==2.13.5',
    'allure-python-commons==2.13.5',
    'cos-python-sdk-v5==1.9.29',
    'pytest==6.2.3',
    'pandas==2.2.2',
    'urllib3==1.26.5',
    'ptsd==0.2.0',
    'requests-toolbelt',
    'pytz==2024.1',
    'thrift==0.20.0',
    'thriftpy2==0.4.20',
    'python-gitlab==4.4.0',
    'kafka-python==2.0.2',
    'backports.tarfile==1.2.0',
    'certifi==2024.8.30',
    'charset-normalizer==3.3.2',
    'Cython==3.0.11',
    'docutils==0.21.2',
    'idna==3.8',
    'importlib_metadata==8.4.0',
    'jaraco.classes==3.4.0',
    'jaraco.context==6.0.1',
    'jaraco.functools==4.0.2',
    'keyring==25.3.0',
    'markdown-it-py==3.0.0',
    'mdurl==0.1.2',
    'more-itertools==10.5.0',
    'nh3==0.2.18',
    'pkginfo==1.10.0',
    'ply==3.11',
    'Pygments==2.18.0',
    'readme_renderer==44.0',
    'requests==2.32.3',
    'requests-toolbelt==1.0.0',
    'rfc3986==2.0.0',
    'rich==13.8.0',
    'six==1.16.0',
    'twine==5.1.1',
    'zipp==3.20.1',
]

DEPENDENCY_LINK = [
    'https://mirrors.aliyun.com/pypi/simple'
]

NAME = 'mini_max_swing'
DESCRIPTION = 'httpgenerator or rpcgenerator distpackage'
URL = 'https://gitlab.xaminim.com/qa/swing'
EMAIL = 'xingyun@minimaxi.com'
AUTHOR = 'zhengguang'


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
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    include_package_data=True,
    url=URL,
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
    data_files=[
        ('', ['swing/rpc_generator/conf/conf.ini']),
    ],
    scripts=['swing/swing_bin/generator.py'],
    cmdclass={
        "install_scripts": InstallScripts
    },
    entry_points={
        'console_scripts': [
            'swing = swing.swing_bin.generator:swing',
        ],
    },
    install_requires=REQUIRES,
    dependency_links=DEPENDENCY_LINK,
)
