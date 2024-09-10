from setuptools import setup
import os
import io

'''
Restored setup.py & setup.cfg following instructions at:
Follow instructions at https://stackoverflow.com/questions/42287533/restore-deleted-file-with-history-in-git

git config --get remote.origin.url
git checkout a53fb714b8b48cd0112ae175a179e4a2c6859de1 -b restore_setuptools_build_support
git mv setup.py setup_1.py
git mv setup.cfg setup_1.cfg
git commit -m "Move file (1)"
SAVED=`git rev-parse HEAD`
git reset --hard "HEAD^"
git mv setup.py setup_2.py
git mv setup.cfg setup_2.cfg
git commit -m "Move file (2)"
git merge $SAVED
git commit -a -n
git checkout master
git merge restore_setuptools_build_support
git commit -a -n
git rm setup_1.py setup_1.cfg
git mv setup_2.py setup.py 
git mv setup_2.cfg setup.cfg
git commit -m "recovery finished"
'''


# ----------------------------------------------------
def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("p2api", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content
# ----------------------------------------------------
from p2api import __about__
setup(
    name='p2api',
    #version=read('p2api', 'VERSION'),
    version=__about__.__version__,
    description='Binding for the ESO phase 2 programmatic API',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://www.eso.org/copdemo/apidoc/index.html',
    author='Thomas Bierwirth',
    author_email='thomas.bierwirth@eso.org',

    packages=['p2api', 'p2api/utils',],
    include_package_data=True,
    entry_points={
        'console_scripts' : [
            #'p2api_add_absolute_time_intervals = p2api.utils.add_absolute_time_intervals:main',
            'p2api_generate_finding_charts = p2api.utils.generate_finding_charts:main',
        ],
    },

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='ESO Phase2 Observation Preparation Programmatic API',

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    py_modules=["p2api"],

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'requests',
        'keyring',
        #'astropy', ## needed for add_absolute_time_intervals
        #'astroplan', ## needed for add_absolute_time_intervals
    ],
    license='MIT'
)
