# 📄 Kubernetes Cost Centre Label Validator

            ┌─────────────┐        ┌─────────────┐
            │  YAML file  │──────▶ │             │
            └─────────────┘        │             │
                                   │             │
            ┌──────────────┐       │             │       ┌─────────────┐
            │  String Arg  │────▶  │  Validator  │────▶ │  Summary    │
            └──────────────┘       │   Script    │       │  Output     │
                                   │             │       │ (Valid /    │
            ┌─────────────┐        │             │       │  Invalid)   │
            │   stdin     │──────▶ │             │       └─────────────┘
            └─────────────┘        └─────────────┘


## ✨ Overview

This is a simple, lightweight Python CLI tool designed to validate Kubernetes manifests for the presence and correctness of a mandatory **cost centre label**.

At MegaTech (fictitious), all Kubernetes resources must include the label:

"metadata.megatech.inc/cost-centre: CC-NNN-YYYY"


Where:
- `NNN` is a 3-digit number **between 050 and 150** (inclusive).
- `YYYY` must match the **current calendar year**.

This tool ensures that all resources comply with this requirement before deployment.

---

## 💡 Problem it solves

In large organizations, cost allocation and chargebacks are critical. Missing or incorrect cost centre labels make it difficult to track cloud expenses and assign costs to the right teams.

This validator can be used:
- Locally by developers before committing YAML.
- In CI/CD pipelines to enforce governance and policy compliance.

---

## ⚙️ How it works

The script:
1. Parses Kubernetes YAML manifests (supports multiple documents separated by `---`).
2. Checks if each resource has the required label under `metadata.labels`.
3. Validates that the label:
   - Matches the regex format `CC-NNN-YYYY`.
   - Has `NNN` between 050 and 150.
   - Has `YYYY` equal to the current year.
4. Prints a summary of **valid** and **invalid** resources.

---

## 🚀 Usage

### ✅ Install dependencies

```bash
# pip install pyyaml

✅ Run the script
You can provide input in three ways:

1️⃣ From a file
# python validator.py --file my-manifests.yaml

2️⃣ From a string

# python validator.py --string "apiVersion: v1\nkind: Namespace\nmetadata:\n  labels:\n    metadata.megatech.inc/cost-centre: CC-071-2025\n  name: example-ns"

3️⃣ From stdin (default)
# cat my-manifests.yaml | python validator.py

✅ Example output
Valid resources: 2
Invalid resources: 2

💬 Example YAML input
apiVersion: v1
kind: Namespace
metadata:
  labels:
    metadata.megatech.inc/cost-centre: CC-071-2025
  name: payments-service
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    metadata.megatech.inc/cost-centre: CC-071-2024
  name: payments-sa
  namespace: payments-service
---
apiVersion: v1
kind: Namespace
metadata:
  name: notification-service
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    metadata.megatech.inc/cost-centre: CC-113-2025
  name: alert-sa
  namespace: notification-service

#In this example, assuming the current year is 2025, resources with 2024 or missing labels will be counted as invalid.

✅ Script logic overview
Reads YAML content (file, string, or stdin).
Iterates over each document.
Uses a regular expression to check the label format.
Checks numeric constraints for NNN.
Verifies YYYY equals the current year.


🛡️ Assumptions
The label must always be found under metadata.labels.
Missing or improperly formatted labels cause the resource to be marked invalid.
Only current year is accepted for YYYY.


💡 Possible future enhancements
Output detailed per-resource report (including resource name and reason for failure).
Support writing results to a file.
Add support for specifying the valid year range via a flag.
Include optional strict mode to fail pipeline runs.

🧑‍💻 Author
Karthik Shekar
Created: July 2025

📄 License
This script is provided as-is for assessment and demonstration purposes.