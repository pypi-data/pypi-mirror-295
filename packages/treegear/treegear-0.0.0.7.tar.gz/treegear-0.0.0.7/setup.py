from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='treegear',
  version='0.0.0.7',
  author='Gyuli',
  author_email='treegear.dev@gmail.com',
  description='This module is for tests for future project.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  # url='treegear.dev',
  url='http://treegear.dev',
  packages=find_packages(),
  install_requires=['click==8.1.7', 'h11==0.14.0', 'uvicorn==0.30.6'],
  # install_requires=['uvicorn'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python uvicorn',
  project_urls={
    'Documentation': 'http://treegear.dev'
  },
  python_requires='>=3.8'
)