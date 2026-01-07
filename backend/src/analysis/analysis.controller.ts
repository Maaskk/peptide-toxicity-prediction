import { Controller, Post, Body } from "@nestjs/common"
import { ApiTags, ApiOperation } from "@nestjs/swagger"
import { AnalysisService } from "./analysis.service"
import { AnalyzeSequenceDto } from "./dto/analyze.dto"

@ApiTags("analysis")
@Controller("api/analysis")
export class AnalysisController {
  constructor(private readonly analysisService: AnalysisService) {}

  @Post("features")
  @ApiOperation({ summary: "Extract and analyze features from a peptide sequence" })
  async analyzeFeatures(@Body() dto: AnalyzeSequenceDto) {
    return this.analysisService.analyzeFeatures(dto)
  }

  @Post("physicochemical")
  @ApiOperation({ summary: "Calculate physicochemical properties" })
  async analyzeProperties(@Body() dto: AnalyzeSequenceDto) {
    return this.analysisService.analyzePhysicochemicalProperties(dto)
  }
}
