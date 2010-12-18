from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

version = '0.1.0'

setup(
    name='opendir',
    version=version,
    description=('Read directory entries individually.'),
    author='David Hain',
    author_email='dhain@zognot.org',
    url='http://zognot.org/projects/opendir/',
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    ext_modules=[
        Extension('opendir', ['opendir.pyx']),
    ],
    cmdclass=dict(build_ext=build_ext),
)
