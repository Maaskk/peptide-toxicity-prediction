import { Module } from "@nestjs/common"
import { PredictionController } from "./prediction.controller"
import { PredictionService } from "./prediction.service"
import { PythonBridgeService } from "./python-bridge.service"

@Module({
  controllers: [PredictionController],
  providers: [PredictionService, PythonBridgeService],
  exports: [PredictionService],
})
export class PredictionModule {}
