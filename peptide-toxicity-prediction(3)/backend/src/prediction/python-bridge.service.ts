import { Injectable } from "@nestjs/common"
import { spawn } from "child_process"
import * as path from "path"

@Injectable()
export class PythonBridgeService {
  async predict(sequences: string[], model = "ensemble") {
    return new Promise((resolve, reject) => {
      // Path to Python script
      const scriptPath = path.join(__dirname, "../../../scripts/predict_api.py")

      // Spawn Python process
      const pythonProcess = spawn("python3", [scriptPath, "--sequences", JSON.stringify(sequences), "--model", model])

      let output = ""
      let errorOutput = ""

      pythonProcess.stdout.on("data", (data) => {
        output += data.toString()
      })

      pythonProcess.stderr.on("data", (data) => {
        errorOutput += data.toString()
      })

      pythonProcess.on("close", (code) => {
        if (code !== 0) {
          reject(new Error(`Python script failed: ${errorOutput}`))
          return
        }

        try {
          const result = JSON.parse(output)
          resolve(result)
        } catch (error) {
          reject(new Error("Failed to parse Python output"))
        }
      })
    })
  }

  async extractFeatures(sequence: string) {
    return new Promise((resolve, reject) => {
      const scriptPath = path.join(__dirname, "../../../scripts/extract_features.py")

      const pythonProcess = spawn("python3", [scriptPath, "--sequence", sequence])

      let output = ""
      let errorOutput = ""

      pythonProcess.stdout.on("data", (data) => {
        output += data.toString()
      })

      pythonProcess.stderr.on("data", (data) => {
        errorOutput += data.toString()
      })

      pythonProcess.on("close", (code) => {
        if (code !== 0) {
          reject(new Error(`Feature extraction failed: ${errorOutput}`))
          return
        }

        try {
          const features = JSON.parse(output)
          resolve(features)
        } catch (error) {
          reject(new Error("Failed to parse feature output"))
        }
      })
    })
  }
}
