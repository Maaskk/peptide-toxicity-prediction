import { Injectable } from "@nestjs/common"
import { DatabaseService } from "../database/database.service"

@Injectable()
export class HistoryService {
  constructor(private readonly database: DatabaseService) {}

  async getHistory(limit = 20) {
    const predictions = await this.database.getRecentPredictions(limit)

    return {
      success: true,
      data: {
        predictions: predictions.map((p) => ({
          id: p.id,
          sequence: p.sequence,
          model: p.model,
          result: {
            prediction: p.prediction,
            confidence: p.confidence,
            probability: {
              toxic: p.toxic_probability,
              non_toxic: p.non_toxic_probability,
            },
          },
          timestamp: p.created_at,
        })),
        total: predictions.length,
      },
    }
  }

  async getStatistics() {
    const stats = await this.database.getStatistics()

    return {
      success: true,
      data: {
        totalPredictions: stats.total,
        toxicPredictions: stats.toxic,
        nonToxicPredictions: stats.nonToxic,
        modelsUsed: stats.modelUsage,
      },
    }
  }

  async searchHistory(query: string, limit = 50) {
    const results = await this.database.searchPredictions(query, limit)

    return {
      success: true,
      data: {
        results: results.map((p) => ({
          id: p.id,
          sequence: p.sequence,
          model: p.model,
          prediction: p.prediction,
          confidence: p.confidence,
          timestamp: p.created_at,
        })),
        total: results.length,
      },
    }
  }
}
