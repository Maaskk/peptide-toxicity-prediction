"""
Utility functions for data handling, logging, and pipeline management.
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def set_random_seed(seed: int = 42):
    """
    Set random seeds for reproducibility.
    
    Args:
        seed: Random seed value
    """
    np.random.seed(seed)
    import random
    random.seed(seed)
    
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def save_results(results: Dict, filepath: str):
    """
    Save results dictionary to JSON file.
    
    Args:
        results: Dictionary of results
        filepath: Output file path
    """
    # Convert numpy types to Python types
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_numpy(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        return obj
    
    results_converted = convert_numpy(results)
    
    with open(filepath, 'w') as f:
        json.dump(results_converted, f, indent=2)
    
    print(f"✓ Results saved to {filepath}")


def load_results(filepath: str) -> Dict:
    """
    Load results from JSON file.
    
    Args:
        filepath: Input file path
        
    Returns:
        Results dictionary
    """
    with open(filepath, 'r') as f:
        results = json.load(f)
    return results


def create_experiment_dir(base_dir: str = "experiments") -> Path:
    """
    Create timestamped experiment directory.
    
    Args:
        base_dir: Base directory for experiments
        
    Returns:
        Path to experiment directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    exp_dir = Path(base_dir) / f"exp_{timestamp}"
    exp_dir.mkdir(parents=True, exist_ok=True)
    return exp_dir


class Logger:
    """Simple logger for pipeline execution."""
    
    def __init__(self, log_file: str = "pipeline.log"):
        """Initialize logger."""
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Clear previous log
        with open(self.log_file, 'w') as f:
            f.write(f"Pipeline Execution Log\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
    
    def log(self, message: str, level: str = "INFO"):
        """
        Log a message.
        
        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        # Print to console
        print(log_entry.strip())
        
        # Write to file
        with open(self.log_file, 'a') as f:
            f.write(log_entry)


def print_section_header(title: str):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")


def print_subsection(title: str):
    """Print formatted subsection header."""
    print(f"\n{'-'*70}")
    print(f"  {title}")
    print(f"{'-'*70}\n")
