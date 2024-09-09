from setuptools import setup, find_packages

setup(
name='Cust_seg_gleafink',
package_dir={"": "src"},
packages=find_packages(where="src"), 
author='Phalguni',
author_email='phalgunishenoy2002@gmail.com',
description='A customer segmentation package for preprocessing data',
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
url='',
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
