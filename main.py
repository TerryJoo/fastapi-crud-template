from fastapi import FastAPI

import user
from dbs import sqlite3
from user import init_db

app = FastAPI()
init_db(engine=sqlite3.get_engine())


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, reload=True, proxy_headers=True, forwarded_allow_ips="*")
