"""
Remove sequence redundancy using CD-HIT-like algorithm.

This ensures train/test sets don't contain highly similar sequences,
preventing overfitting and inflated performance metrics.
"""

import numpy as np
from Bio import SeqIO, pairwise2
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
from collections import defaultdict


def calculate_sequence_identity(seq1, seq2):
    """
    Calculate sequence identity between two peptides.
    
    Returns: Identity percentage (0-100)
    """
    # Use global alignment
    alignments = pairwise2.align.globalxx(seq1, seq2)
    
    if not alignments:
        return 0.0
    
    best_alignment = alignments[0]
    aligned_seq1, aligned_seq2 = best_alignment[0], best_alignment[1]
    
    # Calculate identity
    matches = sum(1 for a, b in zip(aligned_seq1, aligned_seq2) if a == b)
    identity = (matches / max(len(seq1), len(seq2))) * 100
    
    return identity


def cluster_sequences(sequences, identity_threshold=90):
    """
    Cluster sequences by similarity using greedy algorithm.
    
    Args:
        sequences: List of (sequence, label, source) tuples
        identity_threshold: Similarity threshold (default 90%)
    
    Returns:
        List of representative sequences (cluster centers)
    """
    print(f"\nClustering {len(sequences)} sequences at {identity_threshold}% identity...")
    
    # Sort by length (longest first) for better representatives
    sequences = sorted(sequences, key=lambda x: len(x[0]), reverse=True)
    
    clusters = []
    representatives = []
    
    for seq, label, source in sequences:
        # Check if this sequence is similar to any representative
        is_redundant = False
        
        for rep_seq, rep_label, rep_source in representatives:
            identity = calculate_sequence_identity(seq, rep_seq)
            
            if identity >= identity_threshold:
                is_redundant = True
                break
        
        # If not redundant, add as new representative
        if not is_redundant:
            representatives.append((seq, label, source))
    
    print(f"✓ Reduced to {len(representatives)} non-redundant sequences")
    print(f"  Removed {len(sequences) - len(representatives)} redundant sequences ({(1 - len(representatives)/len(sequences))*100:.1f}%)")
    
    return representatives


def remove_redundancy_from_files(input_dir='data/raw', output_dir='data/processed', identity_threshold=90):
    """
    Remove redundant sequences from FASTA files.
    
    Args:
        input_dir: Directory containing input FASTA files
        output_dir: Directory for output non-redundant files
        identity_threshold: Similarity threshold for redundancy removal
    """
    print("=" * 80)
    print("SEQUENCE REDUNDANCY REMOVAL")
    print("=" * 80)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load toxic sequences
    toxic_file = f'{input_dir}/toxic_peptides.fasta'
    toxic_sequences = []
    
    if os.path.exists(toxic_file):
        print(f"\nLoading toxic peptides from {toxic_file}...")
        for record in SeqIO.parse(toxic_file, 'fasta'):
            seq = str(record.seq).upper()
            source = record.description.split('|')[-1] if '|' in record.description else 'unknown'
            toxic_sequences.append((seq, 1, source))
        print(f"✓ Loaded {len(toxic_sequences)} toxic sequences")
    
    # Load non-toxic sequences
    nontoxic_file = f'{input_dir}/nontoxic_peptides.fasta'
    nontoxic_sequences = []
    
    if os.path.exists(nontoxic_file):
        print(f"\nLoading non-toxic peptides from {nontoxic_file}...")
        for record in SeqIO.parse(nontoxic_file, 'fasta'):
            seq = str(record.seq).upper()
            source = record.description.split('|')[-1] if '|' in record.description else 'unknown'
            nontoxic_sequences.append((seq, 0, source))
        print(f"✓ Loaded {len(nontoxic_sequences)} non-toxic sequences")
    
    # Cluster each class separately
    print(f"\n{'='*80}")
    print("CLUSTERING TOXIC PEPTIDES")
    print(f"{'='*80}")
    toxic_nr = cluster_sequences(toxic_sequences, identity_threshold)
    
    print(f"\n{'='*80}")
    print("CLUSTERING NON-TOXIC PEPTIDES")
    print(f"{'='*80}")
    nontoxic_nr = cluster_sequences(nontoxic_sequences, identity_threshold)
    
    # Save non-redundant sequences
    print(f"\n{'='*80}")
    print("SAVING NON-REDUNDANT SEQUENCES")
    print(f"{'='*80}")
    
    # Save toxic
    toxic_output = f'{output_dir}/toxic_peptides_nr{identity_threshold}.fasta'
    with open(toxic_output, 'w') as f:
        for i, (seq, label, source) in enumerate(toxic_nr, 1):
            f.write(f'>toxic_nr_{i}|hemolytic|{source}\n{seq}\n')
    print(f"✓ Saved {len(toxic_nr)} non-redundant toxic peptides to {toxic_output}")
    
    # Save non-toxic
    nontoxic_output = f'{output_dir}/nontoxic_peptides_nr{identity_threshold}.fasta'
    with open(nontoxic_output, 'w') as f:
        for i, (seq, label, source) in enumerate(nontoxic_nr, 1):
            f.write(f'>nontoxic_nr_{i}|antimicrobial|{source}\n{seq}\n')
    print(f"✓ Saved {len(nontoxic_nr)} non-redundant non-toxic peptides to {nontoxic_output}")
    
    # Print summary
    print(f"\n{'='*80}")
    print("REDUNDANCY REMOVAL COMPLETE")
    print(f"{'='*80}")
    print(f"Original: {len(toxic_sequences)} toxic, {len(nontoxic_sequences)} non-toxic")
    print(f"Non-redundant: {len(toxic_nr)} toxic, {len(nontoxic_nr)} non-toxic")
    print(f"Reduction: {len(toxic_sequences) + len(nontoxic_sequences) - len(toxic_nr) - len(nontoxic_nr)} sequences removed")
    print(f"\nNote: Use these non-redundant files for training to prevent overfitting!")


def main():
    """Main execution."""
    # Remove redundancy at 90% identity threshold
    remove_redundancy_from_files(
        input_dir='data/raw',
        output_dir='data/processed',
        identity_threshold=90
    )
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("1. Update src/data_loader.py to use non-redundant files")
    print("2. Run training: python scripts/train_pipeline.py")
    print("=" * 80)


if __name__ == '__main__':
    main()
