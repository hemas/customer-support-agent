# AI-Powered Customer Support Agent 🤖

A production-grade intelligent customer support system that automatically handles customer queries using AI, detects emotions, searches a knowledge base, and generates empathetic responses.

Built to demonstrate production-grade full stack AI engineering 
skills combining Vue.js, Node.js, Python, Agentic AI, and modern 
backend development.

## 🏗️ Architecture Evolution
### Original Architecture
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

### Current Architecture
```
Customer Message
↓
Vue.js Frontend (Port 5173) — Modern UI
↓
Node.js BFF (Port 3000) — API gateway & routing
↓
Python AI Agent (Port 8000) — AI processing
↓
PostgreSQL — Data storage
```


### Why we evolved

| Component | Before | After | Reason |
|---|---|---|---|
| Frontend | None | Vue.js | Modern UI for end users |
| API Gateway | Go | Node.js BFF | Better fit for Vue frontend |
| Testing | None | Jest + Vitest | Production grade quality |
| CI/CD | None | GitHub Actions | Automated deployment |

The Go API (`api/`) is preserved in the codebase as 
reference for the original architecture. The Node.js BFF 
replaced it to better support the Vue.js frontend using 
the Backend For Frontend (BFF) pattern.


## 🛠️ Tech Stack

**Frontend:**
- Vue.js 3 — Modern reactive frontend
- Vue Router — Client side navigation
- Pinia — State management
- Axios — HTTP requests

**Backend (BFF):**
- Node.js — JavaScript runtime
- Express.js — Web framework
- Morgan — Request logging
- Jest — Unit testing
- Supertest — API testing

**AI Agent:**
- Python — AI logic and data processing
- FastAPI — Python web framework
- LangChain — Agentic AI framework
- Groq AI (Llama 3) — LLM for response generation

**Database:**
- PostgreSQL — Customer data, tickets, conversations
- pgvector — Vector embeddings for knowledge base search

**DevOps:**
- Docker — Containerization
- GitHub Actions — CI/CD pipeline

## ✨ Features

- Real-time chat interface with AI responses
- Switch between AI providers (OpenAI/Groq)
- Automatic sentiment analysis
- Intelligent intent detection (billing, technical, shipping)
- Autonomous AI agent with RAG knowledge base search
- Automatic escalation to human when needed
- Support ticket management system
- Full conversation history saved to PostgreSQL
- Containerized with Docker
- CI/CD with GitHub Actions
- Jest + Vitest + Playwright test coverage

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL
- Docker Desktop
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
# bff/.env
PORT=3000
PYTHON_SERVICE_URL=http://localhost:8000
CLIENT_URL=http://localhost:5173

3. Install dependencies:
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js BFF dependencies
cd bff && npm install

# Install Vue frontend dependencies
cd ../client && npm install
```

4. Start all services:
```bash
# Terminal 1 - Python AI Agent
cd agent && python3 api.py

# Terminal 2 - Node.js BFF
cd bff && node src/index.js

# Terminal 3 - Vue Frontend
cd client && npm run dev
```

4. Open browser:
    http://localhost:5173

    ## 📁 Project Structure
    ```
customer-support-agent/
├── agent/                    # Python AI Agent
│   ├── api.py               # FastAPI endpoints
│   ├── main.py              # AI agent logic
│   └── tools/
│       ├── sentiment_tool.py # Sentiment analysis
│       ├── rag_tool.py      # Knowledge base search
│       └── database_tool.py # PostgreSQL operations
├── api/                     # Original Go API (preserved)
│   └── main.go              # Go API gateway
├── bff/                     # Node.js BFF
│   ├── src/
│   │   ├── index.js         # Express server
│   │   └── routes/
│   │       ├── chat.js      # Chat routes
│   │       └── tickets.js   # Ticket routes
│   └── tests/               # Jest tests
│       ├── chat.test.js
│       └── tickets.test.js
├── client/                  # Vue.js Frontend
│   └── src/
│       ├── App.vue          # Root component
│       ├── router/          # Vue Router
│       └── views/
│           ├── ChatView.vue    # Chat page
│           └── TicketsView.vue # Tickets page
├── database/
│   └── schema.sql           # PostgreSQL schema
├── docker-compose.yml
└── requirements.txt
```

## 🔄 How It Works

1. User opens Vue.js frontend at localhost:5173
2. User types message and selects AI provider (OpenAI/Groq)
3. Vue sends POST request to Node.js BFF
4. Node.js validates and forwards to Python agent
5. Python detects sentiment and intent
6. LangChain agent searches knowledge base using pgvector
7. Groq AI generates empathetic response
8. Ticket saved to PostgreSQL
9. Response returned through Node.js to Vue
10. User sees AI response in chat window

## 📝 API Endpoints

### Node.js BFF (Port 3000)

**GET /health**
```json
Response:
{
  "status": "ok"
}
```

**POST /api/chat/process**
```json
Request:
{
  "message": "I need help with my order",
  "customer_name": "John",
  "customer_email": "john@email.com",
  "provider": "groq"
}

Response:
{
  "ticket_id": 15,
  "response": "I understand your concern...",
  "sentiment": "NEUTRAL",
  "intent": "shipping"
}
```

**GET /api/tickets**
```json
Response:
[
  {
    "id": 15,
    "query": "I need help with my order",
    "sentiment": "NEUTRAL",
    "intent": "shipping",
    "status": "open"
  }
]
```

**PUT /api/tickets/:id**
```json
Request:
{
  "status": "resolved"
}

Response:
{
  "id": 15,
  "status": "resolved"
}
```

## 🧪 Running Tests

```bash
# Jest tests (Node.js BFF)
cd bff && npm test

# Vitest tests (Vue frontend) - coming soon
cd client && npm run test

# Playwright E2E tests - coming soon
cd client && npm run test:e2e
```

## 👨‍💻 Author

Hema Pappu
- GitHub: github.com/hemas