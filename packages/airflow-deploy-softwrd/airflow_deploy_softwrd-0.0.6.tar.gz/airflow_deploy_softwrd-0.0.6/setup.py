from setuptools import setup, find_packages

setup(
    name="airflow_deploy_softwrd",
    version="0.0.6",
    author="Md Robiuddin",
    author_email="robiuddin@softwrd.ai",
    description="A Flask application to handle postman webhooks for deploying and taking down repositories.",
    long_description=open('README.md').read(),  # Ensure you have a README.md file
    long_description_content_type="text/markdown",
    url="https://github.com/softwrdai/airflow_deploy_softwrd",  # Replace with your repo URL
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.9',
    install_requires=[
        "Flask",
        "boto3",
    ],
    entry_points={
        "console_scripts": [
            "airflow_deploy_softwrd=airflow_deploy_softwrd.app:main",
        ]
    },
)