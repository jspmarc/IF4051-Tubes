from setuptools import setup, find_packages

print(find_packages(where="src"))

setup(
    name="common_python",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
