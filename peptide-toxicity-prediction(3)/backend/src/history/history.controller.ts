import { Controller, Get, Query } from "@nestjs/common"
import { ApiTags, ApiOperation } from "@nestjs/swagger"
import { HistoryService } from "./history.service"

@ApiTags("history")
@Controller("api/history")
export class HistoryController {
  constructor(private readonly historyService: HistoryService) {}

  @Get()
  @ApiOperation({ summary: 'Get prediction history' })
  async getHistory(@Query('limit') limit?: number) {
    return this.historyService.getHistory(limit)
  }

  @Get("stats")
  @ApiOperation({ summary: "Get statistics from prediction history" })
  async getStats() {
    return this.historyService.getStatistics()
  }

  @Get("search")
  @ApiOperation({ summary: "Search prediction history" })
  async search(@Query('q') query: string, @Query('limit') limit?: number) {
    return this.historyService.searchHistory(query, limit)
  }
}
