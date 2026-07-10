from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_locations import router as locations_router
from app.api.routes_hazards import router as hazards_router
from app.api.routes_alerts import router as alerts_router

app = FastAPI(title="IGAD Early Warning API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Default Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(locations_router)
app.include_router(hazards_router)
app.include_router(alerts_router)


@app.get("/")
async def root():
    return {"message": "IGAD Early Warning API is running"}
