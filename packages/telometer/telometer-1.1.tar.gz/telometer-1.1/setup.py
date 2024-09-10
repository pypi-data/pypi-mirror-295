import setuptools

setuptools.setup(
    name="telometer",
    version="1.01",
    author="Santiago E Sanchez",
    author_email="ses94@stanford.edu",
    description="a simple regular expression based method for measuring individual, chromosome-specific telomere lengths from long-read sequencing data",
    packages=setuptools.find_packages(),
    license='MIT',
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'telometer=telometer:run_telometer',  # 'telometer' is the command, 'telometer:main' means the main function in telometer.py
        ],
    },
)
