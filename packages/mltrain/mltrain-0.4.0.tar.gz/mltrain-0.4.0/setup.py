from setuptools import setup, find_packages


with open("Description.txt", 'r') as f:
    description = f.read()
# print(description)

setup(
    name='mltrain',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tensorflow'
    ],
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/Abfa41/mltrain_python.git',
    author='Abdul Faatih Siddiqui',
    
)
