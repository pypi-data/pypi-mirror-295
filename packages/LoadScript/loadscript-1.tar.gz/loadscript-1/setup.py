from setuptools import setup, find_packages

setup(
    name='LoadScript',
    version='1',
    packages=find_packages(),
    install_requires=[
        # Hier kannst du Abhängigkeiten auflisten, z.B. 'numpy>=1.21.0',
    ],
    author='321Remag',
    # author_email='deine.email@example.com',  # Optional
    description='A module to load and execute scripts from raw URLs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Pulse-External-Team/LoadScript',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
