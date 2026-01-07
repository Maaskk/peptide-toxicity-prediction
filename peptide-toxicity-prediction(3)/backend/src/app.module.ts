import { Module } from "@nestjs/common"
import { ConfigModule } from "@nestjs/config"
import { PredictionModule } from "./prediction/prediction.module"
import { AnalysisModule } from "./analysis/analysis.module"
import { HistoryModule } from "./history/history.module"
import { DatabaseModule } from "./database/database.module"

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    DatabaseModule,
    PredictionModule,
    AnalysisModule,
    HistoryModule,
  ],
})
export class AppModule {}
