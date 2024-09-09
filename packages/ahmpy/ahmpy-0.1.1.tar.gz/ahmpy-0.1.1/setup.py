from setuptools import setup, find_packages

setup(
    name='ahmpy',
    version='0.1.1',
    author='nameingishard',
    author_email='2569674866@qq.com',
    description='tools for ahm company',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

    # 项目依赖
    install_requires=[
        'cos-python-sdk-v5',
        'opencv-python >= 4.10.0.84',
        'openpyxl >= 3.0.10',
    ],

)
