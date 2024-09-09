from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name="dwarf_rotator",
    version="0.1.0",
    author="yeegie",
    long_description=open('readme.md').read(),
    author_email="lotus9200@gmail.com",
    package_dir={"": "src/proxy_rotator"},
    packages=find_packages(where="src/proxy_rotator"),
    include_package_data=True,
    description="Proxy helper, store and rotate proxies.",
    install_requires=required,
)
