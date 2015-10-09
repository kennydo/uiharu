from setuptools import setup, find_packages


setup(
    name='uiharu',
    version='0.0.1',
    description='Python temperature sensor project',
    long_description='',
    url='https://github.com/kennydo/uiharu',
    author='Kenny Do',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
    ],
    keywords='temperature sensor',
    packages=find_packages(),
    install_requires=[
        'influxdb==2.9.2',
        'simplejson==3.8.0',
    ],
    tests_require=[
    ],
    entry_points={
        'console_scripts': [
            'uiharu-collector = uiharu.bin.collector:main',
            'uiharu-server = uiharu.bin.server:main',
        ],
    },
)
