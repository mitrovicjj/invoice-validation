from fastapi import FastAPI
from app.routers import invoices

app = FastAPI(title="Invoice extraction API")

app.include_router(invoices.router, prefix="/api")