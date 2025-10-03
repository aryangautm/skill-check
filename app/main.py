from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resume_router
from app.core.database import Base, get_engine

app = FastAPI(
    title="Skill Check API",
    description="AI-powered resume analysis and MCQ quiz generation platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_router, prefix="/api", tags=["Resume & Questions"])


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Skill Check API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
