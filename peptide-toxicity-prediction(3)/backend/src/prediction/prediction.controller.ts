import { Controller, Post, Get, Param, HttpStatus, Body } from "@nestjs/common"
import { ApiTags, ApiOperation, ApiResponse } from "@nestjs/swagger"
import { PredictionService } from "./prediction.service"
import { PredictSequenceDto, BatchPredictDto } from "./dto/predict.dto"

@ApiTags("predictions")
@Controller("api/predictions")
export class PredictionController {
  constructor(private readonly predictionService: PredictionService) {}

  @Post("single")
  @ApiOperation({ summary: "Predict toxicity for a single peptide sequence" })
  @ApiResponse({ status: HttpStatus.OK, description: "Prediction completed successfully" })
  async predictSingle(@Body() dto: PredictSequenceDto) {
    return this.predictionService.predictSingle(dto)
  }

  @Post("batch")
  @ApiOperation({ summary: "Predict toxicity for multiple peptide sequences" })
  @ApiResponse({ status: HttpStatus.OK, description: "Batch prediction completed" })
  async predictBatch(@Body() dto: BatchPredictDto) {
    return this.predictionService.predictBatch(dto)
  }

  @Get("models")
  @ApiOperation({ summary: "Get available ML models" })
  async getModels() {
    return this.predictionService.getAvailableModels()
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get prediction result by ID' })
  async getPrediction(@Param('id') id: string) {
    return this.predictionService.getPredictionById(id)
  }
}
