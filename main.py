from fastapi import FastAPI
from routers import programs, days, exercises, users, progress, register

app = FastAPI()

# Register routers
app.include_router(programs.router)
app.include_router(days.router)
app.include_router(exercises.router)
app.include_router(users.router)
app.include_router(progress.router)  
app.include_router(register.router)  

@app.get("/")
def root():
    return {"message": "API is running"}
