from setuptools import setup,find_packages


ld='A class to pipe the results of the native python "print" to both the stdout and a logfile with color-coding for log-levels.'



#https://docs.python.org/2/distutils/setupscript.html
setup(name='colorlog',
      version='0.9',
      author='Russell Ryan',
      author_email='rryan@stsci.edu',
      keywords='utility logs color',
      description='Color logging',
      long_description=ld,
      maintainer='Russell Ryan',
      license='MIT',
      url='https://github.com/Russell-Ryan/colorlog',
      platforms='posix',
      classifiers=['Development Status :: 3 Alpha',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering'],
      packages=find_packages())
