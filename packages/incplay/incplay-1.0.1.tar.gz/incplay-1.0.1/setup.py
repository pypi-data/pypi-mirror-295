from setuptools import setup, find_packages
from io import open
from os import path
import pathlib
# Директория, в которой содержится этот файл
HERE = pathlib.Path(__file__).parent
# Текст README-файла
README = (HERE / "README.md").read_text()
# Автоматически собирает в requirements.txt все модули для install_requires, а также настраивает ссылки на зависимости
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup (
 name = 'incplay',
 description = 'A simple commandline app for searching and looking up opensource vulnerabilities',
 version = '1.0.1',
 packages = find_packages(), # list of all packages
 install_requires = install_requires,
 python_requires='>=2.7', # any python greater than 2.7
 entry_points='''
        [console_scripts]
        incplay=main
    ''',
 author="INCOM, LLC",
 keyword="onvif play",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
 url='https://github.com/zolinalexey/incplay',
 download_url='https://github.com/zolinalexey/incplay/archive/1.0.1.tar.gz',
  dependency_links=dependency_links,
  author_email='zolinalexey@gmail.com',
  classifiers=[
            "Programming Language :: Python :: 3.7",
    ]
)