from setuptools import setup

from versions import get_latest_version

# reading long description from file
with open('description.md') as file:
    long_description = file.read()

# specify requirements of your package here
REQUIREMENTS = [
    'websocket-client==1.8.0', 
    'ifaddr==0.2.0', 
    'msgpack==1.0.8'
]

# some more details
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'Topic :: Scientific/Engineering',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.12',
]

latest_version = get_latest_version()

# calling the setup function
setup(name='CK-InoDrive-API',
      version=latest_version['number'],
      description='InoDrive API Library',
      license_files=['LICENSE.txt', 'README.txt'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://cardinalkinetic.com',
      author='Cardinal Kinetic',
      author_email='support@cardinalkinetic.com',
      license='https://www.cardinalkinetic.com/user-manual/api/inodrive-py',
      packages=['CkInoDriveAPI'],
      package_data={"":['*.crt']},
      project_urls={
        'Documentation': 'https://www.cardinalkinetic.com/user-manual/api/inodrive-py'
      },
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='InoWorx InoDrive InoSync MotionControl ServoControl'
      )
