from setuptools import setup, find_packages

setup(
    name='gesund_val_library',
    version='0.1.2',
    author='Gesund AI',
    author_email='hammadbink@gmail.com',
    license="MIT",
    description='Gesund.ai package for running validation metrics for classification, semantic segmentation, instance segmentation, and object detection models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gesund-ai/gesund_val_library/tree/feat/first_release_classification',
    packages=find_packages(),  # This should find all sub-packages
    install_requires=[
        'bson',
        'jsonschema',
        'numpy',
        'scikit-learn',
        'pandas',
        'pydicom',
        'nibabel',
        'opencv-python',
        'SimpleITK',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
