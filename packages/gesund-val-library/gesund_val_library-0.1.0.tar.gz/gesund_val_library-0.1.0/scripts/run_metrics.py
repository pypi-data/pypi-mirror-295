#!/usr/bin/env python

import argparse
import json
import bson
from utils.io_utils import read_json, validate_json_format
import os
from metrics.classification.create_validation import ValidationCreation

def format_metrics(metrics):
    """ Format and print the metrics in a readable way """
    print("\nValidation Metrics:\n" + "-"*40)
    for metric, values in metrics['data'].items():
        print(f"{metric}:")
        for key, value in values.items():
            if isinstance(value, list):  # If it's a confidence interval
                value_str = f"{value[0]:.4f} to {value[1]:.4f}"
            else:
                value_str = f"{value:.4f}"
            print(f"    {key}: {value_str}")
        print("-"*40)

def main():
    parser = argparse.ArgumentParser(description='Run validation metrics calculation.')
    parser.add_argument('--annotations', type=str, required=True, help='Path to the JSON file with annotations.')
    parser.add_argument('--predictions', type=str, required=True, help='Path to the JSON file with predictions.')
    parser.add_argument('--class_mappings', type=str, required=True, help='Path to the JSON file with class mappings.')
    parser.add_argument('--output', type=str, help='Path to the output file to save the results (optional).', default=None)
    
    args = parser.parse_args()
    
    # Load JSON files
    try:
        successful_batch_data = read_json(args.predictions)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading predictions file: {e}")
        return
    
    try:
        annotation_data = read_json(args.annotations)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading annotations file: {e}")
        return
    
    try:
        class_mappings = read_json(args.class_mappings)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading class mappings file: {e}")
        return
    
    # Initialize metrics class and calculate metrics
    batch_job_id = str(bson.ObjectId())
    validation = ValidationCreation(batch_job_id)
    try:
        validation_data = validation.create_validation_collection_data(successful_batch_data, annotation_data)
        metrics = validation.load(validation_data, class_mappings)
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return
    
    # Print the validation data
    format_metrics(metrics)

    # Optionally save the validation data
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(metrics, f, indent=4)
            print(f"\nValidation Metrics saved to {args.output}")
        except Exception as e:
            print(f"Error saving validation metrics: {e}")

if __name__ == "__main__":
    main()
