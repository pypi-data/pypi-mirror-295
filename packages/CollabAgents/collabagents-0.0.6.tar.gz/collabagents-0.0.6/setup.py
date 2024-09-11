from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="CollabAgents",
    version="0.0.6",
    description=("""CollabAgents is a Python framework developed by Vishnu D. for developing AI agents equipped with specialized roles and tools to handle complex user requests efficiently. Users have 100 percent control over their prompts."""
    ),

    long_description=long_description,
    long_description_content_type="text/markdown",
    readme = "README.md",
    author="Vishnu.D",
    author_email="vishnujune17@gmail.com",
    license="MIT",
    keywords =["pip install CollabAgents","pip install collabagents"],
    packages=find_packages(),
    install_requires=[
            # Required Packages
            "instructor==1.3.4",
            "openai==1.40.1",
            "anthropic==0.34.1",
            "pandas==2.2.2",
            "pydantic==2.8.2",
            "pybase64==1.4.0",
            "requests==2.32.3",
            "tiktoken==0.7.0",
            "websocket-client==1.8.0",
            "lxml==5.3.0",
            "pytest-playwright==0.5.1",
            "scikit-learn==1.5.1",
            "statsmodels==0.14.2",
            "scipy==1.14.1",
            "transformers==4.44.2",
            "notebook==7.2.1",
            "requests==2.32.3",
            "beautifulsoup4==4.12.3",
            "openpyxl==3.1.5",
            "xlrd==2.0.1",
            "pyodbc==5.1.0",
            "matplotlib==3.9.2",
            "seaborn==0.13.2",
            "plotly==5.23.0",
            "kaleido==0.2.1",
            "chromadb==0.5.5",
            "semantic-text-splitter==0.15.0",
            "markdownify==0.13.1",
            "sentence-transformers==3.0.1",
            "Markdown==3.7",
            "nest-asyncio==1.6.0"
        ],


    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.12',
  ]
)