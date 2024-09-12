from setuptools import find_packages, setup
import subprocess
import sys
import os

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

def install_dependencies():
    # Install Poppler
    run_command("sudo yum install -y poppler-utils")
    
    # Install Tesseract
    run_command("sudo amazon-linux-extras install epel -y")
    run_command("sudo yum install -y tesseract")
    run_command("conda install -c conda-forge tesseract -y")

    # Set up PATH
    os.environ['PATH'] += ':/usr/bin'
    
    # Create startup scripts
    os.makedirs(os.path.expanduser('~/.ipython/profile_default/startup'), exist_ok=True)
    
    with open(os.path.expanduser('~/.ipython/profile_default/startup/add_to_path.py'), 'w') as f:
        f.write("import os\n")
        f.write("os.environ['PATH'] += ':/usr/bin'\n")

    print("Dependencies installed and PATH set up.")
    print("Please restart your kernel for changes to take effect.")

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="modelcrafter",
    version="0.0.3",
    description="An avahiai library which makes your Gen-AI tasks effortless",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avahi-org/avahiplatform",
    author="Avahi AWS",
    author_email="info@avahitech.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=["boto3>=1.34.160", "loguru>=0.7.2", "python-docx>=1.1.2", "PyMuPDF>=1.24.9", "pandas==2.0.0", "numpy==1.26.4", "docutils>=0.21", "langchain>=0.2.16",
                      "langchain_community>=0.2.16", "langchain-experimental>=0.0.64", 
                      "PyMySQL>=1.1.1", "tabulate>=0.9.0", "langchain-aws>=0.1.17","chromadb==0.5.3", "langchain-chroma>=0.1.3", "unstructured>=0.12.3", "unstructured[pdf]", "pillow>=10.4.0",
                      "pytesseract>=0.3.8",
                      ],
    extras_require={
        "dev": ["twine>=4.0.2"],
        "pdf": ["unstructured[pdf]"]
    },
    python_requires=">=3.9",
)
