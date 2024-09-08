from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()


setup(
    name="nysg_tools",
    version="0.7",
    packages=find_packages(),
    install_requires=["numpy", "pandas"],
    description="Una colección de herramientas utiles para los laboratorios de la UBA FCEN",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Santiago Noya",
    author_email="noyasantiagomail@gmail.com",
    url="https://github.com/Noya-santiago/nysg_tools",
)
