from setuptools import setup, find_packages

setup(
    name='ArpMitmProject',
    version='0.1',
    description='A Python library for ARP spoofing and MITM attacks.',
    author='Matan',
    author_email='matannafgi@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Nathanafgi/ArpMitmProject",
    packages=find_packages(),
    install_requires=['scapy'],
    entry_points={
        'console_scripts': [
            'ArpMitmProject = ArpMitmProject.mitm:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
