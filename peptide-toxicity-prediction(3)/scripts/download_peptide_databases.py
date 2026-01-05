"""
Download peptide data from multiple public databases.

This script downloads data from:
1. DBAASP - Database of Antimicrobial Activity and Structure of Peptides
2. APD3 - Antimicrobial Peptide Database
3. UniProt - Toxin peptides from UniProt
4. DRAMP - Data Repository of Antimicrobial Peptides

Target: 5000+ peptides with clear toxic/non-toxic labels
"""

import requests
import urllib.request
import os
import time
import pandas as pd
from Bio import SeqIO
from io import StringIO
import json


def create_directories():
    """Create necessary directories for downloaded data."""
    directories = [
        'data/raw/downloads',
        'data/raw/downloads/dbaasp',
        'data/raw/downloads/apd3',
        'data/raw/downloads/uniprot',
        'data/raw/downloads/dramp'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("[v0] Created download directories")


def download_dbaasp_data():
    """
    Download hemolytic peptide data from DBAASP.
    
    Note: DBAASP requires registration for bulk downloads.
    This function provides instructions and downloads sample data.
    """
    print("\n=== Downloading DBAASP Data ===")
    output_dir = 'data/raw/downloads/dbaasp'
    
    # Instructions for manual download
    instructions = """
    DBAASP (Database of Antimicrobial Activity and Structure of Peptides)
    Website: https://dbaasp.org/
    
    To download data:
    1. Register for free account at https://dbaasp.org/
    2. Go to Search > Advanced Search
    3. Filter by:
       - Target: Mammalian cells (for cytotoxicity)
       - Activity: Hemolytic activity
    4. Download results as CSV
    5. Save to: data/raw/downloads/dbaasp/hemolytic_peptides.csv
    
    Expected columns: ID, Sequence, HC50 (hemolytic concentration)
    - HC50 < 100 μg/mL = toxic (label=1)
    - HC50 > 100 μg/mL = non-toxic (label=0)
    """
    
    # Save instructions
    with open(f'{output_dir}/DOWNLOAD_INSTRUCTIONS.txt', 'w') as f:
        f.write(instructions)
    
    print(instructions)
    
    # Check if user has already downloaded the file
    manual_file = f'{output_dir}/hemolytic_peptides.csv'
    if os.path.exists(manual_file):
        print(f"\n✓ Found manually downloaded file: {manual_file}")
        return True
    else:
        print(f"\n⚠ Please download DBAASP data manually and place at: {manual_file}")
        return False


def download_apd3_data():
    """
    Download data from APD3 (Antimicrobial Peptide Database).
    
    APD3 provides downloadable datasets of antimicrobial peptides.
    """
    print("\n=== Downloading APD3 Data ===")
    output_dir = 'data/raw/downloads/apd3'
    
    # APD3 download instructions
    instructions = """
    APD3 (Antimicrobial Peptide Database)
    Website: https://aps.unmc.edu/
    
    To download data:
    1. Go to https://aps.unmc.edu/download
    2. Download "All AMP sequences" (FASTA format)
    3. Download "AMP with activity data" (CSV format)
    4. Save files to: data/raw/downloads/apd3/
    
    Files needed:
    - APD_sequences.fasta (all sequences)
    - APD_activity.csv (activity annotations including hemolytic activity)
    
    Labeling:
    - Hemolytic activity present = toxic (label=1)
    - No hemolytic activity = non-toxic (label=0)
    """
    
    with open(f'{output_dir}/DOWNLOAD_INSTRUCTIONS.txt', 'w') as f:
        f.write(instructions)
    
    print(instructions)
    
    # Check for downloaded files
    fasta_file = f'{output_dir}/APD_sequences.fasta'
    activity_file = f'{output_dir}/APD_activity.csv'
    
    if os.path.exists(fasta_file) and os.path.exists(activity_file):
        print(f"\n✓ Found APD3 files")
        return True
    else:
        print(f"\n⚠ Please download APD3 data manually")
        return False


def download_uniprot_toxic_peptides():
    """
    Download toxic peptides from UniProt using REST API.
    
    Queries UniProt for peptides with toxin annotations.
    """
    print("\n=== Downloading UniProt Toxic Peptides ===")
    output_dir = 'data/raw/downloads/uniprot'
    
    # UniProt REST API query for toxins
    # Query: keyword:toxin AND length:[10 TO 50] (peptide range)
    base_url = "https://rest.uniprot.org/uniprotkb/stream"
    
    # Query parameters for toxic peptides
    toxic_params = {
        'query': '(keyword:KW-0800) AND (length:[10 TO 100])',  # KW-0800 = Toxin
        'format': 'fasta',
        'size': '500'
    }
    
    toxic_output = f'{output_dir}/uniprot_toxic_peptides.fasta'
    
    print(f"Querying UniProt for toxic peptides...")
    try:
        response = requests.get(base_url, params=toxic_params, timeout=60)
        if response.status_code == 200:
            with open(toxic_output, 'w') as f:
                f.write(response.text)
            
            # Count sequences
            count = response.text.count('>')
            print(f"✓ Downloaded {count} toxic peptides from UniProt")
            return True
        else:
            print(f"✗ UniProt request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error downloading from UniProt: {e}")
        return False


def download_uniprot_antimicrobial_peptides():
    """
    Download antimicrobial peptides from UniProt (typically non-toxic).
    """
    print("\n=== Downloading UniProt Antimicrobial Peptides (Non-toxic) ===")
    output_dir = 'data/raw/downloads/uniprot'
    
    # Query for antimicrobial peptides without toxin annotations
    base_url = "https://rest.uniprot.org/uniprotkb/stream"
    
    amp_params = {
        'query': '(keyword:KW-0929) AND NOT (keyword:KW-0800) AND (length:[10 TO 100])',  # KW-0929 = Antimicrobial, NOT Toxin
        'format': 'fasta',
        'size': '500'
    }
    
    amp_output = f'{output_dir}/uniprot_amp_nontoxic.fasta'
    
    print(f"Querying UniProt for antimicrobial peptides...")
    try:
        response = requests.get(base_url, params=amp_params, timeout=60)
        if response.status_code == 200:
            with open(amp_output, 'w') as f:
                f.write(response.text)
            
            count = response.text.count('>')
            print(f"✓ Downloaded {count} non-toxic antimicrobial peptides from UniProt")
            return True
        else:
            print(f"✗ UniProt request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error downloading from UniProt: {e}")
        return False


def download_dramp_data():
    """
    Download data from DRAMP (Data Repository of Antimicrobial Peptides).
    """
    print("\n=== Downloading DRAMP Data ===")
    output_dir = 'data/raw/downloads/dramp'
    
    instructions = """
    DRAMP (Data Repository of Antimicrobial Peptides)
    Website: http://dramp.cpu-bioinfor.org/
    
    To download data:
    1. Go to http://dramp.cpu-bioinfor.org/browse/DownloadDataPage.php
    2. Download "General AMPs" (FASTA format)
    3. Download "Hemolytic peptides" (FASTA format)
    4. Save to: data/raw/downloads/dramp/
    
    Files needed:
    - general_amps.fasta (non-toxic antimicrobial peptides)
    - hemolytic_peptides.fasta (toxic peptides)
    """
    
    with open(f'{output_dir}/DOWNLOAD_INSTRUCTIONS.txt', 'w') as f:
        f.write(instructions)
    
    print(instructions)
    
    general_file = f'{output_dir}/general_amps.fasta'
    hemolytic_file = f'{output_dir}/hemolytic_peptides.fasta'
    
    if os.path.exists(general_file) or os.path.exists(hemolytic_file):
        print(f"\n✓ Found DRAMP files")
        return True
    else:
        print(f"\n⚠ Please download DRAMP data manually")
        return False


def create_synthetic_data():
    """
    Generate synthetic toxic and non-toxic peptides for initial testing.
    This provides immediate data while waiting for manual downloads.
    """
    print("\n=== Generating Synthetic Data ===")
    output_dir = 'data/raw/downloads'
    
    toxic_patterns = [
        'KLAKLAKKLAKLAK',
        'KWKLFKKIEKVGQNIRDGIIKAGPAVAVVG',
        'GIGAVLKVLTTGLPALISWIKRKRQQ',
        'GIGKFLKKAKKFGKAFVKILKK',
        'FLGALFKALSKLL',
        'RRRPRPPYLPRPRPPPFFPPRLPPRIPPGFPPRFPPRFP',
        'KWKLFKKIGAVLKVL',
        'GIGKFLHSAGKFGKAFVGQIMNS',
        'KLALKLALKALKAALKLA',
        'RRWRIVVIRVRRC',
        'KWKLFKKIGIGKFLQSAKKF',
        'FFWKLLKSLSKKLLKK',
        'KRLFKKLLFKKLLK',
        'RWKIVVIRVAVLRR',
        'KKLFKKILKKL',
        'GLFGKLIKKFGKKAVGKLDAL',
        'FKRLKKLFKKL',
        'KRFWWWKLLKLW',
        'FKKLKKLFKLAKKF',
        'RWRFYKKLKKK',
        'KLAKKLAKLAKLAKLAKLA',
        'FKLAKKFAKKLAKK',
        'KRWRILWKVLRR',
        'KKFKKLFKKLSPVIPLLH',
        'GIGKFLHSAKKFGKAFVGEIMNS',
        'KWKLFKKIGKFLQSAKKFGK',
        'FFWKLLRKLL',
        'KRLFKKLLFKKLSK',
        'RWKIVVIRVRVR',
        'KKLFKKILKKVL'
    ]
    
    nontoxic_patterns = [
        'GHPQGPPGPPGPPG',
        'GPSGPQGPAGPPGPIG',
        'APGDQGPQGPAGPKG',
        'DRVYIHPFHL',
        'YPFPGPIPNSL',
        'LPGPPGPPGNIGFPGPKGPTG',
        'GEGGGPVGPQGPSG',
        'QGPSGPQGPPGPPG',
        'GPGGPPGPPGPPG',
        'DPPGPMGPMGPPGLAG',
        'VPGESGPQGSPGPQG',
        'FPGERGVQGPPGPQG',
        'GQPGARGPQGPSGPPG',
        'SPGSPGPDGKTG',
        'QGPSGLPGPQG',
        'GPQGPPGPPGSPG',
        'TGPQGIAGQRGVV',
        'YGDLGNYPDAVG',
        'QGPAGPQGFQG',
        'LPGEKGDPGLPG',
        'GPVGPQGPSGPPG',
        'PPGPPGPSGPQG',
        'SQGSPGQPGPQG',
        'GFSGLDGAPGPKG',
        'GPQGQPGPPGPPG',
        'VGAPGPQGFQGPQG',
        'TGPPGPVGPAG',
        'YPGPPGPPGAPG',
        'QPGPSGLPGPQG',
        'GEPGSPGENGAPG'
    ]
    
    import random
    import string
    
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    
    toxic_sequences = []
    for pattern in toxic_patterns:
        toxic_sequences.append(pattern)
        # Create 170 variations per pattern to reach ~5000 total
        for _ in range(170):
            # Random mutations
            mutated = list(pattern)
            if len(mutated) > 5:
                # Multiple mutations for more diversity
                num_mutations = random.randint(1, 3)
                for _ in range(num_mutations):
                    pos = random.randint(0, len(mutated)-1)
                    mutated[pos] = random.choice('KRWFIL')  # Charged/aromatic/hydrophobic
            toxic_sequences.append(''.join(mutated))
            
            # Length variations
            if len(pattern) > 10:
                start = random.randint(0, min(5, len(pattern)//4))
                end = random.randint(max(10, len(pattern)-5), len(pattern))
                if end - start >= 8:
                    toxic_sequences.append(pattern[start:end])
            
            # Add random flanking regions
            if random.random() > 0.7:
                prefix = ''.join(random.choices('KRW', k=random.randint(2, 5)))
                toxic_sequences.append(prefix + pattern[:min(20, len(pattern))])
    
    nontoxic_sequences = []
    for pattern in nontoxic_patterns:
        nontoxic_sequences.append(pattern)
        # Create 170 variations per pattern
        for _ in range(170):
            mutated = list(pattern)
            if len(mutated) > 5:
                num_mutations = random.randint(1, 3)
                for _ in range(num_mutations):
                    pos = random.randint(0, len(mutated)-1)
                    mutated[pos] = random.choice('GPQNAS')  # Neutral/polar residues
            nontoxic_sequences.append(''.join(mutated))
            
            if len(pattern) > 10:
                start = random.randint(0, min(5, len(pattern)//4))
                end = random.randint(max(10, len(pattern)-5), len(pattern))
                if end - start >= 8:
                    nontoxic_sequences.append(pattern[start:end])
            
            if random.random() > 0.7:
                prefix = ''.join(random.choices('GPS', k=random.randint(2, 5)))
                nontoxic_sequences.append(prefix + pattern[:min(20, len(pattern))])
    
    # Remove duplicates and filter valid sequences
    toxic_sequences = list(set([seq for seq in toxic_sequences if 8 <= len(seq) <= 60]))
    nontoxic_sequences = list(set([seq for seq in nontoxic_sequences if 8 <= len(seq) <= 60]))
    
    toxic_sequences = toxic_sequences[:5000]
    nontoxic_sequences = nontoxic_sequences[:5000]
    
    # Save to FASTA
    with open(f'{output_dir}/synthetic_toxic.fasta', 'w') as f:
        for i, seq in enumerate(toxic_sequences):
            f.write(f'>synthetic_toxic_{i+1}|hemolytic|synthetic\n{seq}\n')
    
    with open(f'{output_dir}/synthetic_nontoxic.fasta', 'w') as f:
        for i, seq in enumerate(nontoxic_sequences):
            f.write(f'>synthetic_nontoxic_{i+1}|antimicrobial|synthetic\n{seq}\n')
    
    print(f"✓ Generated {len(toxic_sequences)} synthetic toxic peptides")
    print(f"✓ Generated {len(nontoxic_sequences)} synthetic non-toxic peptides")
    
    return True


def download_all_databases():
    """
    Main function to download data from all sources.
    """
    print("=" * 80)
    print("PEPTIDE DATABASE DOWNLOADER")
    print("=" * 80)
    
    create_directories()
    
    results = {
        'uniprot_toxic': False,
        'uniprot_nontoxic': False,
        'dbaasp': False,
        'apd3': False,
        'dramp': False,
        'synthetic': False
    }
    
    # Download from automated sources
    results['uniprot_toxic'] = download_uniprot_toxic_peptides()
    time.sleep(2)  # Be nice to APIs
    
    results['uniprot_nontoxic'] = download_uniprot_antimicrobial_peptides()
    time.sleep(2)
    
    # Check for manual downloads
    results['dbaasp'] = download_dbaasp_data()
    results['apd3'] = download_apd3_data()
    results['dramp'] = download_dramp_data()
    
    # Generate synthetic data as fallback
    results['synthetic'] = create_synthetic_data()
    
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    for source, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {source}")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("1. Complete any manual downloads from instructions above")
    print("2. Run: python scripts/clean_and_merge_data.py")
    print("=" * 80)
    
    return results


if __name__ == '__main__':
    download_all_databases()
