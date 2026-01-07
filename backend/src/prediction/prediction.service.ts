import { Injectable, BadRequestException } from "@nestjs/common"
import { PythonBridgeService } from "./python-bridge.service"
import { DatabaseService } from "../database/database.service"
import type { PredictSequenceDto, BatchPredictDto } from "./dto/predict.dto"

@Injectable()
export class PredictionService {
  private predictions: Map<string, any> = new Map()

  constructor(
    private readonly pythonBridge: PythonBridgeService,
    private readonly database: DatabaseService,
  ) {}

  async predictSingle(dto: PredictSequenceDto) {
    const { sequence, model } = dto
    const cleaned = this.sanitizeSequence(sequence)

    if (!this.isValidPeptideSequence(cleaned)) {
      throw new BadRequestException("Invalid peptide sequence. Only standard amino acids are allowed.")
    }

    const result = await this.pythonBridge.predict([cleaned], model)

    const predictionId = this.generateId()
    const prediction = {
      id: predictionId,
      sequence: cleaned,
      model: model || "ensemble",
      result: result[0],
      timestamp: new Date().toISOString(),
    }

    await this.database.addPrediction({
      sequence: cleaned,
      model: model || "ensemble",
      prediction: result[0].prediction,
      confidence: result[0].confidence,
      toxicProbability: result[0].probability.toxic,
      nonToxicProbability: result[0].probability.non_toxic,
    })

    return {
      success: true,
      data: prediction,
    }
  }

  async predictBatch(dto: BatchPredictDto) {
    const { sequences, model } = dto
    const cleanedSequences = sequences.map((s) => this.sanitizeSequence(s))

    const invalidSequences = cleanedSequences
      .map((seq, idx) => ({ seq, idx }))
      .filter(({ seq }) => !this.isValidPeptideSequence(seq))
    if (invalidSequences.length > 0) {
      const bad = invalidSequences.map(({ seq, idx }) => sequences[idx] || seq)
      throw new BadRequestException(`Invalid sequences found: ${bad.join(", ")}`)
    }

    const results = await this.pythonBridge.predict(cleanedSequences, model) as Array<{
      prediction: string
      confidence: number
      probability: { toxic: number; non_toxic: number }
    }>

    const batchId = this.generateId()
    const predictions = cleanedSequences.map((seq, idx) => ({
      sequence: seq,
      result: results[idx],
    }))

    await Promise.all(
      predictions.map((p) =>
        this.database.addPrediction({
          sequence: p.sequence,
          model: model || "ensemble",
          prediction: p.result.prediction,
          confidence: p.result.confidence,
          toxicProbability: p.result.probability.toxic,
          nonToxicProbability: p.result.probability.non_toxic,
        }),
      ),
    )

    const batchPrediction = {
      id: batchId,
      model: model || "ensemble",
      predictions,
      total: sequences.length,
      toxic: results.filter((r) => r.prediction === "Toxic").length,
      nonToxic: results.filter((r) => r.prediction === "Non-Toxic").length,
      timestamp: new Date().toISOString(),
    }

    this.predictions.set(batchId, batchPrediction)

    return {
      success: true,
      data: batchPrediction,
    }
  }

  async getPredictionById(id: string) {
    const prediction = this.predictions.get(id)
    if (!prediction) {
      throw new BadRequestException("Prediction not found")
    }
    return {
      success: true,
      data: prediction,
    }
  }

  getAvailableModels() {
    return {
      success: true,
      data: {
        models: [
          {
            id: "logistic_regression",
            name: "Logistic Regression",
            description: "Fast linear classifier, good for interpretability",
            type: "linear",
          },
          {
            id: "random_forest",
            name: "Random Forest",
            description: "Ensemble of decision trees, handles non-linear patterns",
            type: "ensemble",
          },
          {
            id: "svm",
            name: "Support Vector Machine",
            description: "Powerful classifier with kernel trick",
            type: "kernel",
          },
          {
            id: "ensemble",
            name: "Ensemble (Recommended)",
            description: "Combines all models for best accuracy",
            type: "ensemble",
            recommended: true,
          },
        ],
      },
    }
  }

  private isValidPeptideSequence(sequence: string): boolean {
    if (!sequence) return false
    return /^[ACDEFGHIKLMNPQRSTVWY]+$/.test(sequence)
  }

  private generateId(): string {
    return `pred_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  private sanitizeSequence(sequence: string): string {
    return (sequence || "").trim().toUpperCase().replace(/\s+/g, "")
  }
}
