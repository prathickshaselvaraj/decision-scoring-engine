# Multi-Criteria Decision Scoring & Ranking System

## Overview

This project is a **Multi-Criteria Decision Scoring Engine** developed as part of a coding round assessment.
The goal is to rank multiple alternatives (vendors/projects/options) based on multiple criteria and their assigned weights.

Such scoring systems are commonly used in:

* Vendor evaluation and procurement decisions
* Project prioritization
* Selection and shortlisting workflows

The system reads input data from CSV files, normalizes the scores to a common scale, applies weights, calculates a final score for each alternative, ranks them from best to worst, and generates an explanation report showing how each criterion contributed to the final score.

---

## Model / Method Used

This solution uses the **Weighted Sum Model (WSM)**, which is a widely used technique in **Multi-Criteria Decision Making (MCDM)**.

The final score for an alternative is calculated as:

FinalScore = Σ (NormalizedScore × Weight)

---

## Input Files

### 1. criteria.csv

Defines the scoring criteria, their weights, and whether they should be minimized or maximized.

Columns:

* `criterion` → criterion name
* `weight` → weight of criterion (weights must sum to 1.0)
* `direction` → `benefit` or `cost`

Example:

```csv
criterion,weight,direction
cost_per_unit,0.25,cost
quality_score,0.20,benefit
delivery_days,0.15,cost
compliance_score,0.20,benefit
support_sla_hours,0.10,cost
warranty_months,0.10,benefit
```

---

### 2. scores.csv

Contains raw scores for each alternative for all criteria.

Columns:

* `alternative` → name of the alternative (vendor/project/etc.)
* all other columns must match criteria names from `criteria.csv`

Example:

```csv
alternative,cost_per_unit,quality_score,delivery_days,compliance_score,support_sla_hours,warranty_months
VendorA,520,8.6,12,92,6,24
VendorB,480,7.9,10,85,8,18
VendorC,550,9.2,15,96,5,36
```

---

## Normalization Logic

Since criteria may have different units and ranges (cost, days, rating, percentage, etc.), scores are normalized using **Min-Max normalization**.

### Benefit Criteria (higher is better)

Normalized = (x - min) / (max - min)

### Cost Criteria (lower is better)

Normalized = (max - x) / (max - min)

### Edge Case Handling

If `max == min` for a criterion (all alternatives have the same value), the normalized score is set to `1.0` for all alternatives to avoid division-by-zero and treat them equally.

---

## Output Files

After execution, the program generates:

### 1. ranked_output.csv

Contains:

* rank
* alternative name
* final score

Example:

```csv
rank,alternative,final_score
1,VendorG,0.750000
2,VendorC,0.645977
3,VendorA,0.640613
```

---

### 2. explanation_report.md

A detailed explanation report that includes:

* normalized score per criterion
* weight per criterion
* contribution per criterion
* final score
* top contributing criterion

This makes the ranking process transparent and easy to interpret.

---

## Validation Checks Implemented

The system validates input before processing:

* criteria file is not empty
* no duplicate criteria
* weights are numeric and non-negative
* weights sum to 1.0
* direction must be `benefit` or `cost`
* scores file contains `alternative` column
* all required criterion columns exist in scores file
* all score values are numeric
* alternative names cannot be empty

---

## Edge Cases Covered

* Division-by-zero prevention in normalization (`max == min`)
* invalid weights sum
* invalid direction values
* missing score columns
* non-numeric values
* empty alternative name
* identical alternatives (tie score scenario)

---

## How to Run

### Run using default dataset (`data/`)

```powershell
python -m src.main
```

### Run using custom dataset

```powershell
python -m src.main --criteria data\criteria.csv --scores data\scores.csv
```

### Run and store output in a custom folder

```powershell
python -m src.main --criteria data\criteria.csv --scores data\scores.csv --out outputs_final
```

### Run using test datasets (edge case validation)

To verify validation and edge case handling, test datasets are available in the `data_tests/` folder.

Example:

```powershell
python -m src.main --criteria data_tests\criteria_max_min.csv --scores data_tests\scores_max_min.csv --out outputs_test
```
This test case validates the normalization edge case where `max == min` for a criterion.

---

## Project Structure

```
decision-scoring-engine/
│
├── data/                      # main dataset
├── data_tests/                # test datasets for validation/edge cases
├── outputs/                   # generated output files
│
├── src/
│   ├── main.py                # entry point
│   ├── io_utils.py            # CSV reading/writing
│   ├── validators.py          # input validation
│   ├── normalizer.py          # normalization logic
│   ├── scorer.py              # weighted scoring logic
│   ├── ranker.py              # ranking logic
│   ├── reporter.py            # explanation report generator
│
├── README.md
└── requirements.txt
```

---

## Dependencies

No external libraries are required.
The project uses only the Python Standard Library.

---

## Author

Prathicksha S
Decision & Computing Sciences
Coimbatore Institute of Technology (CIT)

---
