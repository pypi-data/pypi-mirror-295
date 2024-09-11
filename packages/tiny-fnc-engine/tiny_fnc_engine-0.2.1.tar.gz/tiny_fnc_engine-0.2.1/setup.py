from setuptools import setup, find_packages

# Declare the constants
PYPI_PACKAGES = ["setuptools", "wheel", "twine"]

def read_readme():
    """Read the README.md file and return its contents."""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()
    
def read_requirements() -> list[str]:
    """Read the requirements.txt file and return its contents."""
    def validate_line(line: str) -> bool:
        """Check if the line is valid."""
        line = line.strip()
        if line.startswith("#") or line == "\n" or line in PYPI_PACKAGES or line == "":
            return False
        return True
    
    with open("package_requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if validate_line(line)]


def main():
    setup(
        name='tiny_fnc_engine',
        version='0.2.1',
        description='Extremely lightweight and minimal function calling engine',
        long_description=read_readme(),
        long_description_content_type="text/markdown",
        author='Atakan Tekparmak',
        author_email='atakantekerparmak@gmail.com',
        url="https://github.com/AtakanTekparmak/tiny_fnc_engine",
        packages=find_packages(),
        install_requires=read_requirements(),
    )

if __name__ == "__main__":
    main()