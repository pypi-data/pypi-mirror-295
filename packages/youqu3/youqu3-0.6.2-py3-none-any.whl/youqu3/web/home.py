#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
:Author: mikigo
:Date: 2022/11/19 上午9:47
:Desc:
"""
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

home = APIRouter()

templates = Jinja2Templates(directory="templates")

hi = f"""
Welcome to use YouQu3
"""

@home.get("/")
async def hello(request: Request):
    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request,
            "title": "YouQu3 WebServer",
            "hi": hi,
        }
    )