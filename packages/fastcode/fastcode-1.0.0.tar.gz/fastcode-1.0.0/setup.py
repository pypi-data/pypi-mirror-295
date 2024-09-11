from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'Programming Language :: Python :: 3.12'
]
 
setup(
  name='fastcode',
  version='1.0.0',
  description='A Python Library for simplifying the use of repetitive code in my python projects.',
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  url='https://github.com/TareqAbeda/Python_Library',  
  author='Tareq Abeda',
  author_email='TareqAbeda@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Protocols', 
  packages=find_packages(),
  install_requires=[] 
)