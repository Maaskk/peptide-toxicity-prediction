"""
Simple database module for storing prediction history
Uses SQLite for simplicity, can be upgraded to PostgreSQL
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class PredictionDatabase:
    """
    Database manager for prediction history
    """
    
    def __init__(self, db_path='data/predictions.db'):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sequence TEXT NOT NULL,
                model TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                toxic_probability REAL NOT NULL,
                non_toxic_probability REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Batch predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batch_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT UNIQUE NOT NULL,
                model TEXT NOT NULL,
                total_sequences INTEGER NOT NULL,
                toxic_count INTEGER NOT NULL,
                non_toxic_count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Feature analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feature_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sequence TEXT NOT NULL,
                length INTEGER NOT NULL,
                hydrophobicity REAL,
                net_charge REAL,
                aromatic_content REAL,
                aac_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_prediction(self, sequence: str, model: str, prediction: str,
                      confidence: float, toxic_prob: float, non_toxic_prob: float,
                      metadata: Optional[Dict] = None) -> int:
        """
        Add a single prediction to database
        
        Args:
            sequence: Peptide sequence
            model: Model used
            prediction: 'Toxic' or 'Non-Toxic'
            confidence: Confidence score
            toxic_prob: Probability of being toxic
            non_toxic_prob: Probability of being non-toxic
            metadata: Additional metadata
        
        Returns:
            Prediction ID
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions 
            (sequence, model, prediction, confidence, toxic_probability, non_toxic_probability, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            sequence,
            model,
            prediction,
            confidence,
            toxic_prob,
            non_toxic_prob,
            json.dumps(metadata) if metadata else None
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def add_batch_prediction(self, batch_id: str, model: str, total: int,
                           toxic_count: int, non_toxic_count: int,
                           metadata: Optional[Dict] = None) -> int:
        """
        Add a batch prediction record
        
        Args:
            batch_id: Unique batch identifier
            model: Model used
            total: Total number of sequences
            toxic_count: Number of toxic predictions
            non_toxic_count: Number of non-toxic predictions
            metadata: Additional metadata
        
        Returns:
            Batch record ID
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO batch_predictions
            (batch_id, model, total_sequences, toxic_count, non_toxic_count, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            batch_id,
            model,
            total,
            toxic_count,
            non_toxic_count,
            json.dumps(metadata) if metadata else None
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def add_feature_analysis(self, sequence: str, length: int, hydrophobicity: float,
                            net_charge: float, aromatic_content: float,
                            aac_data: Dict) -> int:
        """
        Add feature analysis record
        
        Args:
            sequence: Peptide sequence
            length: Sequence length
            hydrophobicity: Hydrophobicity score
            net_charge: Net charge
            aromatic_content: Aromatic content percentage
            aac_data: Amino acid composition data
        
        Returns:
            Analysis record ID
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO feature_analysis
            (sequence, length, hydrophobicity, net_charge, aromatic_content, aac_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            sequence,
            length,
            hydrophobicity,
            net_charge,
            aromatic_content,
            json.dumps(aac_data)
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_predictions(self, limit: int = 20) -> List[Dict]:
        """
        Get recent predictions
        
        Args:
            limit: Number of records to return
        
        Returns:
            List of prediction records
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT * FROM predictions
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_predictions_by_model(self, model: str, limit: int = 50) -> List[Dict]:
        """
        Get predictions filtered by model
        
        Args:
            model: Model name
            limit: Number of records
        
        Returns:
            List of predictions
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT * FROM predictions
            WHERE model = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (model, limit))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict:
        """
        Get overall statistics
        
        Returns:
            Statistics dictionary
        """
        cursor = self.conn.cursor()
        
        # Total predictions
        cursor.execute('SELECT COUNT(*) as count FROM predictions')
        total = cursor.fetchone()['count']
        
        # Toxic vs non-toxic
        cursor.execute('''
            SELECT prediction, COUNT(*) as count 
            FROM predictions 
            GROUP BY prediction
        ''')
        pred_counts = {row['prediction']: row['count'] for row in cursor.fetchall()}
        
        # Model usage
        cursor.execute('''
            SELECT model, COUNT(*) as count 
            FROM predictions 
            GROUP BY model
        ''')
        model_usage = {row['model']: row['count'] for row in cursor.fetchall()}
        
        # Average confidence
        cursor.execute('SELECT AVG(confidence) as avg_conf FROM predictions')
        avg_confidence = cursor.fetchone()['avg_conf']
        
        return {
            'total_predictions': total,
            'toxic_predictions': pred_counts.get('Toxic', 0),
            'non_toxic_predictions': pred_counts.get('Non-Toxic', 0),
            'model_usage': model_usage,
            'average_confidence': avg_confidence
        }
    
    def search_predictions(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Search predictions by sequence
        
        Args:
            query: Search query
            limit: Number of results
        
        Returns:
            List of matching predictions
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT * FROM predictions
            WHERE sequence LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def export_to_csv(self, output_path: str, start_date: Optional[str] = None,
                     end_date: Optional[str] = None):
        """
        Export predictions to CSV
        
        Args:
            output_path: Path for CSV file
            start_date: Optional start date filter
            end_date: Optional end date filter
        """
        import pandas as pd
        
        query = 'SELECT * FROM predictions'
        params = []
        
        if start_date or end_date:
            query += ' WHERE '
            conditions = []
            if start_date:
                conditions.append('created_at >= ?')
                params.append(start_date)
            if end_date:
                conditions.append('created_at <= ?')
                params.append(end_date)
            query += ' AND '.join(conditions)
        
        query += ' ORDER BY created_at DESC'
        
        df = pd.read_sql_query(query, self.conn, params=params)
        df.to_csv(output_path, index=False)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
