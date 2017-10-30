from setuptools import setup, find_packages

setup(
    name='channelflowlib',
    version='0.6.2',
    description='Python modules for channel flow and hydraulics engineering.',
    url='https://github.com/alexiusacademia/ChannelFlowLib',
    author='Alexius Academia',
    author_email='alexius.academia@gmail.com',
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
