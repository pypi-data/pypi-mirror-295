from setuptools import setup, find_packages

setup(
    name="my_custom_lib",  # Название пакета
    version="0.1.0",  # Версия
    description="A simple math library for basic operations",  # Краткое описание
    # long_description=open("README.md").read(),  # Полное описание из файла README
    long_description_content_type="text/markdown",  # Формат файла README
    author="PVPSMILE",  # Твоё имя
    author_email="frank01zeroy@gmail.com",  # Твой email
    url="https://github.com/PVPSMILE/my_custom_lib.git",  # URL на GitHub или другой сайт проекта
    license="MIT",  # Лицензия
    packages=find_packages(),  # Пакеты, которые нужно установить
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Минимальная версия Python
)
