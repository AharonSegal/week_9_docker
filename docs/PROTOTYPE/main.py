from fastapi import FastAPI
from endpoints import router, check_database_exists

app = FastAPI(title="Items API", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    check_database_exists()


# Include all endpoints from endpoints.py
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    # This is only for local development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)