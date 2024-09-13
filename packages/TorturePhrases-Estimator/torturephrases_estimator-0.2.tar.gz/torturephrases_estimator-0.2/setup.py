from setuptools import setup, find_packages

setup(
    name='TorturePhrases_Estimator',
    version='0.2',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    description='A Python package to identify tortured phrases in text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Usman',
    author_email='usman.alot761@gmail.com',
    url='https://github.com/Usman761/TorturePhrases_Estimator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        'TorturePhrases_Estimator': ['tortured_phrases_list.txt'],
    },
)
