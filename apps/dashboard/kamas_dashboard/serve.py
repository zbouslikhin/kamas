import uvicorn

def main():
    uvicorn.run("kamas_dashboard.api:app", reload=True)


if __name__ == "__main__":
    main()
