# 📧 SmartMail AI - Cinematic Edition

> **AI-Powered Email Sender with Ollama Integration**  
> Send professional emails with AI-generated content using Mistral LLM, all wrapped in a stunning cinematic interface.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Ollama](https://img.shields.io/badge/Ollama-Mistral-orange)

---
## ⚠️ Important Notice

> 🔬 This is a lightweight demonstration version of the full SmartMail AI project.
>
> 📦 AI Model Notice: This version uses Ollama with Mistral for easy local 
> testing and deployment. The production version utilizes robust Hugging Face 
> models for enhanced performance, accuracy, and enterprise-grade reliability.
>
> *This simplified version is designed for quick setup, testing, and 
> educational purposes.*

## 🌟 Features

- ✨ **AI Email Generation** - Generate professional emails using Mistral LLM via Ollama
- 📤 **SMTP Email Sending** - Send emails directly through Gmail SMTP
- 📎 **File Attachments** - Upload and attach files to your emails
- 🎨 **Cinematic UI** - Beautiful black & white glassmorphic interface with animations
- 🎯 **Multiple Recipients** - Support for To, CC, and BCC recipients
- 🎭 **Tone Selection** - Choose from Professional, Casual, Formal, or Friendly tones
- 🐳 **Docker Ready** - Fully containerized for easy deployment
- 🔒 **Secure** - Environment-based credentials management

---

## 📁 Project Structure

```
SmartMailAI/
│
├── backend/                        # Backend Application
│   ├── main.py                    # FastAPI server with AI integration
│   ├── .env                       # Environment variables (credentials)
│   └── uploads/                   # Temporary file storage
│
├── frontend/                       # Frontend Application
│   └── index.html                 # Cinematic UI interface
│
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker build instructions
├── docker-compose.yml              # Docker orchestration
├── .dockerignore                   # Docker build exclusions
├── .gitignore                      # Git exclusions
└── README.md                       # This file
```

---

## 🛠️ Technology Stack

### **Backend:**
- **FastAPI** - Modern Python web framework
- **Ollama** - Local LLM inference (Mistral model)
- **SMTP** - Email sending via Gmail
- **Python 3.11** - Programming language

### **Frontend:**
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No frameworks needed
- **Glassmorphism Design** - Cinematic black & white theme

### **DevOps:**
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## 🚀 Quick Start

### **Prerequisites**

1. **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
2. **Ollama** - [Download here](https://ollama.com)
3. **Gmail Account** with App Password

---

## ⚙️ Configuration

### **Step 1: Set Up Gmail App Password**

1. Go to your [Google Account Settings](https://myaccount.google.com/)
2. Navigate to **Security** → **2-Step Verification** (enable if not already)
3. Scroll down to **App passwords**
4. Generate a new app password for "Mail"
5. Copy the 16-character password

### **Step 2: Configure Environment Variables**

Create/Edit `backend/.env` file:

```env
# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_APP_PASSWORD=your-16-char-app-password

# Ollama Configuration (optional - auto-detected in Docker)
OLLAMA_HOST=http://host.docker.internal:11434
```

⚠️ **IMPORTANT:**
- Replace `your-email@gmail.com` with your actual Gmail address
- Replace `your-16-char-app-password` with the app password from Google
- **NEVER commit `.env` to Git** (already in `.gitignore`)

**Example `.env` file:**
```env
SENDER_EMAIL=john.doe@gmail.com
SENDER_APP_PASSWORD=abcd efgh ijkl mnop
OLLAMA_HOST=http://host.docker.internal:11434
```

### **Step 3: Install Ollama and Download Mistral**

```bash
# Install Ollama (if not already installed)
# Visit https://ollama.com and follow installation instructions

# Pull the Mistral model
ollama pull mistral

# Start Ollama server
ollama serve
```

**Keep the Ollama server running** (it needs to be active for AI generation).

---

## 🐳 Docker Deployment

### **Option 1: Using Docker Compose (Recommended)**

```bash
# 1. Navigate to project root
cd SmartMailAI

# 2. Make sure Ollama is running
ollama serve

# 3. Start the container
docker-compose up -d

# 4. Check logs
docker-compose logs -f

# 5. Open frontend/index.html in your browser
```

### **Option 2: Using Docker Commands**

```bash
# Build the image
docker build -t smartmail-ai .

# Run the container (Windows)
docker run -d -p 8000:8000 --name smartmail \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  -v "%cd%/backend/uploads:/app/uploads" \
  smartmail-ai

# Run the container (Mac/Linux)
docker run -d -p 8000:8000 --name smartmail \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  -v "$(pwd)/backend/uploads:/app/uploads" \
  smartmail-ai
```

---

## 🎯 Usage

### **For End Users:**

1. **Start the Backend:**
   ```bash
   docker-compose up -d
   ```

2. **Open the Frontend:**
   - Navigate to `frontend/` folder
   - Open `index.html` in your web browser
   - Or visit: `file:///path/to/SmartMailAI/frontend/index.html`

3. **Send an Email:**
   - Add recipients in the "To" field
   - (Optional) Add CC/BCC recipients
   - Enter subject line
   - Use AI generation or write manually
   - Attach files if needed
   - Click "Send Email"

### **For Developers:**

```bash
# View real-time logs
docker-compose logs -f

# Stop the application
docker-compose down

# Restart after code changes
docker-compose up -d --build

# Access container shell
docker exec -it smartmail bash

# Check container status
docker ps

# View all containers (including stopped)
docker ps -a
```

---

## 🤖 AI Email Generation

The AI generation feature uses **Ollama** with the **Mistral** model to create contextually appropriate emails.

**How it works:**
1. User provides a prompt (e.g., "Request a meeting for next week")
2. Selects desired tone (Professional, Casual, Formal, Friendly)
3. AI generates complete email content
4. User can edit before sending

**Supported Tones:**
- **Professional** - Business-appropriate language
- **Casual** - Friendly and relaxed
- **Formal** - Highly respectful and structured
- **Friendly** - Warm and personable

---

## 📊 API Endpoints

The backend exposes the following REST API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and status |
| GET | `/sender-info` | Get configured sender email |
| POST | `/ai/generate` | Generate email with AI |
| POST | `/upload` | Upload file attachment |
| DELETE | `/upload/{filename}` | Delete uploaded file |
| POST | `/send` | Send email via SMTP |

**Example API Call:**
```bash
# Generate AI email
curl -X POST http://localhost:8000/ai/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Request a meeting next week",
    "tone": "professional"
  }'
```

---

## 🔒 Security Best Practices

✅ **DO:**
- Use Gmail App Passwords (never your actual password)
- Keep `.env` file in `.gitignore`
- Use environment variables for sensitive data
- Enable 2-Factor Authentication on Gmail

❌ **DON'T:**
- Commit `.env` to version control
- Share your app password publicly
- Use your main Gmail password
- Hardcode credentials in code

---

## 🐛 Troubleshooting

### **Problem: "Ollama not available"**

**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# Check if Mistral is installed
ollama list

# If not, install it
ollama pull mistral

# Restart container
docker-compose restart
```

### **Problem: "Sender credentials not configured"**

**Solution:**
- Check that `backend/.env` exists
- Verify `SENDER_EMAIL` and `SENDER_APP_PASSWORD` are set correctly
- Rebuild container: `docker-compose up -d --build`

### **Problem: "AI generation failed"**

**Solution:**
- Ensure Ollama is running: `ollama serve`
- Check Docker logs: `docker-compose logs -f`
- Verify Mistral model is downloaded: `ollama list`

### **Problem: "Email sending failed"**

**Solution:**
- Verify Gmail App Password is correct (16 characters)
- Check that 2-Step Verification is enabled on Gmail
- Ensure you're using App Password, not account password
- Check SMTP settings in `main.py` (smtp.gmail.com:465)

### **Problem: Port 8000 already in use**

**Solution:**
```bash
# Stop existing container
docker-compose down

# Or use different port in docker-compose.yml
ports:
  - "8001:8000"  # Change host port to 8001
```

---

## 🚢 Deployment for Others

### **Sharing Your Project:**

1. **Clone the Repository:**
   ```bash
   git clone <your-repo-url>
   cd SmartMailAI
   ```

2. **Set Up Environment:**
   ```bash
   # Copy example env file
   cp backend/.env.example backend/.env
   
   # Edit with your credentials
   nano backend/.env
   ```

3. **Install Ollama:**
   - Visit https://ollama.com
   - Download and install for your OS
   - Run: `ollama pull mistral`

4. **Start Everything:**
   ```bash
   # Terminal 1: Start Ollama
   ollama serve
   
   # Terminal 2: Start Docker
   docker-compose up -d
   ```

5. **Access Application:**
   - Open `frontend/index.html` in browser
   - Start sending emails! 🚀

---

## 📦 Requirements

**System Requirements:**
- **OS:** Windows 10+, macOS 10.15+, or Linux
- **RAM:** 8GB minimum (16GB recommended for Ollama)
- **Disk:** 5GB free space (for Ollama models)
- **Docker:** Docker Desktop installed and running

**Python Dependencies** (handled by Docker):
```txt
fastapi
uvicorn[standard]
python-multipart
python-dotenv
ollama
pydantic[email]
```

---

## 🎨 UI Features

The frontend features a **cinematic glassmorphic design** with:

- 🌊 **Animated Background** - Breathing gradient effects
- 💎 **Frosted Glass** - Backdrop blur on all elements
- ✨ **Smooth Animations** - Cubic-bezier transitions
- 🎭 **Hover Effects** - Interactive button states
- 📱 **Responsive Design** - Mobile-friendly layout
- 🎬 **Shimmer Effects** - Flowing light animations

---

## 🔧 Development

### **Local Development (Without Docker):**

```bash
# Install dependencies
pip install -r requirements.txt

# Set up .env file
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# Start Ollama
ollama serve

# Run backend
cd backend
python main.py

# Open frontend/index.html in browser
```

### **Making Changes:**

```bash
# Edit code
nano backend/main.py

# Rebuild and restart
docker-compose up -d --build

# View logs
docker-compose logs -f
```

---

## 📝 Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SENDER_EMAIL` | ✅ Yes | Gmail address | `john@gmail.com` |
| `SENDER_APP_PASSWORD` | ✅ Yes | Gmail app password | `abcd efgh ijkl mnop` |
| `OLLAMA_HOST` | ❌ No | Ollama server URL | `http://host.docker.internal:11434` |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **Ollama** - Local LLM inference
- **Mistral AI** - Powerful language model
- **Docker** - Containerization platform

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review Docker logs: `docker-compose logs -f`
3. Verify Ollama is running: `ollama serve`
4. Check `.env` configuration

---

## 🎯 Quick Command Reference

```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild after changes
docker-compose up -d --build

# Check status
docker ps

# Access container
docker exec -it smartmail bash

# Start Ollama
ollama serve

# Check Ollama models
ollama list
```

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---
