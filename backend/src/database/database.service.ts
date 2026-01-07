import { Injectable } from "@nestjs/common"
import * as sqlite3 from "sqlite3"

@Injectable()
export class DatabaseService {
  private db: any

  constructor() {
    this.initializeDatabase()
  }

  private initializeDatabase() {
    const path = require("path")
    const fs = require("fs")
    const dbDir = path.join(process.cwd(), "data")
    if (!fs.existsSync(dbDir)) {
      fs.mkdirSync(dbDir, { recursive: true })
    }
    const dbPath = path.join(dbDir, "predictions.db")
    this.db = new sqlite3.Database(dbPath)

    this.db.run(`
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
    `)

    this.db.run(`
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
    `)
  }

  async addPrediction(data: {
    sequence: string
    model: string
    prediction: string
    confidence: number
    toxicProbability: number
    nonToxicProbability: number
  }): Promise<number> {
    return new Promise((resolve, reject) => {
      this.db.run(
        `INSERT INTO predictions (sequence, model, prediction, confidence, toxic_probability, non_toxic_probability)
         VALUES (?, ?, ?, ?, ?, ?)`,
        [data.sequence, data.model, data.prediction, data.confidence, data.toxicProbability, data.nonToxicProbability],
        function (err: Error) {
          if (err) reject(err)
          else resolve(this.lastID)
        },
      )
    })
  }

  async getRecentPredictions(limit = 20): Promise<any[]> {
    return new Promise((resolve, reject) => {
      this.db.all(`SELECT * FROM predictions ORDER BY id DESC LIMIT ?`, [limit], (err: Error, rows: any[]) => {
        if (err) reject(err)
        else resolve(rows)
      })
    })
  }

  async getStatistics(): Promise<any> {
    return new Promise((resolve, reject) => {
      const stats: any = {}

      // Total predictions
      this.db.get(`SELECT COUNT(*) as count FROM predictions`, (err: Error, row: any) => {
        if (err) return reject(err)
        stats.total = row.count

        // Toxic vs non-toxic
        this.db.all(
          `SELECT prediction, COUNT(*) as count FROM predictions GROUP BY prediction`,
          (err: Error, rows: any[]) => {
            if (err) return reject(err)

            stats.toxic = rows.find((r) => r.prediction === "Toxic")?.count || 0
            stats.nonToxic = rows.find((r) => r.prediction === "Non-Toxic")?.count || 0

            // Model usage
            this.db.all(
              `SELECT model, COUNT(*) as count FROM predictions GROUP BY model`,
              (err: Error, rows: any[]) => {
                if (err) return reject(err)

                stats.modelUsage = rows.reduce((acc: any, row: any) => {
                  acc[row.model] = row.count
                  return acc
                }, {})

                resolve(stats)
              },
            )
          },
        )
      })
    })
  }

  async searchPredictions(query: string, limit = 50): Promise<any[]> {
    return new Promise((resolve, reject) => {
      this.db.all(
        `SELECT * FROM predictions WHERE sequence LIKE ? ORDER BY created_at DESC LIMIT ?`,
        [`%${query}%`, limit],
        (err: Error, rows: any[]) => {
          if (err) reject(err)
          else resolve(rows)
        },
      )
    })
  }
}
