from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
import ollama
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

app = FastAPI(title="SmartMail AI with Ollama")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get credentials from environment
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_APP_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    print("⚠️  WARNING: SENDER_EMAIL or SENDER_APP_PASSWORD not set in .env")

# Allow Docker to connect to host Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Initialize Ollama with custom host
print("📦 Connecting to Ollama (Mistral)...")
print(f"🔗 Using Ollama host: {OLLAMA_HOST}")
try:
    # Create Ollama client with custom host
    client = ollama.Client(host=OLLAMA_HOST)
    # Test connection
    client.list()
    print("✅ Ollama connected successfully!")
    generator = "ollama"
except Exception as e:
    print(f"⚠️  Ollama not available: {e}")
    print("💡 Install Ollama from https://ollama.com and run: ollama pull mistral")
    generator = None

# Models
class EmailRecipient(BaseModel):
    email: EmailStr

class EmailRequest(BaseModel):
    to: List[EmailRecipient]
    cc: Optional[List[EmailRecipient]] = []
    bcc: Optional[List[EmailRecipient]] = []
    subject: str
    body: str

class AIGenerateRequest(BaseModel):
    prompt: str
    tone: str = "professional"

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_files = []

@app.get("/")
def root():
    return {
        "message": "SmartMail AI with Ollama",
        "status": "running",
        "sender_configured": SENDER_EMAIL is not None,
        "ai_ready": generator is not None,
        "ollama_host": OLLAMA_HOST
    }

@app.get("/sender-info")
def get_sender_info():
    """Get sender email for frontend display"""
    if not SENDER_EMAIL:
        raise HTTPException(status_code=500, detail="Sender email not configured")
    return {
        "email": SENDER_EMAIL,
        "configured": True
    }

@app.post("/ai/generate")
async def generate_email(request: AIGenerateRequest):
    """Generate email content using Mistral via Ollama"""
    if not generator:
        raise HTTPException(status_code=500, detail="AI model not available. Install Ollama and run: ollama pull mistral")
    
    try:
        tone_styles = {
            "professional": "professional and businesslike",
            "casual": "casual and friendly",
            "formal": "formal and respectful",
            "friendly": "warm and friendly"
        }
        
        style = tone_styles.get(request.tone, "professional")
        
        prompt = f"""Write a {style} email about: {request.prompt}

Requirements:
- If the name of the recipient is known, include it in the greeting, else use a generic greeting
- Don't include the subject of the mail
- Only write the email body
- Include appropriate greeting
- Clear and concise content
- Proper closing

Email:"""
        
        # Use client.generate() instead of ollama.generate()
        response = client.generate(
            model='mistral',
            prompt=prompt,
            options={
                'temperature': 0.7,
                'top_p': 0.9,
            }
        )
        
        generated_text = response['response'].strip()
        
        return {
            "success": True,
            "generated_text": generated_text,
            "tone": request.tone
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file for attachment"""
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        uploaded_files.append(file_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "filepath": file_path,
            "size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/upload/{filename}")
async def delete_file(filename: str):
    """Delete uploaded file"""
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            if file_path in uploaded_files:
                uploaded_files.remove(file_path)
            return {"success": True, "message": "File deleted"}
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send")
async def send_email(request: EmailRequest):
    """Send email via SMTP using credentials from .env"""
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="Sender credentials not configured"
        )
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ', '.join([r.email for r in request.to])
        if request.cc:
            msg['Cc'] = ', '.join([r.email for r in request.cc])
        msg['Subject'] = request.subject
        
        # Add body
        msg.attach(MIMEText(request.body, 'plain'))
        
        # Add attachments
        for filepath in uploaded_files:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(filepath)}'
                    )
                    msg.attach(part)
        
        # All recipients
        all_recipients = [r.email for r in request.to]
        all_recipients.extend([r.email for r in request.cc])
        all_recipients.extend([r.email for r in request.bcc])
        
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg, to_addrs=all_recipients)
        
        # Clear uploaded files
        for filepath in uploaded_files:
            if os.path.exists(filepath):
                os.remove(filepath)
        uploaded_files.clear()
        
        return {
            "success": True,
            "message": "Email sent successfully!",
            "recipients": len(all_recipients),
            "from": SENDER_EMAIL
        }
        
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=401, 
            detail="Authentication failed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)