"""
Feature extraction module for peptide sequences.

Converts amino acid sequences into numerical feature vectors suitable for machine learning.
Includes amino acid composition, physicochemical properties, and optional k-mer features.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import warnings

warnings.filterwarnings('ignore')


class PeptideFeatureExtractor:
    """
    Comprehensive feature extractor for peptide sequences.
    
    Implements multiple feature representation methods including:
    - Amino acid composition (AAC)
    - Physicochemical properties
    - Dipeptide composition (optional)
    """
    
    # Standard amino acids
    AMINO_ACIDS = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                   'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    
    def __init__(self, use_dipeptide: bool = False):
        """
        Initialize feature extractor.
        
        Args:
            use_dipeptide: Whether to include dipeptide composition features (400 dims)
        """
        self.use_dipeptide = use_dipeptide
        self.feature_names = self._generate_feature_names()
        
    def _generate_feature_names(self) -> List[str]:
        """Generate descriptive names for all features."""
        names = []
        
        # Amino acid composition features
        names.extend([f'AAC_{aa}' for aa in self.AMINO_ACIDS])
        
        # Sequence length
        names.append('length')
        
        # Physicochemical properties
        names.extend([
            'molecular_weight',
            'net_charge_pH7',
            'isoelectric_point',
            'aromaticity',
            'instability_index',
            'gravy'  # Grand average of hydropathy
        ])
        
        # Dipeptide composition (optional)
        if self.use_dipeptide:
            dipeptides = [aa1 + aa2 for aa1 in self.AMINO_ACIDS 
                         for aa2 in self.AMINO_ACIDS]
            names.extend([f'DPC_{dp}' for dp in dipeptides])
        
        return names
    
    def extract_amino_acid_composition(self, sequence: str) -> np.ndarray:
        """
        Calculate amino acid composition (AAC).
        
        AAC represents the frequency of each amino acid normalized by sequence length.
        This is a fundamental feature for protein/peptide characterization.
        
        Args:
            sequence: Amino acid sequence string
            
        Returns:
            Array of 20 AAC values (one per amino acid)
        """
        sequence = sequence.upper()
        length = len(sequence)
        
        if length == 0:
            return np.zeros(20)
        
        aac = np.array([sequence.count(aa) / length for aa in self.AMINO_ACIDS])
        return aac
    
    def extract_physicochemical_properties(self, sequence: str) -> np.ndarray:
        """
        Extract physicochemical properties using BioPython.
        
        These properties are critical for understanding peptide behavior:
        - Molecular weight: Mass of the peptide
        - Net charge: Electrostatic properties at pH 7
        - Isoelectric point: pH at which peptide has no net charge
        - Aromaticity: Proportion of aromatic amino acids (F, W, Y)
        - Instability index: Estimate of protein stability
        - GRAVY: Hydrophobicity measure (positive = hydrophobic)
        
        Args:
            sequence: Amino acid sequence string
            
        Returns:
            Array of 6 physicochemical features
        """
        try:
            analyzed_seq = ProteinAnalysis(sequence.upper())
            
            # Molecular weight (Da)
            mw = analyzed_seq.molecular_weight()
            
            # Net charge at pH 7.0
            # Toxic peptides often have distinct charge distributions
            charge = analyzed_seq.charge_at_pH(7.0)
            
            # Isoelectric point
            # pH at which peptide has zero net charge
            pi = analyzed_seq.isoelectric_point()
            
            # Aromaticity
            # Fraction of aromatic amino acids (Phe, Trp, Tyr)
            aromaticity = analyzed_seq.aromaticity()
            
            # Instability index
            # > 40 suggests unstable protein
            instability = analyzed_seq.instability_index()
            
            # GRAVY (Grand Average of Hydropathy)
            # Hydrophobicity correlates with membrane interactions (toxicity mechanism)
            gravy = analyzed_seq.gravy()
            
            return np.array([mw, charge, pi, aromaticity, instability, gravy])
            
        except Exception as e:
            # Handle invalid sequences gracefully
            print(f"Warning: Could not analyze sequence '{sequence[:20]}...': {str(e)}")
            return np.zeros(6)
    
    def extract_dipeptide_composition(self, sequence: str) -> np.ndarray:
        """
        Calculate dipeptide composition (DPC).
        
        DPC captures local sequence order information by counting all possible
        2-mer combinations (400 dipeptides: 20 x 20).
        This provides more sequence context than simple AAC.
        
        Args:
            sequence: Amino acid sequence string
            
        Returns:
            Array of 400 dipeptide composition values
        """
        sequence = sequence.upper()
        length = len(sequence)
        
        if length < 2:
            return np.zeros(400)
        
        # Count all dipeptides
        dipeptide_counts = {}
        for aa1 in self.AMINO_ACIDS:
            for aa2 in self.AMINO_ACIDS:
                dipeptide_counts[aa1 + aa2] = 0
        
        # Count occurrences
        for i in range(length - 1):
            dipeptide = sequence[i:i+2]
            if dipeptide in dipeptide_counts:
                dipeptide_counts[dipeptide] += 1
        
        # Normalize by number of dipeptides in sequence
        total_dipeptides = max(1, length - 1)
        dpc = np.array([dipeptide_counts[aa1 + aa2] / total_dipeptides 
                       for aa1 in self.AMINO_ACIDS 
                       for aa2 in self.AMINO_ACIDS])
        
        return dpc
    
    def extract_features(self, sequence: str) -> np.ndarray:
        """
        Extract all features for a single peptide sequence.
        
        Args:
            sequence: Amino acid sequence string
            
        Returns:
            Feature vector combining all representations
        """
        features = []
        
        # 1. Amino acid composition (20 features)
        aac = self.extract_amino_acid_composition(sequence)
        features.append(aac)
        
        # 2. Sequence length (1 feature)
        # Length is important: toxic peptides often have characteristic sizes
        length = np.array([len(sequence)])
        features.append(length)
        
        # 3. Physicochemical properties (6 features)
        physchem = self.extract_physicochemical_properties(sequence)
        features.append(physchem)
        
        # 4. Dipeptide composition (400 features, optional)
        if self.use_dipeptide:
            dpc = self.extract_dipeptide_composition(sequence)
            features.append(dpc)
        
        # Concatenate all features
        feature_vector = np.concatenate(features)
        return feature_vector
    
    def extract_batch(self, sequences: List[str], 
                     labels: Optional[List[int]] = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Extract features for a batch of sequences.
        
        Args:
            sequences: List of amino acid sequences
            labels: Optional list of binary labels (0=non-toxic, 1=toxic)
            
        Returns:
            Tuple of (X, y) where:
                X: Feature matrix of shape (n_samples, n_features)
                y: Label array of shape (n_samples,) or None
        """
        print(f"Extracting features for {len(sequences)} sequences...")
        print(f"Feature dimensionality: {len(self.feature_names)}")
        
        X = np.array([self.extract_features(seq) for seq in sequences])
        y = np.array(labels) if labels is not None else None
        
        print(f"Feature extraction complete. Shape: {X.shape}")
        return X, y
    
    def get_feature_names(self) -> List[str]:
        """Return list of feature names for interpretation."""
        return self.feature_names
