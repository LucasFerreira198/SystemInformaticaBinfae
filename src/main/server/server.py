from fastapi import FastAPI

#Routers
from src.main.routers.authRoutes import authRoutes
from src.main.routers.userRoutes import userRoutes

app = FastAPI()

# import routes
app.include_router(authRoutes)
app.include_router(userRoutes)
