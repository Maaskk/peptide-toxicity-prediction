import { Injectable } from "@nestjs/common"
import type { AnalyzeSequenceDto } from "./dto/analyze.dto"

@Injectable()
export class AnalysisService {
  async analyzeFeatures(dto: AnalyzeSequenceDto) {
    const { sequence } = dto

    const aac = this.calculateAAC(sequence)
    const properties = this.calculateProperties(sequence)

    return {
      success: true,
      data: {
        sequence,
        length: sequence.length,
        aminoAcidComposition: aac,
        physicochemicalProperties: properties,
      },
    }
  }

  async analyzePhysicochemicalProperties(dto: AnalyzeSequenceDto) {
    const { sequence } = dto
    const properties = this.calculateProperties(sequence)

    return {
      success: true,
      data: properties,
    }
  }

  private calculateAAC(sequence: string) {
    const aminoAcids = "ACDEFGHIKLMNPQRSTVWY".split("")
    const aac: Record<string, number> = {}

    aminoAcids.forEach((aa) => {
      const count = sequence.split(aa).length - 1
      aac[aa] = (count / sequence.length) * 100
    })

    return aac
  }

  private calculateProperties(sequence: string) {
    const hydrophobicityScale: Record<string, number> = {
      A: 1.8,
      C: 2.5,
      D: -3.5,
      E: -3.5,
      F: 2.8,
      G: -0.4,
      H: -3.2,
      I: 4.5,
      K: -3.9,
      L: 3.8,
      M: 1.9,
      N: -3.5,
      P: -1.6,
      Q: -3.5,
      R: -4.5,
      S: -0.8,
      T: -0.7,
      V: 4.2,
      W: -0.9,
      Y: -1.3,
    }

    const chargeScale: Record<string, number> = {
      A: 0,
      C: 0,
      D: -1,
      E: -1,
      F: 0,
      G: 0,
      H: 0.5,
      I: 0,
      K: 1,
      L: 0,
      M: 0,
      N: 0,
      P: 0,
      Q: 0,
      R: 1,
      S: 0,
      T: 0,
      V: 0,
      W: 0,
      Y: 0,
    }

    let hydrophobicity = 0
    let charge = 0
    let aromaticCount = 0

    for (const aa of sequence) {
      hydrophobicity += hydrophobicityScale[aa] || 0
      charge += chargeScale[aa] || 0
      if (["F", "W", "Y"].includes(aa)) {
        aromaticCount++
      }
    }

    return {
      hydrophobicity: hydrophobicity / sequence.length,
      netCharge: charge,
      aromaticContent: (aromaticCount / sequence.length) * 100,
      length: sequence.length,
    }
  }
}
