"""
Clean and merge peptide data from multiple sources.

This script:
1. Loads data from all downloaded sources
2. Cleans sequences (removes invalid amino acids, filters by length)
3. Labels sequences appropriately (toxic=1, non-toxic=0)
4. Removes exact duplicates
5. Balances the dataset
6. Saves to FASTA format for training
"""

import os
import re
from Bio import SeqIO, Seq, SeqRecord
from collections import defaultdict
import pandas as pd
import random


class PeptideCleaner:
    """Clean and standardize peptide sequences."""
    
    # Standard 20 amino acids
    VALID_AAS = set('ACDEFGHIKLMNPQRSTVWY')
    
    def __init__(self, min_length=5, max_length=100):
        self.min_length = min_length
        self.max_length = max_length
        self.stats = {
            'total_loaded': 0,
            'invalid_aa': 0,
            'too_short': 0,
            'too_long': 0,
            'duplicates': 0,
            'valid': 0
        }
    
    def clean_sequence(self, sequence):
        """
        Clean a single peptide sequence.
        
        Returns: (cleaned_sequence, is_valid)
        """
        # Convert to uppercase
        sequence = str(sequence).upper()
        
        # Remove whitespace
        sequence = sequence.strip()
        
        # Check for invalid amino acids
        if not all(aa in self.VALID_AAS for aa in sequence):
            self.stats['invalid_aa'] += 1
            return None, False
        
        # Check length
        if len(sequence) < self.min_length:
            self.stats['too_short'] += 1
            return None, False
        
        if len(sequence) > self.max_length:
            self.stats['too_long'] += 1
            return None, False
        
        self.stats['valid'] += 1
        return sequence, True
    
    def print_stats(self):
        """Print cleaning statistics."""
        print("\n=== Cleaning Statistics ===")
        print(f"Total loaded: {self.stats['total_loaded']}")
        print(f"Invalid amino acids: {self.stats['invalid_aa']}")
        print(f"Too short (<{self.min_length}): {self.stats['too_short']}")
        print(f"Too long (>{self.max_length}): {self.stats['too_long']}")
        print(f"Duplicates removed: {self.stats['duplicates']}")
        print(f"Valid sequences: {self.stats['valid']}")


class DatasetMerger:
    """Merge peptide datasets from multiple sources."""
    
    def __init__(self):
        self.toxic_sequences = {}  # sequence -> source
        self.nontoxic_sequences = {}  # sequence -> source
        self.cleaner = PeptideCleaner(min_length=5, max_length=100)
    
    def load_fasta(self, filepath, label, source_name):
        """
        Load peptides from FASTA file.
        
        Args:
            filepath: Path to FASTA file
            label: 1 for toxic, 0 for non-toxic
            source_name: Name of data source
        """
        if not os.path.exists(filepath):
            print(f"⚠ File not found: {filepath}")
            return 0
        
        count = 0
        print(f"\nLoading {filepath}...")
        
        for record in SeqIO.parse(filepath, "fasta"):
            self.cleaner.stats['total_loaded'] += 1
            sequence = str(record.seq).upper()
            
            # Clean sequence
            cleaned_seq, is_valid = self.cleaner.clean_sequence(sequence)
            
            if is_valid:
                # Add to appropriate dictionary
                if label == 1:
                    if cleaned_seq not in self.toxic_sequences:
                        self.toxic_sequences[cleaned_seq] = source_name
                        count += 1
                    else:
                        self.cleaner.stats['duplicates'] += 1
                else:
                    if cleaned_seq not in self.nontoxic_sequences:
                        self.nontoxic_sequences[cleaned_seq] = source_name
                        count += 1
                    else:
                        self.cleaner.stats['duplicates'] += 1
        
        print(f"✓ Loaded {count} unique sequences from {source_name}")
        return count
    
    def load_dbaasp_csv(self, filepath):
        """
        Load DBAASP data from CSV with HC50 values.
        
        HC50 < 100 μg/mL = toxic
        HC50 > 100 μg/mL = non-toxic
        """
        if not os.path.exists(filepath):
            print(f"⚠ DBAASP file not found: {filepath}")
            return 0, 0
        
        print(f"\nLoading {filepath}...")
        
        try:
            df = pd.read_csv(filepath)
            toxic_count = 0
            nontoxic_count = 0
            
            for _, row in df.iterrows():
                self.cleaner.stats['total_loaded'] += 1
                
                # Extract sequence and HC50
                sequence = str(row.get('Sequence', '')).upper()
                hc50 = row.get('HC50', None)
                
                # Clean sequence
                cleaned_seq, is_valid = self.cleaner.clean_sequence(sequence)
                
                if is_valid and hc50 is not None:
                    try:
                        hc50_value = float(hc50)
                        
                        # Label based on HC50 threshold
                        if hc50_value < 100:
                            # Toxic (hemolytic)
                            if cleaned_seq not in self.toxic_sequences:
                                self.toxic_sequences[cleaned_seq] = 'DBAASP'
                                toxic_count += 1
                        else:
                            # Non-toxic
                            if cleaned_seq not in self.nontoxic_sequences:
                                self.nontoxic_sequences[cleaned_seq] = 'DBAASP'
                                nontoxic_count += 1
                    except ValueError:
                        continue
            
            print(f"✓ DBAASP: {toxic_count} toxic, {nontoxic_count} non-toxic")
            return toxic_count, nontoxic_count
            
        except Exception as e:
            print(f"✗ Error loading DBAASP: {e}")
            return 0, 0
    
    def load_apd3_data(self, fasta_path, activity_path):
        """
        Load APD3 data with activity annotations.
        """
        if not os.path.exists(fasta_path) or not os.path.exists(activity_path):
            print(f"⚠ APD3 files not found")
            return 0, 0
        
        print(f"\nLoading APD3 data...")
        
        try:
            # Load activity data
            activity_df = pd.read_csv(activity_path)
            hemolytic_ids = set()
            
            for _, row in activity_df.iterrows():
                if 'hemolytic' in str(row).lower() or 'cytotoxic' in str(row).lower():
                    hemolytic_ids.add(row.get('ID', ''))
            
            # Load sequences
            toxic_count = 0
            nontoxic_count = 0
            
            for record in SeqIO.parse(fasta_path, "fasta"):
                self.cleaner.stats['total_loaded'] += 1
                sequence = str(record.seq).upper()
                peptide_id = record.id
                
                cleaned_seq, is_valid = self.cleaner.clean_sequence(sequence)
                
                if is_valid:
                    if peptide_id in hemolytic_ids:
                        if cleaned_seq not in self.toxic_sequences:
                            self.toxic_sequences[cleaned_seq] = 'APD3'
                            toxic_count += 1
                    else:
                        if cleaned_seq not in self.nontoxic_sequences:
                            self.nontoxic_sequences[cleaned_seq] = 'APD3'
                            nontoxic_count += 1
            
            print(f"✓ APD3: {toxic_count} toxic, {nontoxic_count} non-toxic")
            return toxic_count, nontoxic_count
            
        except Exception as e:
            print(f"✗ Error loading APD3: {e}")
            return 0, 0
    
    def load_all_sources(self):
        """Load data from all available sources."""
        print("=" * 80)
        print("LOADING DATA FROM ALL SOURCES")
        print("=" * 80)
        
        download_dir = 'data/raw/downloads'
        
        # Load UniProt data
        self.load_fasta(
            f'{download_dir}/uniprot/uniprot_toxic_peptides.fasta',
            label=1,
            source_name='UniProt_Toxic'
        )
        
        self.load_fasta(
            f'{download_dir}/uniprot/uniprot_amp_nontoxic.fasta',
            label=0,
            source_name='UniProt_AMP'
        )
        
        # Load synthetic data
        self.load_fasta(
            f'{download_dir}/synthetic_toxic.fasta',
            label=1,
            source_name='Synthetic'
        )
        
        self.load_fasta(
            f'{download_dir}/synthetic_nontoxic.fasta',
            label=0,
            source_name='Synthetic'
        )
        
        # Load DBAASP (if available)
        self.load_dbaasp_csv(f'{download_dir}/dbaasp/hemolytic_peptides.csv')
        
        # Load APD3 (if available)
        self.load_apd3_data(
            f'{download_dir}/apd3/APD_sequences.fasta',
            f'{download_dir}/apd3/APD_activity.csv'
        )
        
        # Load DRAMP (if available)
        self.load_fasta(
            f'{download_dir}/dramp/hemolytic_peptides.fasta',
            label=1,
            source_name='DRAMP'
        )
        
        self.load_fasta(
            f'{download_dir}/dramp/general_amps.fasta',
            label=0,
            source_name='DRAMP'
        )
        
        # Load existing data from project
        self.load_fasta(
            'data/raw/toxic_peptides.fasta',
            label=1,
            source_name='Original'
        )
        
        self.load_fasta(
            'data/raw/nontoxic_peptides.fasta',
            label=0,
            source_name='Original'
        )
    
    def balance_dataset(self, target_size=10000):
        """
        Balance the dataset to have equal toxic/non-toxic samples.
        
        Args:
            target_size: Total target dataset size (will be split 50/50)
        """
        print(f"\n=== Balancing Dataset (Target: {target_size} total) ===")
        
        toxic_list = list(self.toxic_sequences.items())
        nontoxic_list = list(self.nontoxic_sequences.items())
        
        print(f"Before balancing: {len(toxic_list)} toxic, {len(nontoxic_list)} non-toxic")
        
        # Target size per class
        per_class = target_size // 2
        
        # Sample or use all available
        if len(toxic_list) > per_class:
            random.shuffle(toxic_list)
            toxic_list = toxic_list[:per_class]
        
        if len(nontoxic_list) > per_class:
            random.shuffle(nontoxic_list)
            nontoxic_list = nontoxic_list[:per_class]
        
        # Update dictionaries
        self.toxic_sequences = dict(toxic_list)
        self.nontoxic_sequences = dict(nontoxic_list)
        
        print(f"After balancing: {len(self.toxic_sequences)} toxic, {len(self.nontoxic_sequences)} non-toxic")
        
        total = len(self.toxic_sequences) + len(self.nontoxic_sequences)
        if total < target_size:
            print(f"\n⚠ Warning: Only {total} peptides available (target was {target_size})")
            print("Consider downloading more data from DBAASP, APD3, or DRAMP for larger dataset")
    
    def save_to_fasta(self, output_dir='data/raw'):
        """Save cleaned and merged data to FASTA files."""
        print(f"\n=== Saving to {output_dir} ===")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save toxic peptides
        toxic_file = f'{output_dir}/toxic_peptides.fasta'
        with open(toxic_file, 'w') as f:
            for i, (seq, source) in enumerate(self.toxic_sequences.items(), 1):
                f.write(f'>toxic_peptide_{i}|hemolytic|{source}\n{seq}\n')
        
        print(f"✓ Saved {len(self.toxic_sequences)} toxic peptides to {toxic_file}")
        
        # Save non-toxic peptides
        nontoxic_file = f'{output_dir}/nontoxic_peptides.fasta'
        with open(nontoxic_file, 'w') as f:
            for i, (seq, source) in enumerate(self.nontoxic_sequences.items(), 1):
                f.write(f'>nontoxic_peptide_{i}|antimicrobial|{source}\n{seq}\n')
        
        print(f"✓ Saved {len(self.nontoxic_sequences)} non-toxic peptides to {nontoxic_file}")
        
        # Save metadata
        metadata = {
            'toxic_count': len(self.toxic_sequences),
            'nontoxic_count': len(self.nontoxic_sequences),
            'total_count': len(self.toxic_sequences) + len(self.nontoxic_sequences),
            'sources': self._get_source_distribution()
        }
        
        metadata_file = f'{output_dir}/dataset_info.txt'
        with open(metadata_file, 'w') as f:
            f.write("PEPTIDE DATASET INFORMATION\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total Peptides: {metadata['total_count']}\n")
            f.write(f"Toxic: {metadata['toxic_count']} ({metadata['toxic_count']/metadata['total_count']*100:.1f}%)\n")
            f.write(f"Non-toxic: {metadata['nontoxic_count']} ({metadata['nontoxic_count']/metadata['total_count']*100:.1f}%)\n\n")
            f.write("Source Distribution:\n")
            for source, count in metadata['sources'].items():
                f.write(f"  {source}: {count}\n")
        
        print(f"✓ Saved metadata to {metadata_file}")
    
    def _get_source_distribution(self):
        """Get distribution of sequences by source."""
        source_counts = defaultdict(int)
        for source in self.toxic_sequences.values():
            source_counts[source] += 1
        for source in self.nontoxic_sequences.values():
            source_counts[source] += 1
        return dict(source_counts)
    
    def print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 80)
        print("DATASET SUMMARY")
        print("=" * 80)
        print(f"Total peptides: {len(self.toxic_sequences) + len(self.nontoxic_sequences)}")
        print(f"Toxic peptides: {len(self.toxic_sequences)}")
        print(f"Non-toxic peptides: {len(self.nontoxic_sequences)}")
        print(f"\nSource distribution:")
        for source, count in self._get_source_distribution().items():
            print(f"  {source}: {count}")
        
        self.cleaner.print_stats()


def main():
    """Main execution function."""
    print("=" * 80)
    print("PEPTIDE DATA CLEANING AND MERGING")
    print("=" * 80)
    
    # Initialize merger
    merger = DatasetMerger()
    
    # Load all data sources
    merger.load_all_sources()
    
    # Balance dataset (target 10000 total = 5000 per class)
    merger.balance_dataset(target_size=10000)
    
    # Save to FASTA
    merger.save_to_fasta(output_dir='data/raw')
    
    # Print summary
    merger.print_summary()
    
    print("\n" + "=" * 80)
    print("✓ DATA PREPARATION COMPLETE!")
    print("\nNext step: Run training")
    print("  python scripts/train_pipeline.py")
    print("=" * 80)


if __name__ == '__main__':
    main()
