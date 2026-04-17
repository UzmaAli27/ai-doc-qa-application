from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import pdf_routes
from routes import qa_routes
from routes import media_routes
from routes import unified_qa_routes
from routes import query_routes

from services.embedding_service import load_vector_store


# STEP 1: create app
app = FastAPI(
    title="Multimodal Document QA Assistant",
    description="Upload PDFs, Videos, Audio and ask semantic questions with AI answers",
    version="1.0"
)


# STEP 2: CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# STEP 3: load vector store at startup
@app.on_event("startup")
def startup_event():
    load_vector_store()


# STEP 4: register routes
app.include_router(pdf_routes.router)
app.include_router(qa_routes.router)
app.include_router(media_routes.router)
app.include_router(unified_qa_routes.router)
app.include_router(query_routes.router)


# STEP 5: root endpoint
@app.get("/")
def home():
    return {
        "message": "AI Document QA Backend Running Successfully"
    }