from setuptools import setup, find_packages

setup(
    name='channelflowlib',
    version='0.9.0',
    description='Python library for open channel flow and hydraulics engineering calculations.',
    long_description='Python library for open channel flow and hydraulics engineering calculations.',
    url='https://github.com/alexiusacademia/ChannelFlowLib',
    author='Alexius Academia',
    author_email='alexius.sayco.academia@gmail.com',
    license='GNU GPL 3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='hydraulics open-channel fluid-flow',
    packages=find_packages(exclude=['tests*']),
    data_files=None
)
