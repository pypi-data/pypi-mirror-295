from setuptools import setup, find_packages

setup(
    name='hein-hplc',
    version='0.2.3',
    packages=find_packages(),
    include_package_data=True,
    description='This web app analyze deconvoluted HPLC peaks and plot time course data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ivory Zhang',
    author_email='ivoryzhang@chem.ubc.ca',
    license='MIT',
    install_requires=[
        "dash-bootstrap-components",
        "pandas",
        "scipy",
        "plotly",
        "numpy",
        "rainbow-api",
    ],
    entry_points={
        'console_scripts': [
            'hein-hplc=hein_hplc.app:main',
        ],
    },
    url='https://gitlab.com/heingroup/hein-hplc'
)
