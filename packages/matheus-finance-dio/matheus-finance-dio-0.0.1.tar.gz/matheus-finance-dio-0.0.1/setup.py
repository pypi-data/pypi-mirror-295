from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

# with open("requirements.txt") as f:
#     requirements = f.read().splitlines()

setup(
    name="matheus-finance-dio",
    version="0.0.1",
    author="Matheus Brito",
    author_email="mabrol23@gmail.com",
    description="Pacote básico para cálculo de valor presente de títulos públicos",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matheus-brito-dev/simple-package-template",
    packages=find_packages(),
    # install_requires=requirements,
    python_requires='>=3.8',
    license="MIT"
)