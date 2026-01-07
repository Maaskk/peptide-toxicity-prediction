# Getting 5000-10000 Peptides - Complete Guide

## Quick Start (Automated - Gets ~5000-6000 immediately)

Just run these two commands:

```bash
python scripts/download_peptide_databases.py
python scripts/clean_and_merge_data.py
```

This will automatically:
- Download 500+ real peptides from UniProt
- Generate 5000 high-quality synthetic peptides per class
- Clean and merge everything
- Give you **~6000-8000 total peptides ready for training**

## Getting 10000+ Peptides (Manual Downloads Required)

To reach 10000+ peptides, download from these sources:

### 1. DBAASP (Best Source - 3000+ hemolytic peptides)

**Website**: https://dbaasp.org/

**Steps**:
1. Register free account at https://dbaasp.org/
2. Go to **Search → Advanced Search**
3. Set filters:
   - Target: `Mammalian cells`
   - Activity: `Hemolytic activity`
4. Click **Search**
5. Click **Download → CSV format**
6. Save as: `data/raw/downloads/dbaasp/hemolytic_peptides.csv`

**Expected columns**: `ID`, `Sequence`, `HC50`
- The script will automatically label based on HC50 values

### 2. APD3 (2000+ antimicrobial peptides)

**Website**: https://aps.unmc.edu/

**Steps**:
1. Go to https://aps.unmc.edu/download
2. Download **"All AMP sequences"** (FASTA format)
3. Download **"AMP with activity data"** (CSV format)
4. Save to:
   - `data/raw/downloads/apd3/APD_sequences.fasta`
   - `data/raw/downloads/apd3/APD_activity.csv`

### 3. DRAMP (1500+ peptides)

**Website**: http://dramp.cpu-bioinfor.org/

**Steps**:
1. Go to http://dramp.cpu-bioinfor.org/browse/DownloadDataPage.php
2. Download:
   - **"General AMPs"** (FASTA) - non-toxic
   - **"Hemolytic peptides"** (FASTA) - toxic
3. Save to:
   - `data/raw/downloads/dramp/general_amps.fasta`
   - `data/raw/downloads/dramp/hemolytic_peptides.fasta`

### 4. After Downloads

Once you've downloaded the files, just run:

```bash
python scripts/clean_and_merge_data.py
```

The script will automatically:
- Find all downloaded files
- Clean sequences (remove invalid amino acids)
- Remove duplicates
- Balance to get equal toxic/non-toxic samples
- Merge with synthetic data
- Save to your project's `data/raw/` folder

## Expected Results

| Source | Toxic | Non-toxic | Total |
|--------|-------|-----------|-------|
| UniProt (automated) | 500 | 500 | 1,000 |
| Synthetic (automated) | 5,000 | 5,000 | 10,000 |
| DBAASP (manual) | 2,000 | 1,000 | 3,000 |
| APD3 (manual) | 500 | 1,500 | 2,000 |
| DRAMP (manual) | 800 | 700 | 1,500 |
| **TOTAL** | **8,800** | **8,700** | **17,500** |

After balancing, you'll have **10,000 peptides** (5,000 toxic, 5,000 non-toxic).

## Data Quality

The scripts automatically:
- ✓ Remove invalid amino acids (only standard 20 AAs)
- ✓ Filter by length (5-100 amino acids)
- ✓ Remove exact duplicates
- ✓ Balance classes (50/50 toxic/non-toxic)
- ✓ Track sources for each peptide
- ✓ Save metadata and statistics

## Synthetic Data Quality

The synthetic peptides are based on:
- Real hemolytic peptide patterns (high lysine, amphipathic)
- Real antimicrobial peptide patterns (collagen-like, proline-rich)
- Variations include mutations, truncations, and extensions
- Validated to have realistic amino acid compositions

While not as good as real experimental data, they provide a solid foundation for training.

## Next Steps

After preparing data:

```bash
# Train models with new data
python scripts/train_pipeline.py

# Check results
ls results/
```

Your models will now train on **5000-10000 peptides** instead of 210!
