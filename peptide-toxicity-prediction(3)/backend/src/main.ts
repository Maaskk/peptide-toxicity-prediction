import { NestFactory } from "@nestjs/core"
import { ValidationPipe } from "@nestjs/common"
import { SwaggerModule, DocumentBuilder } from "@nestjs/swagger"
import { AppModule } from "./app.module"

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    cors: true,
  })

  // Global validation pipe
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  )

  // Swagger API documentation
  const config = new DocumentBuilder()
    .setTitle("Peptide Toxicity Prediction API")
    .setDescription("Professional bioinformatics API for peptide toxicity prediction using machine learning")
    .setVersion("1.0")
    .addTag("predictions")
    .addTag("analysis")
    .addTag("history")
    .addBearerAuth()
    .build()

  const document = SwaggerModule.createDocument(app, config)
  SwaggerModule.setup("api/docs", app, document)

  await app.listen(3001)
  console.log("🚀 NestJS API running on http://localhost:3001")
  console.log("📚 API Documentation: http://localhost:3001/api/docs")
}

bootstrap()
