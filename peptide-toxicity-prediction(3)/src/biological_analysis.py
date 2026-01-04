"""
Biological interpretation module.

Analyzes feature patterns, amino acid distributions, and physicochemical 
properties to provide biological insights into toxicity mechanisms.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict
from pathlib import Path
from scipy import stats


class BiologicalAnalyzer:
    """
    Provides biological interpretation of toxicity prediction results.
    
    Analyzes amino acid composition, physicochemical properties, and
    sequence characteristics to identify molecular signatures of toxicity.
    """
    
    AMINO_ACIDS = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                   'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    
    # Amino acid properties for interpretation
    AA_PROPERTIES = {
        'hydrophobic': ['A', 'V', 'I', 'L', 'M', 'F', 'W', 'P'],
        'hydrophilic': ['S', 'T', 'N', 'Q'],
        'positive': ['K', 'R', 'H'],
        'negative': ['D', 'E'],
        'aromatic': ['F', 'W', 'Y'],
        'small': ['A', 'G', 'S', 'T']
    }
    
    def __init__(self, output_dir: str = "results"):
        """Initialize biological analyzer."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        sns.set_style("whitegrid")
    
    def analyze_amino_acid_distribution(self, sequences: List[str], 
                                       labels: np.ndarray):
        """
        Analyze amino acid composition differences between toxic and non-toxic peptides.
        
        Statistical comparison reveals which amino acids are enriched in toxic peptides.
        This can provide insights into toxicity mechanisms (e.g., membrane disruption
        via hydrophobic residues, charge-based interactions).
        
        Args:
            sequences: List of peptide sequences
            labels: Binary labels (0=non-toxic, 1=toxic)
        """
        print("\n" + "="*70)
        print("BIOLOGICAL ANALYSIS: Amino Acid Distribution")
        print("="*70 + "\n")
        
        # Separate toxic and non-toxic sequences
        toxic_seqs = [seq for seq, label in zip(sequences, labels) if label == 1]
        nontoxic_seqs = [seq for seq, label in zip(sequences, labels) if label == 0]
        
        print(f"Toxic peptides: {len(toxic_seqs)}")
        print(f"Non-toxic peptides: {len(nontoxic_seqs)}")
        
        # Calculate AA composition for each group
        toxic_comp = self._calculate_group_composition(toxic_seqs)
        nontoxic_comp = self._calculate_group_composition(nontoxic_seqs)
        
        # Statistical testing (t-test)
        print("\nAmino Acid Enrichment Analysis:")
        print(f"{'AA':<5} {'Toxic %':<12} {'Non-toxic %':<15} {'Difference':<12} {'p-value':<10} {'Significance'}")
        print("-" * 70)
        
        significant_aas = []
        for aa in self.AMINO_ACIDS:
            toxic_vals = [seq.count(aa) / len(seq) for seq in toxic_seqs if len(seq) > 0]
            nontoxic_vals = [seq.count(aa) / len(seq) for seq in nontoxic_seqs if len(seq) > 0]
            
            t_stat, p_value = stats.ttest_ind(toxic_vals, nontoxic_vals)
            diff = np.mean(toxic_vals) - np.mean(nontoxic_vals)
            
            sig = ""
            if p_value < 0.001:
                sig = "***"
                significant_aas.append((aa, diff, p_value))
            elif p_value < 0.01:
                sig = "**"
                significant_aas.append((aa, diff, p_value))
            elif p_value < 0.05:
                sig = "*"
                significant_aas.append((aa, diff, p_value))
            
            print(f"{aa:<5} {np.mean(toxic_vals)*100:>10.2f}% {np.mean(nontoxic_vals)*100:>13.2f}% "
                  f"{diff*100:>10.2f}% {p_value:>10.4f}   {sig}")
        
        print("\n* p < 0.05, ** p < 0.01, *** p < 0.001")
        
        # Interpret significant findings
        if significant_aas:
            print("\nBiological Interpretation:")
            print("-" * 70)
            self._interpret_significant_aas(significant_aas)
        
        # Plot comparison
        self._plot_aa_comparison(toxic_comp, nontoxic_comp)
    
    def analyze_physicochemical_properties(self, X: np.ndarray, y: np.ndarray,
                                          feature_names: List[str]):
        """
        Analyze physicochemical property distributions.
        
        Compares molecular weight, charge, hydrophobicity, etc. between
        toxic and non-toxic peptides.
        
        Args:
            X: Feature matrix
            y: Labels
            feature_names: List of feature names
        """
        print("\n" + "="*70)
        print("BIOLOGICAL ANALYSIS: Physicochemical Properties")
        print("="*70 + "\n")
        
        # Find physicochemical feature indices
        physchem_features = ['length', 'molecular_weight', 'net_charge_pH7', 
                            'isoelectric_point', 'aromaticity', 'instability_index', 'gravy']
        
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        axes = axes.flatten()
        
        for idx, feat_name in enumerate(physchem_features):
            if feat_name in feature_names:
                feat_idx = feature_names.index(feat_name)
                
                toxic_vals = X[y == 1, feat_idx]
                nontoxic_vals = X[y == 0, feat_idx]
                
                # Statistical test
                t_stat, p_value = stats.ttest_ind(toxic_vals, nontoxic_vals)
                
                # Plot distributions
                axes[idx].hist(nontoxic_vals, bins=30, alpha=0.6, label='Non-toxic', 
                             color='green', density=True)
                axes[idx].hist(toxic_vals, bins=30, alpha=0.6, label='Toxic', 
                             color='red', density=True)
                
                axes[idx].set_xlabel(feat_name.replace('_', ' ').title())
                axes[idx].set_ylabel('Density')
                axes[idx].legend()
                
                # Add statistics to title
                sig = ""
                if p_value < 0.001:
                    sig = "***"
                elif p_value < 0.01:
                    sig = "**"
                elif p_value < 0.05:
                    sig = "*"
                
                axes[idx].set_title(f'{feat_name.replace("_", " ").title()}\np={p_value:.4f} {sig}')
                
                # Print statistics
                print(f"{feat_name.replace('_', ' ').title()}:")
                print(f"  Toxic:     mean={np.mean(toxic_vals):.3f}, std={np.std(toxic_vals):.3f}")
                print(f"  Non-toxic: mean={np.mean(nontoxic_vals):.3f}, std={np.std(nontoxic_vals):.3f}")
                print(f"  p-value: {p_value:.6f} {sig}\n")
        
        # Hide unused subplots
        for idx in range(len(physchem_features), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        filepath = self.output_dir / "physicochemical_distributions.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Physicochemical property distributions saved to {filepath}")
        plt.close()
    
    def analyze_length_distribution(self, sequences: List[str], labels: np.ndarray):
        """
        Analyze sequence length distribution.
        
        Toxic peptides often have characteristic length ranges related to
        their mechanism of action (e.g., membrane-disrupting peptides are typically 10-40 AA).
        
        Args:
            sequences: List of peptide sequences
            labels: Binary labels
        """
        print("\n" + "="*70)
        print("BIOLOGICAL ANALYSIS: Sequence Length")
        print("="*70 + "\n")
        
        toxic_lengths = [len(seq) for seq, label in zip(sequences, labels) if label == 1]
        nontoxic_lengths = [len(seq) for seq, label in zip(sequences, labels) if label == 0]
        
        print(f"Toxic peptides:")
        print(f"  Mean length: {np.mean(toxic_lengths):.2f} ± {np.std(toxic_lengths):.2f} AA")
        print(f"  Range: {min(toxic_lengths)} - {max(toxic_lengths)} AA")
        
        print(f"\nNon-toxic peptides:")
        print(f"  Mean length: {np.mean(nontoxic_lengths):.2f} ± {np.std(nontoxic_lengths):.2f} AA")
        print(f"  Range: {min(nontoxic_lengths)} - {max(nontoxic_lengths)} AA")
        
        # Statistical test
        t_stat, p_value = stats.ttest_ind(toxic_lengths, nontoxic_lengths)
        print(f"\nStatistical difference: p = {p_value:.6f}")
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.hist(nontoxic_lengths, bins=30, alpha=0.6, label='Non-toxic', 
                color='green', density=True)
        plt.hist(toxic_lengths, bins=30, alpha=0.6, label='Toxic', 
                color='red', density=True)
        plt.xlabel('Sequence Length (amino acids)', fontweight='bold')
        plt.ylabel('Density', fontweight='bold')
        plt.title('Peptide Length Distribution', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filepath = self.output_dir / "length_distribution.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Length distribution saved to {filepath}")
        plt.close()
    
    def _calculate_group_composition(self, sequences: List[str]) -> Dict[str, float]:
        """Calculate average amino acid composition for a group of sequences."""
        composition = {aa: 0.0 for aa in self.AMINO_ACIDS}
        
        for seq in sequences:
            seq = seq.upper()
            length = len(seq)
            if length == 0:
                continue
            for aa in self.AMINO_ACIDS:
                composition[aa] += seq.count(aa) / length
        
        # Average across all sequences
        n_seqs = len(sequences)
        for aa in composition:
            composition[aa] /= n_seqs
        
        return composition
    
    def _plot_aa_comparison(self, toxic_comp: Dict, nontoxic_comp: Dict):
        """Plot amino acid composition comparison."""
        aas = list(toxic_comp.keys())
        toxic_vals = [toxic_comp[aa] * 100 for aa in aas]
        nontoxic_vals = [nontoxic_comp[aa] * 100 for aa in aas]
        
        x = np.arange(len(aas))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(x - width/2, nontoxic_vals, width, label='Non-toxic', color='green', alpha=0.7)
        ax.bar(x + width/2, toxic_vals, width, label='Toxic', color='red', alpha=0.7)
        
        ax.set_xlabel('Amino Acid', fontweight='bold')
        ax.set_ylabel('Composition (%)', fontweight='bold')
        ax.set_title('Amino Acid Composition: Toxic vs Non-toxic Peptides', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(aas)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        
        filepath = self.output_dir / "aa_composition_comparison.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Amino acid composition comparison saved to {filepath}")
        plt.close()
    
    def _interpret_significant_aas(self, significant_aas: List[Tuple]):
        """Provide biological interpretation of significant amino acids."""
        for aa, diff, p_val in sorted(significant_aas, key=lambda x: abs(x[1]), reverse=True):
            direction = "enriched in" if diff > 0 else "depleted in"
            
            # Determine properties
            properties = []
            for prop, aa_list in self.AA_PROPERTIES.items():
                if aa in aa_list:
                    properties.append(prop)
            
            prop_str = ", ".join(properties) if properties else "polar"
            
            print(f"  • {aa} ({prop_str}): {direction} toxic peptides")
            print(f"    Difference: {abs(diff)*100:.2f}%, p={p_val:.6f}")
            
            # Mechanistic interpretation
            if aa in ['K', 'R'] and diff > 0:
                print(f"    → Positive charge may facilitate membrane interaction")
            elif aa in ['D', 'E'] and diff > 0:
                print(f"    → Negative charge can disrupt ionic homeostasis")
            elif aa in ['F', 'W', 'Y'] and diff > 0:
                print(f"    → Aromatic residues enhance membrane insertion")
            elif aa in ['L', 'I', 'V'] and diff > 0:
                print(f"    → Hydrophobic residues promote membrane partitioning")
            print()
