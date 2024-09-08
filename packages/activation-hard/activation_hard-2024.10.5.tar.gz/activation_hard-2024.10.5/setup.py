# coding: utf-8
import os,shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name='activation-hard',  # 包名
    version='2024.10.5',  # 版本号
    description='权限激活相关',
    long_description='',
    author='tencent',
    author_email='pengluan@tencent.com',
    url='https://github.com/data-infra/cube-studio',
    license='',
    install_requires=[
        'PySnooper',
        'kubernetes',
        "cryptography"
    ],
    python_requires='>=3.6',
    keywords='',
    packages=find_packages(),  # 必填 包含所有的py文件
    package_data={
        '': ['*.so'],
    },
    # package_dir={'': 'activation'},  # 必填 包的地址
    include_package_data=True,  # 将数据文件也打包
    )
