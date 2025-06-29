import io
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv
from utils import predict
from supabase import create_client

# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inisialisasi Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inisialisasi FastAPI
app = FastAPI()

# Middleware CORS untuk akses frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "NutriAPI aktif"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), save: bool = Form(True)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")  # Penting!
        result = predict(image)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": f"Gagal prediksi: {str(e)}"}


@app.get("/history")
def get_history(user_id: int):
    try:
        response = supabase.table("history") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("detected_at", desc=True) \
            .execute()

        data = response.data
        history = [
            {
                "date": item["detected_at"][:10] if item["detected_at"] else None,
                "food": item["food"],
                "nutrition": {
                    "kalori": item["kalori"],
                    "protein": item["protein"],
                    "lemak": item["lemak"],
                    "karbo": item["karbo"],
                }
            }
            for item in data 
        ]
        return {"status": "success", "history": history}
    except Exception as e:
        print("Gagal mengambil history:", str(e))
        return {"status": "error", "message": f"Gagal mengambil riwayat: {str(e)}"}
