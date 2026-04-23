# /// script
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "pymongo",
#   "pandas",
# ]
# ///

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import aircom,power,flow,pressure,export_csv,export_data


app = FastAPI(title="Aircom Data API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตทุก Origin
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก Method (GET, POST, etc.)
    allow_headers=["*"],  # อนุญาตทุก Header
)

app.include_router(aircom.router)
app.include_router(power.router)
app.include_router(flow.router)
app.include_router(pressure.router)
app.include_router(export_csv.router)
app.include_router(export_data.router)

@app.get("/")
async def root():
    return {"message": "Server is running smoothly"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8565)