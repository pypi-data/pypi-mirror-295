## ⚡ Patient Characterization for SNDS Data
This package provides tools for characterizing patients based on Electronic Health Records (EHR) from the SNDS data. It includes a variety of functions to identify different diseases, treatments, and patient characteristics.


**Features**

- Identify patients with specific diseases such as COPD, Hypertension, Diabetes, Cerebrovascular disease, Heart failure, Myocardial infarction, Chronic ischaemic heart disease, Stroke, Renal disease, Liver and pancreas diseases, Undernutrition, Parkinson's disease, Epilepsy, Psychiatric diseases, Peripheral vascular disease, Dyslipidemia.
- Determine whether patients have received specific treatments (chemotherapy, radiotherapy, surgery, etc.).
- Generate Snakey diagrams for visualizing patient treatment pathways.
- Support for adding or deleting specific treatment codes (surgery, radiotherapy, chemotherapy, endocrine therapy, targeted therapy).
- Determine if a patient is treated for specific conditions based on ICD-10 and ATC codes.
- Assess the quantity and dates of treatments.
- Identify neoadjuvant or adjuvant therapies.
- Calculate chemotherapy intervals.
- Identify tobacco and alcohol use.

**[📄 Documentation](https://docs.google.com/document/d/1BghK8JQGn6b9dgt7sP5SMTgyjGs5ucVTO-7dTivEyII/edit?usp=sharing)**

## 💾 Installation

```
pip install EHRPOP
```


## 🧠 Usage

Here's a basic example to get you started with using the package:

```
# Importing the Package
import EHRPOP as pchar
```

```
import pandas as pd

# First, load your EHR data into a DataFrame:
df = pd.read_csv('path_to_your_EHR_data.csv')

# Use the provided functions to characterize your patients. For example, to identify patients with COPD:
COPD_patients = pchar.isCOPD(df, 'COPD')
print(COPD_patients)

# You can generate Snakey diagrams to visualize patient treatment pathways:
pchar.SnakeyDiagram(df)

```
