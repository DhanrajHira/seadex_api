import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", access_log=False, port=8000)
