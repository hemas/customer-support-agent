# AI-Powered Customer Support Agent 🤖

A production-grade intelligent customer support system that automatically handles customer queries using AI, detects emotions, searches a knowledge base, and generates empathetic responses.

Built this project to demonstrate production grade AI engineering skills comibing Agentic AI, AQS, ML and modern backend development

## 🏗️ Architecture
```
Customer Message
      ↓
Go API (Port 8080)
      ↓
Python AI Agent (Port 8000)
      ↓
AWS Comprehend → Sentiment Analysis
Groq AI (Llama 3) → Response Generation
PostgreSQL → Data Storage
```

## 🛠️ Tech Stack

- **Python** — AI Agent, AWS integration, data processing
- **Go** — High performance REST API gateway
- **PostgreSQL** — Customer data, tickets, conversations
- **AWS Comprehend** — Sentiment analysis and intent detection
- **LangChain** — Agentic AI framework
- **Groq AI (Llama 3)** — Free LLM for response generation
- **Docker** — Containerization

## ✨ Features

- Real-time sentiment analysis using AWS Comprehend
- Intelligent intent detection (billing, technical, general)
- Autonomous AI agent that thinks and decides independently
- Knowledge base search for accurate answers
- Automatic escalation to human when needed
- Full conversation history saved to PostgreSQL
- Containerized with Docker for easy deployment

## 🚀 Getting Started

### Prerequisites
- Docker Desktop
- AWS Account with Comprehend access
- Groq API key (free at console.groq.com)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hemas/customer-support-agent.git
cd customer-support-agent
```

2. Create .env file:
```
GROQ_API_KEY=your_groq_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
DB_HOST=postgres
DB_PORT=5432
DB_NAME=support_agent_db
DB_USER=postgres
DB_PASSWORD=postgres123
```

3. Start everything:
```bash
docker-compose up -d
```

4. Test it:
```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Smith",
    "customer_email": "john@example.com",
    "query": "I was charged twice this month!"
  }'
```

## 📁 Project Structure
```
customer-support-agent/
├── agent/
│   ├── main.py          # AI Agent brain
│   ├── api.py           # FastAPI service
│   └── tools/
│       ├── sentiment_tool.py   # AWS Comprehend
│       └── database_tool.py    # PostgreSQL
├── api/
│   └── main.go          # Go API gateway
├── database/
│   └── schema.sql       # Database schema
├── docker-compose.yml
└── requirements.txt
```

## 🔄 How It Works

1. Customer sends message to Go API
2. Go API forwards to Python AI Agent
3. AWS Comprehend detects sentiment and intent
4. LangChain Agent searches knowledge base
5. Groq AI generates empathetic response
6. Full conversation saved to PostgreSQL
7. Response returned to customer

## 📝 API Endpoints

### POST /query
Send a customer message and get AI response.

Request:
```json
{
  "customer_name": "John Smith",
  "customer_email": "john@example.com",
  "query": "I was charged twice this month!"
}
```

Response:
```json
{
  "ticket_id": 1,
  "response": "I understand your frustration...",
  "sentiment": "NEGATIVE",
  "intent": "billing"
}
```
## 👨‍💻 Author
Hema Pappu
- GitHub: github.com/hemas
