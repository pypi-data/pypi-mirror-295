# Validation Metrics Library

## Overview

This library provides tools for calculating validation metrics for predictions and annotations in machine learning workflows. It includes a command-line tool for computing and displaying validation metrics.

## Installation

To use this library, ensure you have the necessary dependencies installed in your environment. You can install them via `pip`:

```sh
pip install .
```

## Usage

### Command-Line Tool

The primary script for running validation metrics is `run_metrics.py`. This script calculates validation metrics based on JSON files containing predictions and annotations.

#### Arguments

- `annotations` (required): Path to the JSON file containing annotation data.
- `predictions` (required): Path to the JSON file containing prediction data.
- `class_mappings` (required): Path to the JSON file containing class_mappings data.
- `--output` (optional): Path to the file where the results will be saved. If not provided, the results will be printed to the console.

#### Example

1. **Basic Usage**: Print metrics to the console

   ```sh
   python run_metrics.py path/to/annotations.json path/to/predictions.json
   ```

2. **Save Metrics to File**: Save metrics to a specified file

   ```sh
   python -m scripts.run_metrics --annotations test_data/test_annotations_classification.json --predictions test_data/test_predictions_classification.json --class_mappings test_data/test_class_mappings.json --output ./testing.json
   ```
This command will execute the metrics calculation and save the results to `path/to/output.json`. If the `--output` flag is not provided, the results will be displayed directly in the console.

### Example JSON Inputs

- **Annotations (`test_annotations_classification.json`)**:
  ```json
  {
  "664df1bf782d9eb107789013": {
    "image_id": "664df1bf782d9eb107789013",
    "annotation": [
      {
        "id": "664dfb2085d8059c72b7b24a",
        "label": 0
      }
    ]
  },

  "664df1bf782d9eb107789015": {
    "image_id": "664df1bf782d9eb107789015",
    "annotation": [
      {
        "id": "664dfb2085d8059c72b7b24d",
        "label": 1
      }
    ]
  },
  ...
  }
  ```

- **Predictions (`test_predictions_classification.json`)**:
  ```json
  {
  "664df1bf782d9eb107789013": {
    "image_id": "664df1bf782d9eb107789013",
    "prediction_class": 1,
    "confidence": 0.731047693767988,
    "logits": [
      0.2689523062320121,
      0.731047693767988
    ],
    "loss": 16.11764907836914
  },

  "664df1bf782d9eb107789015": {
    "image_id": "664df1bf782d9eb107789015",
    "prediction_class": 1,
    "confidence": 0.7308736572776326,
    "logits": [
      0.26912634272236735,
      0.7308736572776326
    ],
    "loss": 0.007578411139547825
  },
  ...
  ```

- **Class Mappings (`test_class_mappings.json`)**:
  ```json
  {"0": "normal", "1": "pneumonia"}
  ```


### Example Outputs
#### Console Output

When results are printed to the console, they will be in the following format:

```json
Validation Metrics:
----------------------------------------
Accuracy:
    Validation: 0.4375
    Confidence_Interval: 0.2656 to 0.6094
----------------------------------------
Micro F1:
    Validation: 0.4375
    Confidence_Interval: 0.2656 to 0.6094
----------------------------------------
Macro F1:
    Validation: 0.4000
    Confidence_Interval: 0.2303 to 0.5697
----------------------------------------
AUC:
    Validation: 0.3996
    Confidence_Interval: 0.2299 to 0.5693
----------------------------------------
Precision:
    Validation: 0.4343
    Confidence_Interval: 0.2625 to 0.6060
----------------------------------------
Sensitivity:
    Validation: 0.4549
    Confidence_Interval: 0.2824 to 0.6274
----------------------------------------
Specificity:
    Validation: 0.4549
    Confidence_Interval: 0.2824 to 0.6274
----------------------------------------
Matthews C C:
    Validation: -0.1089
    Confidence_Interval: 0.0010 to 0.2168
----------------------------------------
```

#### Output File

If the --output flag is used, the metrics will be saved in the specified file path. The format of the saved file will be the same as the console output.
