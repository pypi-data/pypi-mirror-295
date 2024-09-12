import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="combinatorlite",
    version="1.9",
    author="Swarna Kamal Paul",
    author_email="swarna.kpaul@gmail.com",
    description="The programming model to integrate AI components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swarna-kpaul/combinatorlite",
    project_urls={
        "Bug Tracker": "https://github.com/swarna-kpaul/combinatorlite/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
	keywords = ['programming model', 'dataflow graph', 'functional programming','Integrative AI'],
	install_requires=[ 'requests']
)