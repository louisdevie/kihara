import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='kihara',
    version='0.2.0',

    author='Louis DEVIE',
    author_email='louisdevie.contact@gmail.com',

    description='Something',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/louisdevie/kihara',

    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],

    packages=[
        'kihara',
    ],

    entry_points={
        'console_scripts': [
            'kihara = kihara.__main__:main',
            'kihara-download = kihara.download:main',
            'kihara-hide = kihara.hide:main',
            'kihara-extract = kihara.extract:main',
            'kihara-index = kihara.index:main',
            'kihara-link = kihara.link:main',
        ],
    },

    python_requires='>=3.8',
)
