from setuptools import setup, find_packages

setup(
    name='potatodb',
    version='1.0.3',
    license="MIT License with attribution requirement",
    author="Ranit Bhowmick",
    author_email='bhowmickranitking@duck.com',
    description='''PotatoDB is a lightweight, file-based NoSQL database for Python projects, designed for easy setup and use in small-scale applications. Ideal for developers seeking simple data persistence without the complexity of traditional databases.''',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kawai-Senpai/PotatoDB',
    download_url='https://github.com/Kawai-Senpai/PotatoDB',
    keywords=["NoSQL", "Database", "JSON", "Persistence", "Lightweight", "File-based"],
    install_requires=[],
)
