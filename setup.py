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
        'alembic==0.8.2',
        'PyMySQL==0.6.6',
        'pyusb==1.0.0b1',
        'SQLAlchemy==1.0.8',
        'temperusb==1.2.3',
    ],
    tests_require=[
    ],
    entry_points={
    },
)
