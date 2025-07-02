#!/usr/bin/env python3

import sys  # To allow reading of standard input when no file or string is given
import yaml #To process multi-document yaml files
import re # Regular expression for validating labels and formats
import argparse # to process CLI options and arguements
from datetime import datetime # Retrieve and pricess current year for label validation

def validate_cost_centre_label(resource):
    """
    Validates if a Kubernetes resource has a correct cost centre label.

    Returns True if valid, False otherwise.
    """
    # Get current year to validate YYYY part of the label
    current_year = datetime.now().year

    # Safely get metadata and labels dictionaries
    metadata = resource.get("metadata", {})
    labels = metadata.get("labels", {})

    # Get the cost centre label value
    label_value = labels.get("metadata.megatech.inc/cost-centre")
    if not label_value:
        return False  # Label missing

    # Validate label format: CC-NNN-YYYY
    pattern = r"^CC-(\d{3})-(\d{4})$"
    match = re.match(pattern, label_value)
    if not match:
        return False

    # Extract NNN and YYYY parts
    nnn = int(match.group(1))
    yyyy = int(match.group(2))

    # Validate NNN range
    if nnn < 50 or nnn > 150:
        return False

    # Validate year
    if yyyy != current_year:
        return False

    return True  # All checks passed

def main():
    """
    Main function to handle CLI arguments and input sources.
    """
    parser = argparse.ArgumentParser(
        description="Validate Kubernetes manifests for cost centre label correctness."
    )
    parser.add_argument("--file", type=str, help="Path to a YAML file containing manifests.")
    parser.add_argument("--string", type=str, help="YAML content as a string.")

    args = parser.parse_args()

    # Determine input source
    if args.file:
        with open(args.file, 'r') as f:
            input_text = f.read()
    elif args.string:
        input_text = args.string
    else:
        input_text = sys.stdin.read()

    try:
        docs = list(yaml.safe_load_all(input_text))
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        sys.exit(1)

    valid_count = 0
    invalid_count = 0

    for doc in docs:
        if doc is None:
            continue  # Skip empty documents
        if validate_cost_centre_label(doc):
            valid_count += 1
        else:
            invalid_count += 1

    print(f"Valid resources: {valid_count}")
    print(f"Invalid resources: {invalid_count}")


if __name__ == "__main__":
    main()

