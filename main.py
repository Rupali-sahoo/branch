import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from orchestration.workflow import FatigueWorkflow
from memory.history_store import HistoryStore


app = FastAPI(
    title="FatigueSense API",
    description="Backend API for FatigueSense",
    version="1.0.0"
)


# ---------------------------------------
# CORS
# ---------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ---------------------------------------
# Directories
# ---------------------------------------

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ---------------------------------------
# Objects
# ---------------------------------------

workflow = FatigueWorkflow()
history_store = HistoryStore()


# ---------------------------------------
# Health Check
# ---------------------------------------

@app.get("/")
def home():

    return {
        "message": "FatigueSense API is running"
    }


# ---------------------------------------
# Analyze Image
# ---------------------------------------

@app.post("/analyze")
async def analyze_image(
    user_id: str = Form(...),
    image: UploadFile = File(...)
):

    try:

        # ------------------------------
        # Validate extension
        # ------------------------------

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".heic"
        }

        extension = Path(image.filename).suffix.lower()

        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail="Unsupported image format"
            )

        # ------------------------------
        # Save uploaded image
        # ------------------------------

        safe_filename = Path(image.filename).name

        file_path = UPLOAD_DIR / safe_filename

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                image.file,
                buffer
            )

        # ------------------------------
        # Run complete workflow
        # ------------------------------

        result = workflow.analyze(
            user_id=user_id,
            image_path=str(file_path),
            image_name=safe_filename
        )

        # ------------------------------
        # Return result
        # ------------------------------

        return result

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------
# Get History
# ---------------------------------------

@app.get("/history/{user_id}")
def get_history(user_id: str):

    history = history_store.get_history(user_id)

    return {
        "success": True,
        "user_id": user_id,
        "history": history
    }