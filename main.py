from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routes import user, organisation, permissions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="User Access Management",
    description="pyapp backend task",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
   allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error_message": exc.detail})

@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"error_message": "internal server error"})

app.include_router(user.router)
app.include_router(organisation.router)
app.include_router(permissions.router)