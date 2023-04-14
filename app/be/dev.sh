#!/bin/env sh

cd src && uvicorn main:app --port 8080 --reload
