import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="minefob",
	version="1.0.3.1",
	author="Caleb North",
	author_email="contact@fivesixfive.dev",
	description="A package that provides full control over any Minehut server",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(include=["request"]),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6'
)
