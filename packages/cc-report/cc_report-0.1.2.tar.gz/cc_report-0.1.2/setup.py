# -*- coding: utf-8 -*-
# @Time   :08/05/2024 6:03 pm
# @Author :UPEX_FCC
# @Email  :cc.cheng@bitget.com
# @Site   :
# @File   :setup.py

import setuptools

setuptools.setup(
    name='cc_report',
    version='0.1.2',
    packages=setuptools.find_packages(),
    license='MIT',
    author='cc.cheng',
    author_email='chaicc145@gmail.com',
    description='A MODIFIED REPORT',
    install_requires=['pytest'],
    # 静态文件依赖
    package_data={"": ['*.html']},
    # pypi插件分类器
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pytest"
    ],
    # 指定插件文件
    entry_points={"pytest11": ["testreport = cc_report.pytest_testreport"]},
    python_requires='>=3.6',
)
