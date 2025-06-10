import uvicorn

from fastapi import FastAPI

from routers.users import router as users_router

app = FastAPI()

app.include_router(users_router)

@app.get("/info")
def get_info_by_this_project():
    return {
        "project": "change",
        "creator_programmer": "Sergey Grishecnko",
        "creator_designer": "Galina Tarasenko",
        "created_year": 2025,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)