package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

type QueryRequest struct {
	CustomerName  string `json:"customer_name"`
	CustomerEmail string `json:"customer_email"`
	Query         string `json:"query"`
}

type AgentResponse struct {
	TicketID  int    `json:"ticket_id"`
	Response  string `json:"response"`
	Sentiment string `json:"sentiment"`
	Intent    string `json:"intent"`
}

func main() {
	godotenv.Load("../.env")

	router := gin.Default()

	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status":  "ok",
			"service": "go-api",
		})
	})

	router.POST("/query", handleQuery)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	fmt.Printf("Go API running on port %s\n", port)
	router.Run(":" + port)
}

func handleQuery(c *gin.Context) {
	var request QueryRequest

	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(400, gin.H{"error": "Invalid request format"})
		return
	}

	if request.Query == "" {
		c.JSON(400, gin.H{"error": "Query cannot be empty"})
		return
	}

	if request.CustomerEmail == "" {
		c.JSON(400, gin.H{"error": "Customer email is required"})
		return
	}

	agentResponse, err := callPythonAgent(request)
	if err != nil {
		c.JSON(500, gin.H{"error": "Agent service unavailable"})
		return
	}

	c.JSON(200, agentResponse)
}

func callPythonAgent(request QueryRequest) (*AgentResponse, error) {
	pythonServiceURL := "http://python-agent:8000/process"
	payload, err := json.Marshal(request)
	if err != nil {
		return nil, err
	}

	resp, err := http.Post(
		pythonServiceURL,
		"application/json",
		bytes.NewBuffer(payload),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var agentResponse AgentResponse
	err = json.Unmarshal(body, &agentResponse)
	if err != nil {
		return nil, err
	}

	return &agentResponse, nil
}
