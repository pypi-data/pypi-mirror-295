from setuptools import setup, find_packages
import os.path

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.1.2'
DESCRIPTION = 'Some simple utils.'

setup(
    name='tq_utils',
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://gitee.com/torchW/tqutils',
    author='TripleQuiz',
    author_email='triple_quiz@163.com',
    license='MIT',
    keywords=['python', 'util', 'code analyze', 'file manager', 'graph', 'dot', 'profile'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: Chinese (Simplified)',
    ],
    packages=find_packages(include=['tq_utils', 'tq_utils.*']),
    install_requires=[
        'pydot==3.0.1',
        'pygraphviz==1.11',
        'pyinstrument==4.6.2',
    ],
    include_package_data=True,
    exclude_package_data={},
    zip_safe=False,
)

"""
打包发布步骤：
1. 测试代码
2. commit & create tag
3. 打包源分发包和轮子，命令：python setup.py sdist bdist_wheel
4. PyPI发布，命令：twine upload -r tq_utils dist/*
"""
