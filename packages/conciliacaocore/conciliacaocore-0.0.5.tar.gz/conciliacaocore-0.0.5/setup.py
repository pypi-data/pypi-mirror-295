from setuptools import setup, find_packages

setup(
    name="conciliacaocore",
    version="0.0.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "psycopg2-binary>=2.9.5",
        "pyspark>=3.3.2",
    ],
    author="Fernando Miranda Calil",
    author_email="fcalil@sdnadigital.com",
    description="Utilitários comuns para projetos de conciliação",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sdna-team/okto/sdna-conciliacao",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
