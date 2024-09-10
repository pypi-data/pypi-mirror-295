https://packaging.python.org/en/latest/tutorials/packaging-projects/

from setuptools import setup, find_packages

setup(name='power_nlp_cpu',
		version='1.0',
		description='power_nlp_cpu',
		url='https://github.com/ExpertOfAI/power_nlp',
		author='ExpertOfAI1',
		license='MIT',
		packages=find_packages(),
		classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		],
		python_requires='>=3.6',
		)
pip install twine		
python setup.py sdist

twine upload dist/*
<Enter API token , created from pypi account "create api token">