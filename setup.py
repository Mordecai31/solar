from setuptools import setup, find_packages

setup(
    name="solar-calculator",
    version="1.0.0",
    description="Solar System Calculator for Nigeria",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "streamlit>=1.28.0",
        "plotly>=5.17.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "pre-commit>=3.5.0"
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "xgboost>=2.0.0",
            "lightgbm>=4.1.0"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)