from setuptools import find_packages, setup

setup(
    name='generate_waveform',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        "numpy==1.24.4",
        "fastapi==0.114.0",
        "uvicorn==0.30.6"
    ],
    test_suite='tests',
    tests_require=[
        'pytest',
    ],
    author='Zahra Shamsi',
    author_email='zahra.shamsi@gmail.com',
    description='Generate waves',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
