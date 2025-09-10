from fastapi import FastAPI,File, UploadFile, HTTPException,Request
from app.routes import user, product, order
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI E-commerce Backend")

# setup limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request:Request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# Include routers
app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)


@app.get("/")
@limiter.limit("3/minute;10/hour")
async def root(request:Request):
    return {"message": "E-commerce FastAPI backend running"}


import shutil
import os
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": file_path}


from fastapi.responses import FileResponse

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)