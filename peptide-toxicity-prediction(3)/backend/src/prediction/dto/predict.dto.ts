import { IsString, IsNotEmpty, IsOptional, IsArray, ArrayMinSize } from "class-validator"
import { ApiProperty } from "@nestjs/swagger"

export class PredictSequenceDto {
  @ApiProperty({
    description: "Peptide sequence using standard amino acid letters",
    example: "ACDEFGHIKLMNPQRSTVWY",
  })
  @IsString()
  @IsNotEmpty()
  sequence: string

  @ApiProperty({
    description: "ML model to use for prediction",
    example: "ensemble",
    required: false,
  })
  @IsString()
  @IsOptional()
  model?: string
}

export class BatchPredictDto {
  @ApiProperty({
    description: "Array of peptide sequences",
    example: ["ACDEFGHIK", "MKLPQRSTVWY"],
  })
  @IsArray()
  @ArrayMinSize(1)
  @IsString({ each: true })
  sequences: string[]

  @ApiProperty({
    description: "ML model to use for prediction",
    example: "ensemble",
    required: false,
  })
  @IsString()
  @IsOptional()
  model?: string
}
