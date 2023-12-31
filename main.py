from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from src.routes.dns import dns_router

app = FastAPI()

app.include_router(dns_router, prefix="/dns")

@app.get("/")
async def home():
    return {"message": "Aegis Infrastructure Manager"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")