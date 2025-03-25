# AI Story Teller Tool for Children - NiteStory.AI
CS687 Capstone project (City University of Seattle) Winter 2025

1. Install all libraries and dependencies
```
Cd backend
```
```
pip install -r requirements.txt
```
2. Update .env file with your API keys:
```
HUGGINGFACEHUB_API_TOKEN=hf_X....
OPENAI_API_KEY=sk-qz.....
REACT_APP_API_URL=https://....-8000.app.github.dev
```
3. Start backend

```
Cd backend
```
```
uvicorn app.main:app --reload 
```
3. Start frontend:

```
Cd frontend
```
```
Npm start
``` 

**Demo:** http://localhost:3000/ 

**Test API:** http://127.0.0.1:8000/docs#/ 

Note: use pictures and pdf files from Testing data if needed
