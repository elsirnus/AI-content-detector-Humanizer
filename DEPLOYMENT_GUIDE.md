# 🚀 Streamlit Cloud Deployment Guide

## Step 1: Prepare Your Repository (Already Done! ✅)

We've already created:
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.github/workflows/deploy.yml` - Auto-deployment workflow
- ✅ `requirements.txt` - Optimized dependencies

## Step 2: Push to GitHub

```bash
cd /workspaces/AI-content-detector-Humanizer
git add .
git commit -m "feat: add Streamlit Cloud deployment config"
git push origin main
```

## Step 3: Deploy to Streamlit Cloud

### Option A: Automatic (Recommended)
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repository
4. Set to deploy from `main` branch
5. Set main file to `main.py`
6. Click "Deploy"

### Option B: Using Streamlit CLI
```bash
streamlit deploy
```

## Step 4: Configure Secrets (if needed)

If your app uses API keys or environment variables:

1. In Streamlit Cloud dashboard, go to your app settings
2. Click "Secrets"
3. Add your secrets in TOML format:
```toml
API_KEY = "your-api-key-here"
DATABASE_URL = "your-db-url"
```

Then access in code:
```python
import streamlit as st
api_key = st.secrets["API_KEY"]
```

## Step 5: Monitor & Update

- **Auto-updates**: Every push to `main` triggers deployment
- **View logs**: In Streamlit Cloud dashboard
- **Manage app**: https://share.streamlit.io

---

## 📊 Your App Details

**App URL Pattern:**
```
https://your-username-projectname.streamlit.app
```

**Features Supported:**
- ✅ PDF uploads (max 200MB per file)
- ✅ Text analysis
- ✅ Batch processing
- ✅ Document comparison
- ✅ Statistics dashboard
- ✅ CSV/Excel exports

---

## 🔧 Troubleshooting

### App won't deploy
- Check `requirements.txt` syntax
- Ensure no local imports
- Verify all imports are in requirements.txt

### App loads but features missing
- Check `.streamlit/config.toml`
- Verify page imports in `main.py`
- Check for missing dependencies

### Slow performance
- Optimize PDF processing
- Use caching decorators
- Stream large outputs

---

## 💡 Next Steps

1. Push your code to GitHub
2. Deploy to Streamlit Cloud
3. Share your app URL with users
4. Monitor performance in dashboard
5. Make updates by pushing to main branch

**Need help?** → https://docs.streamlit.io/deploy/streamlit-cloud
