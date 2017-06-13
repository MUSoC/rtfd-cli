from setuptools import setup, find_packages
import rtfd-cli

setup(name='rtfd-cli',
      version='0.1',
      description='CLI to download docs from ReadTheDocs.org',
      author='Nitanshu Vashistha',
      author_email='nitanshu.vzard@gmail.com',
      packages = find_packages(),
      entry_points={
            'console_scripts': [
                  'rtfd-cli = rtfd-cli.rtfd-cli:command_line',
            ]
      },
      url='https://github.com/MUSoC/rtfd-cli',
      keywords=['readthedocs', 'terminal', 'command-line', 'rtfd', 'python'],
      license='Add Later',
      classifiers=[],
      install_requires=[
            'requests',
            'BeautifulSoup4',
            'colorama',
            'json'
      ]
     )
