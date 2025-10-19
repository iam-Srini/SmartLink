from fastapi import FastAPI

app = FastAPI(title = "SmartLink", version="1.0")

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartLink API"
    }