import { IsString, IsNotEmpty } from "class-validator"
import { ApiProperty } from "@nestjs/swagger"

export class AnalyzeSequenceDto {
  @ApiProperty({
    description: "Peptide sequence to analyze",
    example: "ACDEFGHIKLMNPQRSTVWY",
  })
  @IsString()
  @IsNotEmpty()
  sequence: string
}
