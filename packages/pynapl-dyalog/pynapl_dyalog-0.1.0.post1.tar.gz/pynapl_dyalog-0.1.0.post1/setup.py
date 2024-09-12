from setuptools import setup

setup(
    name="pynapl-dyalog",
    version='0.1.0post1',
    description='Python - Dyalog APL interface',
    long_description="This package allows communication between Python and Dyalog APL.",
    url='https://github.com/fastai/pynapl',
    author='Dyalog',
    author_email='support@dyalog.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: APL',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='apl dyalog-apl interface',
    packages=['pynapl'],
    package_data={
        'pynapl': [ 'Py.dyalog', 'PyTest.dyalog', 'WinPySlave.dyalog', 'IPC.dyalog', 'WinPySlave.dyapp' ]
    },
)

