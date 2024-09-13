from setuptools import setup, find_packages

setup(
    name='sage_lib',  # El nombre del paquete
    version='0.1.5.18',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
	'imageio',
    ],
    entry_points={
        'console_scripts': [
            'sage = sage_lib.main:main',  # Establece 'sage' como el comando de consola
        ],
    },
)

