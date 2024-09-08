from setuptools import setup, find_packages

setup(
    name='salascorp_descriptive',  # Nombre de la librería
    version='0.2.0',                # Versión inicial
    description='implifies descriptive analysis before building propensity models. It offers key features like descriptive stats, distribution tests, interactive visualizations, and variable transformations. Ideal for streamlining data prep and gaining insights before launching predictive models.',
    author='Oscar Ancizar Salas',
    author_email='salascorp@gmail.com',
    url='https://github.com/salascorp/salascorp_descriptive.git',  # URL del repositorio
    packages=find_packages(),       # Busca automáticamente paquetes
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'ipywidgets',
        'scipy',
    ],
)
