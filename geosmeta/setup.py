from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='geosmeta',
      version='0.2',
      description='Store geosciences metadata in a database',
      url='https://www.wiki.ed.ac.uk/display/geoinf/GeosMeta+project',
      author='',
      author_email='',
      license='???',
      packages=['geosmeta'],
      install_requires=[
          'requests',
      ],
      scripts=[
          'bin/create_user'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
