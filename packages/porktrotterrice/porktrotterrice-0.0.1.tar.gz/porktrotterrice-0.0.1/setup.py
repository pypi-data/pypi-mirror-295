"""Setup for the chocobo package."""
import setuptools
with open('README.md') as f:
    README = f.read()
setuptools.setup(
    author="wuchongchong",
    author_email="137928049@qq.com",
    name='porktrotterrice',
    license="MIT",
    description='好吃的猪脚饭',
    version='v0.0.1',
    long_description=README,
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
)