from setuptools import setup, find_packages
import rtfd

setup(name='rtfd-cli',
      version='0.1.1',
      description='CLI to download docs from ReadTheDocs.org',
      author='Nitanshu Vashistha',
      author_email='nitanshu.vzard@gmail.com',
      packages = find_packages(),
      entry_points={
            'console_scripts': [
                  'rtfd-cli = rtfd.rtfd:command_line',
            ]
      },
      url='https://github.com/MUSoC/rtfd-cli',
      keywords=['readthedocs', 'terminal', 'command-line', 'rtfd', 'python'],
      license='MIT',
      downlaod_url='https://github.com/nvzard/rtfd-cli/archive/0.1.1.tar.gz',
      classifiers=[],
      install_requires=[
            'requests',
            'BeautifulSoup4',
            'tqdm',
            'colorama'
      ]
     )
