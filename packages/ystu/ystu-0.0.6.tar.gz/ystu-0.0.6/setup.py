from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='ystu',
  version='0.0.6',
  author='aleksejeei',
  author_email='aleksejeei@gmail.com',
  description='Auth on site YSTU',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/aleksejeei/ystu_lib',
  packages=find_packages(),
  install_requires=['requests', 'bs4'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/aleksejeei'
  },
  python_requires='>=3.10'
)