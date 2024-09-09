from setuptools import setup, find_packages

setup(
    name="log-crafter",
    version="1.0.1",
    author="Teissier Léo",
    author_email="leo.teissier@numericable.fr",
    description="Une bibliothèque pour générer des logs",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/votre_utilisateur/logcraft",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "setuptools",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)