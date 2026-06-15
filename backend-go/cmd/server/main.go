package main

import (
	"log"
	"os"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/limiter"
	"github.com/joho/godotenv"
	"github.com/kisanai/backend/internal/gateway"
	"github.com/kisanai/backend/internal/middleware"
	"github.com/kisanai/backend/internal/weather"
)

func main() {
	_ = godotenv.Load()

	app := fiber.New(fiber.Config{
		BodyLimit: 15 * 1024 * 1024, // 15MB for images
		ErrorHandler: func(c *fiber.Ctx, err error) error {
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
		},
	})

	app.Use(logger.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins: os.Getenv("ALLOWED_ORIGINS"),
		AllowHeaders: "Origin, Content-Type, Accept, Authorization",
	}))
	app.Use(limiter.New(limiter.Config{
		Max:        60,
		Expiration: 60,
	}))

	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "ok"})
	})

	// Protected routes
	api := app.Group("/api", middleware.JWTOptional())

	api.Post("/disease-detect", gateway.ProxyTo(os.Getenv("DISEASE_SERVICE_URL")+"/detect"))
	api.Post("/fertilizer", gateway.ProxyTo(os.Getenv("FERTILIZER_SERVICE_URL")+"/recommend"))
	api.Post("/yield", gateway.ProxyTo(os.Getenv("YIELD_SERVICE_URL")+"/predict"))
	api.Post("/chat", gateway.ProxyTo(os.Getenv("CHATBOT_SERVICE_URL")+"/chat"))
	api.Get("/weather-advice", weather.Handler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Gateway running on :%s", port)
	log.Fatal(app.Listen(":" + port))
}
