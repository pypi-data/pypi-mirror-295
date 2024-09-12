from setuptools import setup, find_packages
setup(
    name='llm-parse-json',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    description='A simple JSON parsing tool that preprocesses and parses JSON strings.',
    author='li-xiu-qi',
    author_email='lixiuqixiaoke@qq.com',
    url='https://github.com/li-xiu-qi/llm-parse-json',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)