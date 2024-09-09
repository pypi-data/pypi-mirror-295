# setup.py
from setuptools import setup, find_packages

setup(
    name="Ale2D",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "arcade",
        "pymunk"
    ],
    author="Tu Nombre",
    description="Un motor de juego 2D basado en Pygame y Arcade con físicas, carga de archivos y manejo de imágenes.",
    url="https://github.com/Alejandrix2456github/Ale2D-Engine",
)
