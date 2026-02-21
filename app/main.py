from fastapi import FastAPI
from app.parser import router as parser_router
from app.validator import router as validator_router
from app.temporal import router as temporal_router
from app.investment import router as investment_router
from app.performance import router as performance_router

app = FastAPI(title="BlackRock Auto Saving API")

app.include_router(parser_router)
app.include_router(validator_router)
app.include_router(temporal_router)
app.include_router(investment_router)
app.include_router(performance_router)