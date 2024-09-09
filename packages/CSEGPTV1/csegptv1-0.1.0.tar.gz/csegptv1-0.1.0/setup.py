from setuptools import setup, find_packages

setup(
    name='CSEGPTV1',  
    version='0.1.0',
    description='A Google Custom Search and Google Sheets integration for querying and logging results',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sulyman Anjolaoluwa',
    author_email='quaero24@gmail.com',
    url='https://github.com/Quaero-1/quaero',  
    packages=find_packages(), 
    install_requires=[
        'requests',
        'gspread',
        'oauth2client',
        'python-dotenv',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
