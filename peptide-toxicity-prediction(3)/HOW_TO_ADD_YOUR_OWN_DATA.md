# How to Add Your Own Data for Training

## Quick Guide

If you have downloaded a file with peptide sequences, here's how to add them to train the model.

## Step 1: Prepare Your Data File

Your file should be in **FASTA format** or **CSV format**.

### Option A: FASTA Format (Recommended)

Create a file like `my_toxic_peptides.fasta`:

```
>toxic_peptide_1|my_source
GIGAVLKVLTTGLPALISWIKRKRQQ
>toxic_peptide_2|my_source
KWKLFKKIEKVGQNIRDGIIKAGPAVAVVGQATQIAK
>toxic_peptide_3|my_source
KLAKLAKKLAKLAK
```

**Format:**
- Header line starts with `>`
- Can include description: `>id|description|source`
- Sequence on next line (only standard amino acids: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y)
- Each sequence on separate lines

### Option B: CSV Format

Create a file like `my_peptides.csv`:

```csv
Sequence,Label,Source
GIGAVLKVLTTGLPALISWIKRKRQQ,1,my_source
KWKLFKKIEKVGQNIRDGIIKAGPAVAVVGQATQIAK,1,my_source
GIVEQCCTSICSLYQLENYCN,0,my_source
```

**Columns:**
- `Sequence`: Peptide sequence (required)
- `Label`: 1 for toxic, 0 for non-toxic (required)
- `Source`: Your data source name (optional)

## Step 2: Place Your Files

Put your files in the `data/raw/` directory:

```bash
# For FASTA files
data/raw/my_toxic_peptides.fasta
data/raw/my_nontoxic_peptides.fasta

# OR for CSV
data/raw/my_peptides.csv
```

## Step 3: Update the Data Loader (If Needed)

### If Using FASTA Files

The existing `src/data_loader.py` already supports FASTA files. Just make sure your files are named:
- `toxic_peptides.fasta` (or it will merge with existing)
- `nontoxic_peptides.fasta` (or it will merge with existing)

### If Using CSV Files

You'll need to convert CSV to FASTA first. Use this script:

```python
# convert_csv_to_fasta.py
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Read CSV
df = pd.read_csv('data/raw/my_peptides.csv')

# Separate toxic and non-toxic
toxic = df[df['Label'] == 1]
nontoxic = df[df['Label'] == 0]

# Write FASTA files
with open('data/raw/my_toxic_peptides.fasta', 'w') as f:
    for i, row in toxic.iterrows():
        f.write(f">peptide_{i}|{row.get('Source', 'custom')}\n{row['Sequence']}\n")

with open('data/raw/my_nontoxic_peptides.fasta', 'w') as f:
    for i, row in nontoxic.iterrows():
        f.write(f">peptide_{i}|{row.get('Source', 'custom')}\n{row['Sequence']}\n")
```

## Step 4: Merge with Existing Data

### Option A: Use the Clean and Merge Script

The `clean_and_merge_data.py` script will automatically find and merge your files:

```bash
python scripts/clean_and_merge_data.py
```

This script:
- Finds all FASTA files in `data/raw/`
- Cleans sequences (removes invalid amino acids)
- Removes duplicates
- Balances classes
- Saves to `data/raw/toxic_peptides.fasta` and `data/raw/nontoxic_peptides.fasta`

### Option B: Manual Merge

If you want to manually add your sequences:

```bash
# Append your toxic sequences
cat data/raw/my_toxic_peptides.fasta >> data/raw/toxic_peptides.fasta

# Append your non-toxic sequences
cat data/raw/my_nontoxic_peptides.fasta >> data/raw/nontoxic_peptides.fasta
```

Then run the clean script:
```bash
python scripts/clean_and_merge_data.py
```

## Step 5: Train with Your Data

After merging, train the models:

```bash
python scripts/train_pipeline.py
```

The training will use:
- Your custom sequences
- Existing sequences
- All merged together

## Example: Complete Workflow

```bash
# 1. Place your file
cp /path/to/your/sequences.fasta data/raw/my_sequences.fasta

# 2. If CSV, convert to FASTA first
python convert_csv_to_fasta.py  # (create this script if needed)

# 3. Merge with existing data
python scripts/clean_and_merge_data.py

# 4. Train models
python scripts/train_pipeline.py

# 5. Check results
cat data/raw/dataset_info.txt  # See how many sequences were used
ls results/  # See trained models and visualizations
```

## Data Requirements

Your sequences must:
- ✅ Use only standard 20 amino acids: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y
- ✅ Be at least 5 amino acids long
- ✅ Be at most 100 amino acids long
- ✅ Have clear labels (toxic=1, non-toxic=0)

## Checking Your Data

Before training, verify your data:

```bash
# Count sequences
grep -c "^>" data/raw/my_toxic_peptides.fasta
grep -c "^>" data/raw/my_nontoxic_peptides.fasta

# Check format
head -5 data/raw/my_toxic_peptides.fasta

# Validate sequences (check for invalid amino acids)
python3 -c "
from Bio import SeqIO
import sys

file = 'data/raw/my_toxic_peptides.fasta'
valid_aas = set('ACDEFGHIKLMNPQRSTVWY')
invalid = []

for record in SeqIO.parse(file, 'fasta'):
    seq = str(record.seq).upper()
    invalid_aas = set(seq) - valid_aas
    if invalid_aas:
        invalid.append((record.id, invalid_aas))

if invalid:
    print('⚠ Invalid amino acids found:')
    for seq_id, aas in invalid[:10]:
        print(f'  {seq_id}: {aas}')
else:
    print('✓ All sequences are valid!')
"
```

## Troubleshooting

### Problem: "Invalid amino acids found"
**Solution:** Remove sequences with non-standard amino acids (B, J, O, U, X, Z, etc.)

### Problem: "Too many duplicates"
**Solution:** The clean script will automatically remove duplicates

### Problem: "Imbalanced classes"
**Solution:** The clean script will balance automatically (50/50 split)

### Problem: "File not found"
**Solution:** Make sure files are in `data/raw/` directory

## Quick Reference

**File locations:**
- Your data: `data/raw/my_*.fasta` or `data/raw/my_*.csv`
- Merged data: `data/raw/toxic_peptides.fasta` and `data/raw/nontoxic_peptides.fasta`
- Trained models: `results/trained_models.pkl`
- Dataset info: `data/raw/dataset_info.txt`

**Key commands:**
```bash
# Merge data
python scripts/clean_and_merge_data.py

# Train models
python scripts/train_pipeline.py

# Check dataset size
cat data/raw/dataset_info.txt
```



