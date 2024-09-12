from setuptools import setup, find_packages

setup(
    name="djadjawdawdawdawdwadawdwadawdsadawdasdawdas",  # Paketinizin adı
    version="0.1",  # Sürüm numarası
    packages=find_packages(),  # Paketleri otomatik bulmak için
    include_package_data=True,  # README.md, LICENSE gibi dosyaları dahil etmek için
    install_requires=[],  # Gerekli bağımlılıkları ekleyebilirsiniz
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # PyPI'de README.md'yi Markdown olarak göstermek için
    author="Burak KAYA",
    author_email="burakkaya_2004@hotmail.com",
    url="https://github.com/username/package",  # Projenizin URL'si (GitHub, Bitbucket, vb.)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)