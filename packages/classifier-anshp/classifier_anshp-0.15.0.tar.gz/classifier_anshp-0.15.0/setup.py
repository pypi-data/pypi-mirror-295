from setuptools import setup

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='classifier_anshp',  
    version='0.15.0',  
    author='Anshuman Pattnaik',  
    author_email='helloanshu04@gmail.com',  
    description='A linear classifier built using tensorflow.', 
    long_description=description, 
    long_description_content_type='text/markdown',  
    url='https://github.com/ANSHPG/pypi-pkg-clsfr',  
    packages=['classifier_anshp'], 
    install_requires=[
        'tensorflow>=2.0.0',  
        'numpy>=1.18.0', 
    ], 
    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points = {
        "console_scripts":[
            "classifier-anshp = classifier_linear:clsfr",
            "dataset-1 = classifier_linear:dataset_1",
            "dataset-2 = classifier_linear:dataset_2"
        ],
    }, 
)