from setuptools import setup

setup(
    name='classifier_linear',  
    version='0.5.0',  
    author='Anshuman Pattnaik',  
    author_email='helloanshu04@gmail.com',  
    description='A linear classifier built using tensorflow.', 
    long_description='lond description', 
    long_description_content_type='text/markdown',  
    url='https://github.com/ANSHPG',  
    packages=['classifier_linear'], 
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
)