from setuptools import setup, find_packages

setup(
    name='god_ocr',  # Replace with your library name
    version='0.1.0',  # Initial version number
    description='OCR King',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='SORRY',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/your_project',  # Replace with your repository URL
    license='MIT',  # Your license type
    packages=find_packages(),  # Automatically find packages in the current directory
    install_requires=[  # List your dependencies here
        'PIL',
'argparse',
'benchmark',
'collections',
'concurrent',
'copy',
'cv2',
'dataclasses',
'datasets',
'dotenv',
'filetype',
'fitz',
'ftfy',
'functools',
'google',
'hashlib',
'io',
'itertools',
'json',
'llama',
'logging',
'math',
'numpy',
'os',
'playwright',
'pydantic',
'pydantic_settings',
'pypdfium2',
'pytesseract',
'random',
'rapidfuzz',
're',
'requests',
'streamlit',
'subprocess',
'surya',
'tabulate',
'the',
'time',
'tokenizers',
'torch',
'tqdm',
'transformers',
'typing',
'warnings'
    ],
    classifiers=[  # Additional metadata about your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Minimum Python version requirement
)
