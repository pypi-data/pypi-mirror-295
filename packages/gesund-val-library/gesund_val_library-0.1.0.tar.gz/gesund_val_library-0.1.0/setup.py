from setuptools import setup, find_packages

setup(
    name='gesund_val_library',
    version='0.1.0',
    author='Gesund AI',
    author_email='hammadbink@gmail.com',
    description='Gesund.ai package for running validation metrics for classification, semantic segmentation, instance segmentation, and object detection models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gesund-ai/gesund_val_library/tree/feat/first_release_classification',
    packages=find_packages(),
    install_requires=[
        'bson',
        'jsonschema',
        'numpy',         # Required for numerical operations
        'scikit-learn',  # Required for metrics calculations
        'pandas',        # Required for data handling
        'pydicom',       # Required for DICOM file handling
        'nibabel',       # Required for NIfTI file handling
        'opencv-python', # Required for image processing
        'SimpleITK',     # Required for medical image processing
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'run_metrics=gesund_val_library.scripts.run_metrics:main',
        ],
    },
)
