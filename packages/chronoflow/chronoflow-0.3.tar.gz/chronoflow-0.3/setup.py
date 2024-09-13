from setuptools import setup, find_packages

setup(
    name = "chronoflow",
    version='0.3',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'datetime': [
            'pytz',
            'datetime',
            'tzlocal',
        ],
        'ginter': [
            'gspread',
            'oauth2client',
            'google-api-python-client',
        ],
    },

)