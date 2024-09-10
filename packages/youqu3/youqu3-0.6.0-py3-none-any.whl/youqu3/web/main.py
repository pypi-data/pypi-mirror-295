#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
:Author: mikigo
:Date: 2022/11/19 上午9:47
:Desc:
"""
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
from youqu3.web.home import home
from youqu3.web.get_form import form

api_router = APIRouter()


app = FastAPI(
    title="YouQu3 WebServer",
    version="0.1.0",
    description="Next-Gen Linux Autotest Framework.",
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(home)
app.include_router(form)

def main():
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=5656,
        reload=True
    )

if __name__ == '__main__':
    main()