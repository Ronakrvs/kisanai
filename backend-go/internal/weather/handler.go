package weather

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"

	"github.com/gofiber/fiber/v2"
)

type openMeteoResp struct {
	Current struct {
		Temperature2m     float64 `json:"temperature_2m"`
		RelativeHumidity  int     `json:"relative_humidity_2m"`
		Precipitation     float64 `json:"precipitation"`
		WindSpeed10m      float64 `json:"wind_speed_10m"`
	} `json:"current"`
	Daily struct {
		Time          []string  `json:"time"`
		TempMax       []float64 `json:"temperature_2m_max"`
		TempMin       []float64 `json:"temperature_2m_min"`
		PrecipSum     []float64 `json:"precipitation_sum"`
	} `json:"daily"`
}

type ForecastDay struct {
	Date     string  `json:"date"`
	MaxTemp  float64 `json:"max_temp"`
	MinTemp  float64 `json:"min_temp"`
	Rainfall float64 `json:"rainfall"`
}

type WeatherResponse struct {
	Location struct {
		Lat float64 `json:"lat"`
		Lon float64 `json:"lon"`
	} `json:"location"`
	Current struct {
		Temperature float64 `json:"temperature"`
		Humidity    int     `json:"humidity"`
		Rainfall    float64 `json:"rainfall"`
		WindSpeed   float64 `json:"wind_speed"`
	} `json:"current"`
	Advice   []string      `json:"advice"`
	Forecast []ForecastDay `json:"forecast"`
}

var meteoClient = &http.Client{Timeout: 10 * time.Second}

func Handler(c *fiber.Ctx) error {
	latStr := c.Query("lat")
	lonStr := c.Query("lon")

	lat, err := strconv.ParseFloat(latStr, 64)
	if err != nil || latStr == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "lat required"})
	}
	lon, err := strconv.ParseFloat(lonStr, 64)
	if err != nil || lonStr == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "lon required"})
	}

	url := fmt.Sprintf(
		"https://api.open-meteo.com/v1/forecast?latitude=%.4f&longitude=%.4f"+
			"&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"+
			"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"+
			"&timezone=Asia%%2FKolkata&forecast_days=7",
		lat, lon,
	)

	resp, err := meteoClient.Get(url)
	if err != nil {
		return c.Status(fiber.StatusBadGateway).JSON(fiber.Map{"error": "weather API unavailable"})
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var meteo openMeteoResp
	if err := json.Unmarshal(body, &meteo); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "parse error"})
	}

	advice := buildAdvice(meteo.Current.Temperature2m, float64(meteo.Current.RelativeHumidity), meteo.Current.Precipitation, meteo.Current.WindSpeed10m)

	forecast := make([]ForecastDay, len(meteo.Daily.Time))
	for i, t := range meteo.Daily.Time {
		forecast[i] = ForecastDay{
			Date:     t,
			MaxTemp:  meteo.Daily.TempMax[i],
			MinTemp:  meteo.Daily.TempMin[i],
			Rainfall: meteo.Daily.PrecipSum[i],
		}
	}

	wr := WeatherResponse{}
	wr.Location.Lat = lat
	wr.Location.Lon = lon
	wr.Current.Temperature = meteo.Current.Temperature2m
	wr.Current.Humidity = meteo.Current.RelativeHumidity
	wr.Current.Rainfall = meteo.Current.Precipitation
	wr.Current.WindSpeed = meteo.Current.WindSpeed10m
	wr.Advice = advice
	wr.Forecast = forecast

	return c.JSON(wr)
}

func buildAdvice(temp, humidity, rainfall, windSpeed float64) []string {
	var advice []string

	if rainfall > 70 {
		advice = append(advice, "Heavy rainfall expected — avoid irrigation tomorrow.")
	} else if rainfall < 5 && humidity < 40 {
		advice = append(advice, "Dry conditions detected — irrigate your crops today.")
	}

	if humidity > 90 {
		advice = append(advice, "High humidity — risk of fungal infections. Apply fungicide as a precaution.")
	}

	if temp > 40 {
		advice = append(advice, "Extreme heat — water crops in the early morning or evening only.")
	} else if temp < 10 {
		advice = append(advice, "Cold temperature — protect sensitive crops from frost damage.")
	}

	if windSpeed > 40 {
		advice = append(advice, "Strong winds — avoid spraying pesticides or fertilizers today.")
	}

	if len(advice) == 0 {
		advice = append(advice, "Weather conditions are favourable for farming. Continue regular schedule.")
	}

	return advice
}
