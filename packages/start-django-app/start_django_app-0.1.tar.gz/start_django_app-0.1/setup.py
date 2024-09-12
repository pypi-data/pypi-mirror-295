from setuptools import setup, find_packages

setup(
    name="start-django-app",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "start-django-app=start_django_app.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
