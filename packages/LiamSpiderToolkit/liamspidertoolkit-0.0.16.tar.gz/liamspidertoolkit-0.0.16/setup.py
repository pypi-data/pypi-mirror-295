from setuptools import setup, find_packages

setup(
    name='LiamSpiderToolkit',
    version='0.0.16',
    packages=find_packages(),
    package_data={'': ['*.txt', '*.md', '*.py', '*.in']},
    description='liam`s spader package, 我的私人自定义爬虫包.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Liam',
    author_email='a61628904@163.com',
    url='https://github.com/your-username/your-package',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'bs4'
        # 'sqlite3'
    ],
)
