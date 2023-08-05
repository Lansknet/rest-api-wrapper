from setuptools import setup, find_packages

# Récupère le contenu du fichier README.md pour l'utiliser comme description longue.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lansknet_api_wrapper',
    version='0.1',
    packages=find_packages(),  # Spécifie le dossier contenant le code
    install_requires=[
        'aiohttp',
        'requests',
    ],
    url='https://github.com/Lansknet/rest-api-wrapper',
    author='Arthur Vasseur',
    author_email='arthur.vasseur@epitech.eu',
    description='A wrapper for the Lansknet API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Assurez-vous que cela correspond à votre licence dans le fichier LICENSE.
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Spécifiez la version minimale de Python requise.
)