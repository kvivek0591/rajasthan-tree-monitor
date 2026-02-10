# 🚀 Deployment Guide

## Rajasthan Green Cover Monitoring - Cloud Deployment Options

---

## 🎯 Quick Comparison

| Platform | Difficulty | Cost | Best For | SSL Issues? |
|----------|-----------|------|----------|-------------|
| **Streamlit Cloud** | ⭐ Easy | Free | Dashboard | ❌ No |
| **Heroku** | ⭐⭐ Medium | $7/mo | Full app | ❌ No |
| **Railway** | ⭐⭐ Medium | Pay-as-go | Full app | ❌ No |
| **Google Cloud Run** | ⭐⭐⭐ Hard | Pay-as-go | Production | ❌ No |
| **DigitalOcean** | ⭐⭐⭐ Hard | $5/mo | Full control | ❌ No |
| **Vercel** | ❌ Not suitable | N/A | Frontend only | ❌ No (but won't work) |

---

## ✅ Option 1: Streamlit Cloud (Recommended)

### **Perfect For:**
- Quick deployment
- Free tier
- Built for Streamlit apps
- No server management

### **Limitations:**
- Public by default (can add password)
- Shared resources
- Community tier: 1GB RAM

### **Deployment Steps:**

#### **1. Prepare Repository**

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor

# Create GitHub repository
git init
git add .
git commit -m "Initial commit - Rajasthan Green Cover Monitoring"

# Push to GitHub (create repo first at github.com)
git remote add origin https://github.com/YOUR_USERNAME/rajasthan-tree-monitor.git
git branch -M main
git push -u origin main
```

#### **2. Create Streamlit Cloud Account**

1. Go to: https://streamlit.io/cloud
2. Sign up with GitHub
3. Click "New app"

#### **3. Configure Deployment**

- **Repository:** YOUR_USERNAME/rajasthan-tree-monitor
- **Branch:** main
- **Main file path:** frontend/app.py
- **Python version:** 3.11

#### **4. Add Secrets**

In Streamlit Cloud dashboard → App settings → Secrets:

```toml
# Add Earth Engine credentials here after authentication
# (Will guide you through this after deployment)
```

#### **5. Deploy**

Click "Deploy!" - Takes ~5 minutes

---

## ✅ Option 2: Heroku (Full Application)

### **Perfect For:**
- Production deployment
- Full control over environment
- Easy scaling

### **Cost:** $7/month (Eco plan)

### **Deployment Steps:**

#### **1. Install Heroku CLI**

```bash
brew tap heroku/brew && brew install heroku
```

#### **2. Create Heroku App**

```bash
cd rajasthan-tree-monitor

heroku login
heroku create rajasthan-tree-monitor

# Add Python buildpack
heroku buildpacks:add heroku/python
```

#### **3. Create Procfile**

Create `Procfile`:
```
web: streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0
```

#### **4. Create runtime.txt**

Create `runtime.txt`:
```
python-3.11.3
```

#### **5. Deploy**

```bash
git add .
git commit -m "Heroku deployment"
git push heroku main

heroku open
```

---

## ✅ Option 3: Railway (Modern Alternative)

### **Perfect For:**
- Modern deployment experience
- Pay-as-you-go pricing
- Simple setup

### **Cost:** ~$5-10/month (usage-based)

### **Deployment Steps:**

#### **1. Sign Up**

Go to: https://railway.app

#### **2. New Project**

- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository

#### **3. Configure**

Railway auto-detects Python and Streamlit

Add start command:
```bash
streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0
```

#### **4. Deploy**

Railway automatically deploys on git push

---

## ✅ Option 4: Docker + Cloud Run (Production)

### **Perfect For:**
- High availability
- Scalability
- Production workloads

### **Cost:** Pay-as-you-go (very cheap for low traffic)

### **Deployment Steps:**

#### **1. Create Dockerfile**

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### **2. Create .dockerignore**

```
venv/
__pycache__/
*.pyc
.env
data/*.json
.git/
```

#### **3. Build and Test Locally**

```bash
docker build -t rajasthan-monitor .
docker run -p 8501:8501 rajasthan-monitor
```

#### **4. Deploy to Google Cloud Run**

```bash
# Install gcloud CLI
brew install --cask google-cloud-sdk

# Authenticate
gcloud auth login

# Create project
gcloud projects create rajasthan-monitor

# Enable Cloud Run
gcloud services enable run.googleapis.com

# Build and deploy
gcloud builds submit --tag gcr.io/rajasthan-monitor/app
gcloud run deploy --image gcr.io/rajasthan-monitor/app --platform managed
```

---

## 🔐 Earth Engine Authentication for Cloud

### **Challenge:**
Earth Engine authentication requires interactive OAuth flow

### **Solutions:**

#### **Option A: Service Account** (Recommended for Production)

1. Create service account in Google Cloud Console
2. Download JSON key
3. Store as environment variable/secret
4. Initialize Earth Engine with service account:

```python
import ee
import json

# Load service account credentials
credentials = ee.ServiceAccountCredentials(
    email='YOUR_SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com',
    key_data=json.loads(os.environ['EE_SERVICE_ACCOUNT_KEY'])
)

# Initialize
ee.Initialize(credentials)
```

#### **Option B: Pre-authenticated Credentials**

1. Authenticate locally first
2. Export credentials
3. Upload as secrets to cloud platform
4. Load on app startup

---

## 📝 Environment Variables Needed

For any cloud deployment, set these:

```bash
# Required
EARTHENGINE_CREDENTIALS=<credentials_json>

# Optional
VEGETATION_LOSS_THRESHOLD=5
CLOUD_COVER_THRESHOLD=20
ANALYSIS_INTERVAL_DAYS=7
```

---

## 🔒 Security Considerations

### **1. Earth Engine Credentials**
- Never commit credentials to git
- Use platform secrets/environment variables
- Rotate periodically

### **2. API Keys**
- Store in environment variables
- Use platform secret management

### **3. Access Control**
- Add authentication to dashboard (Streamlit auth)
- Use environment-based configs
- Whitelist IP addresses if needed

---

## 📊 Deployment Checklist

### **Before Deployment:**
- [ ] Remove hardcoded secrets
- [ ] Add .env.example
- [ ] Create .gitignore
- [ ] Test locally with Docker
- [ ] Update requirements.txt
- [ ] Add README deployment section

### **During Deployment:**
- [ ] Set environment variables
- [ ] Configure secrets
- [ ] Set up Earth Engine credentials
- [ ] Test health endpoint
- [ ] Verify data persistence

### **After Deployment:**
- [ ] Test all features
- [ ] Run sample analysis
- [ ] Check logs
- [ ] Set up monitoring
- [ ] Document deployment URL

---

## 🚀 Quick Start Commands

### **Streamlit Cloud:**
```bash
# Push to GitHub
git init && git add . && git commit -m "Deploy"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main

# Then deploy via streamlit.io/cloud
```

### **Heroku:**
```bash
heroku create rajasthan-monitor
git push heroku main
heroku open
```

### **Railway:**
```bash
# Just connect GitHub repo via Railway dashboard
# Auto-deploys on push
```

### **Docker (Local Test):**
```bash
docker build -t rajasthan-monitor .
docker run -p 8501:8501 rajasthan-monitor
# Visit localhost:8501
```

---

## 💰 Cost Estimates

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| Streamlit Cloud | **Free** | Community tier |
| Railway | $5-10 | Usage-based |
| Heroku | $7 | Eco dyno |
| Google Cloud Run | $1-5 | Very low traffic |
| DigitalOcean | $5 | Droplet |

---

## 🎯 Recommended Path

### **For Quick Demo:**
→ **Streamlit Cloud** (Free, 10 minutes)

### **For Production:**
→ **Railway** or **Heroku** ($5-7/month, stable)

### **For Scale:**
→ **Google Cloud Run** (Pay-as-go, auto-scaling)

---

## ❌ Why NOT Vercel

### **Vercel is Great For:**
- ✅ Next.js / React apps
- ✅ Static sites
- ✅ Quick API routes (< 10s execution)

### **Vercel is BAD For:**
- ❌ Long-running processes (our analysis: 2-3 min)
- ❌ Heavy Python applications
- ❌ Streamlit apps
- ❌ Data processing workloads

### **Vercel Limitations:**
- Execution timeout: 10s (hobby), 60s (pro)
- Our analysis needs: 120-180s
- Limited Python support
- Not designed for Streamlit

---

## 🆘 Troubleshooting Deployment

### **Issue: "Module not found"**
```bash
# Ensure requirements.txt is complete
pip freeze > requirements.txt
```

### **Issue: "Port binding error"**
```bash
# Use platform's PORT environment variable
streamlit run app.py --server.port=$PORT
```

### **Issue: "Earth Engine not authenticated"**
- Set up service account credentials
- Or use pre-authenticated tokens in secrets

### **Issue: "Memory limit exceeded"**
- Upgrade to higher tier plan
- Optimize data processing
- Use Earth Engine server-side processing

---

## 📞 Need Help?

- **Streamlit Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **Heroku Docs:** https://devcenter.heroku.com/categories/python-support
- **Railway Docs:** https://docs.railway.app
- **Earth Engine Service Account:** https://developers.google.com/earth-engine/guides/service_account

---

## ✅ SSL Certificate Issues?

**Short Answer:** No SSL issues on any cloud platform

**Why:**
- Cloud platforms have proper SSL certificates
- Production Python environments are configured correctly
- HTTPS is handled by the platform
- Your local macOS SSL issue won't occur

---

**Ready to deploy?** Start with **Streamlit Cloud** for the easiest experience!
