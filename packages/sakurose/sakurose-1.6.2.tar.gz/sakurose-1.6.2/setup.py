from setuptools import setup, find_packages

setup(
    name='sakurose',
    version='1.6.2',
    description='SakuRose: Simplifica la creación de APIs, códigos y aplicaciones de Discord.',
    author='InsAnya606',
    author_email='insanyadev@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Pillow',
        'discord.py',
        'pytz'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)