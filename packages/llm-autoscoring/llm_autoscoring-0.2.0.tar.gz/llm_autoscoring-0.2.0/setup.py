from setuptools import setup, find_packages

setup(
    name="llm_autoscoring",
    version="0.2.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "numpy",
        "scikit-learn",
        "nltk",
        "python-dateutil",
        "openai",
        "spacy",
    ],
    extras_require={
        "dev": ["pytest", "black", "isort", "mypy", "flake8"],
    },
    author="David Bustos Usta",
    author_email="david.bustos@us.dlapiper.com",
    description="A library for AutoScoring LLM extraction processes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm_autoscoring",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)