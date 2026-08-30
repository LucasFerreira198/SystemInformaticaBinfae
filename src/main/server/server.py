from fastapi import FastAPI

#Routers
from src.main.routers.authRoutes import authRoutes

app = FastAPI()

# import routes
app.include_router(authRoutes)
