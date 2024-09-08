from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='CybrocksLibrary',
  version='0.0.1.2',
  description='just some reandom crap',
  long_description = open('README.txt', encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt', encoding='utf-8').read(),
  url='',  
  author='Cybrock9000',
  author_email='ethandepree672@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Library', 
  packages=find_packages(),
  install_requires=[''] 
)