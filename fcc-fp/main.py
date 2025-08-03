from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from psycopg2 import Error as DBError

from .db import get_db_connection

app = FastAPI()
app.mount("/static", StaticFiles(directory="fcc-fp/static"), name="static")
templates = Jinja2Templates(directory="fcc-fp/templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    try:
        conn = get_db_connection()
        conn.close()
        return templates.TemplateResponse("index.html", {"request": request})
    except DBError as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": f"Database connection failed: {e}"},
            status_code=500
        )
