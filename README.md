# KisanAI — AI Farming Assistant

Multilingual AI platform for Indian farmers. 100% open source. Near-zero cost MVP.

## Features

| Module | Tech | Status |
|--------|------|--------|
| Crop Disease Detection | YOLOv8n + ONNX | Ready (needs trained model) |
| Fertilizer Recommendation | Random Forest | Ready (needs dataset) |
| Crop Yield Prediction | XGBoost | Ready (needs dataset) |
| Weather-based Advice | Go + Open-Meteo | Ready (no API key needed) |
| AI Chatbot (Hindi + English) | Llama 3 + RAG + pgvector | Ready (needs Ollama) |
| Authentication | Supabase OTP + Google | Ready |

## Architecture

```
Next.js (Vercel)
      ↓
Go Fiber Gateway (Render) — JWT auth, rate limiting
      ↓
┌─────────────────────────────────────────┐
│ Disease (8001) │ Fertilizer (8002)       │
│ Yield (8003)   │ Chatbot (8004)          │
│         Weather (built-in Go)            │
└─────────────────────────────────────────┘
      ↓
PostgreSQL + pgvector (Supabase)
```

## Quick Start (Docker)

```bash
git clone <repo>
cd ai-farming-assistant

# Copy env files
cp backend-go/.env.example backend-go/.env
cp frontend/.env.local.example frontend/.env.local
# Edit both files with your Supabase credentials

# Start everything
docker compose up --build
```

Open http://localhost:3000

## Manual Setup

### 1. Database (Supabase)

1. Create project at supabase.com
2. Run migrations:
   ```sql
   -- In Supabase SQL editor
   \i database/migrations/001_init.sql
   \i database/migrations/002_rls.sql
   ```

### 2. Go Gateway

```bash
cd backend-go
cp .env.example .env   # fill in values
go mod tidy
go run ./cmd/server
```

### 3. Python Services

Each service runs the same way:

```bash
cd services/disease-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8001
```

Repeat for `fertilizer-service` (port 8002), `yield-service` (8003), `chatbot-service` (8004).

### 4. Frontend

```bash
cd frontend
cp .env.local.example .env.local   # fill in Supabase keys
npm install
npm run dev
```

### 5. Chatbot — Install Ollama + Llama 3

```bash
# Install Ollama (https://ollama.com)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3

# Seed knowledge base
cd services/chatbot-service
DATABASE_URL=<your-db-url> python -m app.seed_knowledge
```

## Training the AI Models

### Disease Detection

```bash
cd services/disease-service/models
# Download PlantVillage from Kaggle
kaggle datasets download -d abdallahalidev/plantvillage-dataset
unzip plantvillage-dataset.zip -d data/
python train.py
python train.py export
cp runs/classify/disease_v1/weights/best.onnx models/disease_model.onnx
```

### Fertilizer Model

```bash
cd services/fertilizer-service/models
# Download: https://kaggle.com/datasets/gdabhishek/fertilizer-prediction
python train.py
```

### Yield Model

```bash
cd services/yield-service/models
# Download: https://kaggle.com/datasets/akshatgupta7/crop-yield-in-indian-states-dataset
python train.py
```

## Deploy to Production (Free)

| Component | Platform | Cost |
|-----------|----------|------|
| Frontend | Vercel Free | ₹0 |
| Backend services | Render Free | ₹0 |
| Database | Supabase Free | ₹0 |
| Storage | Supabase Free | ₹0 |
| LLM | Ollama on Render | ₹0 |
| Weather | Open-Meteo | ₹0 |

### Deploy Frontend

```bash
cd frontend
npx vercel --prod
```

### Deploy Backend (Render)

Push to GitHub → Connect repo on render.com → Use `docs/render.yaml`

## Environment Variables

### Gateway (`backend-go/.env`)

```
PORT=8080
ALLOWED_ORIGINS=https://your-app.vercel.app
SUPABASE_JWT_SECRET=<from Supabase settings>
DISEASE_SERVICE_URL=https://kisanai-disease.onrender.com
FERTILIZER_SERVICE_URL=https://kisanai-fertilizer.onrender.com
YIELD_SERVICE_URL=https://kisanai-yield.onrender.com
CHATBOT_SERVICE_URL=https://kisanai-chatbot.onrender.com
```

### Frontend (`frontend/.env.local`)

```
NEXT_PUBLIC_API_URL=https://kisanai-gateway.onrender.com
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

## License

MIT — Free to use, modify, and deploy.
