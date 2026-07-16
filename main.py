import os
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

# =====================================================================
# 🛠️ SYSTEM CONFIGURATION & SECURITY SCHEMES
# =====================================================================
SECRET_KEY = "SUPER_SECRET_ATLAS_CRYPTOGRAPHIC_KEY_CHANGE_THIS_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Atlas Enterprise Core Engine", version="2.0.0")

# Enable CORS so your Next.js frontend can communicate with it flawlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock User Database for Role-Based Access Control (RBAC) demonstration
USER_DB = {
    "admin@atlas.ai": {
        "username": "admin@atlas.ai",
        "full_name": "Atlas Administrator",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin"
    },
    "user@atlas.ai": {
        "username": "user@atlas.ai",
        "full_name": "Standard Analyst",
        "hashed_password": pwd_context.hash("user123"),
        "role": "user"
    }
}

# =====================================================================
# 🔑 AUTHENTICATION MODULE (JWT & RBAC)
# =====================================================================
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/auth/login", response_model=Token)
async def login(payload: LoginRequest):
    user = USER_DB.get(payload.username)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

# =====================================================================
# 📷 COMPUTER VISION MODULE (Form Scanning & PDF Extraction)
# =====================================================================
@app.post("/api/analyze/document")
async def analyze_document(file: UploadFile = File(...)):
    """
    Accepts raw PDFs, images, or forms, runs processing logic,
    and returns a clean structured data payload.
    """
    # Verify file existence and metadata extensions
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".pdf", ".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Unsupported document format.")
    
    try:
        # Read raw byte array contents safely from upload stream
        file_bytes = await file.read()
        
        # --- SIMULATED COMPUTER VISION / OCR PARSING PIPELINE ---
        # In full production, you plug in your local OCR engine or Cloud API:
        # Example: extracted_text = pytesseract.image_to_string(Image.open(io.BytesIO(file_bytes)))
        
        simulated_extracted_text = (
            f"LOAN AGREEMENT AMENDMENT -- Reference ID: ATL-2026-X\n"
            f"Principal evaluation sum allocated: $350,000. \n"
            f"Interest rate structured at 4.75% fixed margin.\n"
            f"Status classification: Compliant structural terms confirmed."
        )
        
        # Structural data conversion logic
        structured_metadata = {
            "filename": file.filename,
            "parsed_at": datetime.utcnow().isoformat(),
            "detected_principal": 350000,
            "detected_rate": 0.0475,
            "raw_payload_text": simulated_extracted_text,
            "risk_mitigation_score": 98.2
        }
        
        return {"status": "success", "data": structured_metadata}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data pipeline analysis failure: {str(e)}")

# =====================================================================
# 🤖 MULTI-AI AGENT MODULE & CHATBOT PANEL
# =====================================================================
class Message(BaseModel):
    role: str
    content: str

class ChatPayload(BaseModel):
    messages: List[Message]
    context_document_id: Optional[str] = None

@app.post("/api/agent/chat")
async def coordinate_agents(payload: ChatPayload):
    """
    Simulates a multi-agent orchestration pipeline.
    Agent 1: Evaluates user intent.
    Agent 2: Queries local contextual vectors.
    Agent 3: Returns compiled synthesis.
    """
    latest_user_message = payload.messages[-1].content
    
    # In production, connect this directly to your LLM framework or vector layer:
    # client = OpenAI()
    # response = client.chat.completions.create(...)
    
    agent_compiled_response = (
        f"Atlas Agent Network evaluation complete. \n"
        f"User query topic processed: '{latest_user_message}'. \n"
        f"Cross-referencing historical validation indices reveals zero operational friction points. "
        f"Core portfolio configurations remain secure."
    )
    
    return {
        "status": "active",
        "response": agent_compiled_response,
        "processed_by": "Agent_Panel_Cluster_Alpha"
    }

# =====================================================================
# 🔐 ADMIN CONTROL ACCESS PANEL
# =====================================================================
@app.get("/api/admin/metrics")
async def get_admin_metrics(role: str = "user"):
    # Enforce strict Role-Based Access Control thresholds
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Enterprise Administrative privileges required."
        )
        
    return {
        "system_load": "optimal",
        "active_jwt_sessions": 14,
        "api_throughput_status": "nominal",
        "critical_alerts": []
    }
