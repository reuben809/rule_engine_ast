from fastapi import FastAPI
from src.api import router
from src.database import engine, Base

app = FastAPI(title="Rule Engine with AST")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
