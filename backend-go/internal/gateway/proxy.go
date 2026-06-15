package gateway

import (
	"bytes"
	"io"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
)

var httpClient = &http.Client{Timeout: 30 * time.Second}

// ProxyTo forwards the incoming request to targetURL and streams back the response.
func ProxyTo(targetURL string) fiber.Handler {
	return func(c *fiber.Ctx) error {
		req, err := http.NewRequest(c.Method(), targetURL, nil)
		if err != nil {
			return fiber.ErrInternalServerError
		}

		// Forward body
		body := c.Body()
		if len(body) > 0 {
			req.Body = io.NopCloser(bytes.NewReader(body))
			req.ContentLength = int64(len(body))
		}

		// Forward headers
		c.Request().Header.VisitAll(func(k, v []byte) {
			req.Header.Set(string(k), string(v))
		})

		// Propagate user identity
		if uid := c.Locals("user_id"); uid != nil {
			req.Header.Set("X-User-ID", uid.(string))
		}

		resp, err := httpClient.Do(req)
		if err != nil {
			return c.Status(fiber.StatusBadGateway).JSON(fiber.Map{
				"error": "upstream service unavailable",
			})
		}
		defer resp.Body.Close()

		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			return fiber.ErrInternalServerError
		}

		c.Status(resp.StatusCode)
		c.Set("Content-Type", resp.Header.Get("Content-Type"))
		return c.Send(respBody)
	}
}
