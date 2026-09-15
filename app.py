from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import shutil
import os

app = FastAPI()

# ✅ CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folders
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

KEY = "SKU"  # change if needed

# ----------------------------
# SAVE FILE FUNCTION
# ----------------------------
def save_file(upload_file):
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path


# ----------------------------
# MAIN API
# ----------------------------
@app.post("/upload/")
async def upload_files(
    amazon: UploadFile = File(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    file3: UploadFile = File(...)
):
    try:
        # Save files
        amazon_path = save_file(amazon)
        f1 = save_file(file1)
        f2 = save_file(file2)
        f3 = save_file(file3)

        # Load Amazon file
        amazon_df = pd.read_excel(amazon_path)
        amazon_df.columns = amazon_df.columns.str.strip()

        results = []

        # Process each file
        for file_path in [f1, f2, f3]:
            df = pd.read_excel(file_path)
            df.columns = df.columns.str.strip()

            # Merge
            merged = df.merge(
                amazon_df,
                on=KEY,
                how="left",
                indicator=True,
                suffixes=('_file', '_amazon')
            )

            # Missing SKUs
            missing = merged[merged['_merge'] == 'left_only']

            output_file = os.path.join(
                OUTPUT_DIR,
                os.path.basename(file_path).replace(".xlsx", "_missing.xlsx")
            )

            missing.to_excel(output_file, index=False)

            results.append({
                "input_file": os.path.basename(file_path),
                "output_file": output_file,
                "missing_count": len(missing)
            })

        return {
            "status": "success",
            "message": "Processing completed",
            "results": results
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }