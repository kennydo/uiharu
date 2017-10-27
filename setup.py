from setuptools import setup, find_packages


setup(
    name='uiharu',
    version='0.0.2',
    description='Python temperature sensor project',
    long_description='',
    url='https://github.com/kennydo/uiharu',
    author='Kenny Do',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
    ],
    keywords='temperature sensor',
    packages=find_packages(),
    install_requires=[
    ],
    tests_require=[
    ],
    entry_points={
        'console_scripts': [
            'uiharu-exporter = uiharu.bin.exporter:main',
        ],
    },
)
