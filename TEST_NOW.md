# 🧪 TEST THE APP NOW - Quick Commands

## ✅ Everything is Ready to Test!

---

## 🎯 Three Ways to Test (Choose One)

### 1️⃣ **Quick Demo Test** (10 seconds, no auth needed)

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate
python demo_mode.py
```

**Shows:**
- ✅ Complete analysis output
- ✅ NDVI calculations
- ✅ Change detection
- ✅ Alert system
- ✅ Data export

**Perfect for:** Seeing how it works instantly

---

### 2️⃣ **Visual Dashboard Test** (1 minute, no auth needed)

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate
streamlit run frontend/app.py
```

**Opens:** http://localhost:8501 in your browser

**Shows:**
- 📊 Interactive charts
- 📈 Trend graphs
- 🗺️ District metrics
- ⚠️ Alerts
- 📥 Export options

**Perfect for:** Exploring the interface

---

### 3️⃣ **Real Satellite Data Test** (5 minutes, auth required)

**Step 1:** Authenticate (one-time)
```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate
earthengine authenticate
```
(Opens browser → Sign in → Done)

**Step 2:** Run analysis
```bash
python backend/cli.py --quick
```

**Gets:**
- 🛰️ Real Sentinel-2 satellite data
- 📊 Actual vegetation analysis
- 🌳 Real NDVI values for Rajasthan
- ⚠️ Actual change detection

**Perfect for:** Production use

---

## 🚀 Recommended: Start with Option 1

**Copy and paste this:**

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor && source venv/bin/activate && python demo_mode.py
```

**Expected output:**
```
📍 Jodhpur District
   Mean NDVI: 0.4066
   NDVI Change: -0.0585 (-12.58%)
   ⚠️ ALERT: 12.59% vegetation change detected!
   Vegetation Loss Area: 154.17 hectares

✓ Demo data saved to: data/demo_analysis_20260210_155403.json
```

---

## 📊 Then View in Dashboard

**Copy and paste this:**

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor && source venv/bin/activate && streamlit run frontend/app.py
```

**Your browser will open showing:**
- Interactive gauges
- Charts and graphs
- District comparison
- Alert notifications

Press **Ctrl+C** in terminal to stop the dashboard

---

## 🎯 What Each Test Shows

| Test | Time | Auth? | Shows |
|------|------|-------|-------|
| **Demo Mode** | 10 sec | ❌ | Analysis output & alerts |
| **Dashboard** | 1 min | ❌ | Visual interface with charts |
| **Real Data** | 5 min | ✅ | Actual satellite analysis |

---

## ✅ Demo Data Already Created

A demo analysis file has been generated:
- **Location:** `data/demo_analysis_20260210_155403.json`
- **Contains:** Jodhpur and Bikaner analysis
- **Includes:** NDVI values, changes, alerts

**You can view this in the dashboard right now!**

---

## 🎓 What You'll Learn

### From Demo Mode:
- How NDVI values look (0.15-0.6 for Rajasthan)
- Change detection logic (-12% triggers alert)
- Output format (console + JSON)
- Alert system (>5% change = warning)

### From Dashboard:
- Visual interface and charts
- Interactive controls
- Trend analysis
- Export capabilities

### From Real Data:
- Actual satellite imagery
- Current vegetation state
- Real deforestation detection
- Production workflow

---

## 💡 Quick Start Command

**Just copy this entire block and paste in terminal:**

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate
echo "🧪 Running Demo Test..."
python demo_mode.py
echo ""
echo "✅ Demo complete! Now launching dashboard..."
echo "Press Ctrl+C to stop the dashboard when done"
sleep 3
streamlit run frontend/app.py
```

This will:
1. Run demo analysis
2. Show results
3. Launch dashboard automatically
4. Display data visually

---

## 📁 Files Created During Testing

After testing, you'll have:

```
data/
├── demo_analysis_20260210_155403.json  ← Demo data (already exists!)

And after real analysis:
├── analysis_20260210_160530.json       ← Real satellite data
├── analysis_20260217_093015.json       ← Next week's data
└── ...                                  ← Historical data
```

---

## 🔍 Verify Installation

Before testing, verify everything is installed:

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate
python test_setup.py
```

Should show:
```
✅ All packages installed successfully!
```

---

## 🆘 If Something Goes Wrong

### Dashboard won't start?
```bash
# Kill any process on port 8501
lsof -ti:8501 | xargs kill -9

# Try again
streamlit run frontend/app.py
```

### Python command not found?
```bash
# Make sure virtual environment is activated
source venv/bin/activate
```

### Import errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📊 Expected Results

### Demo Mode Output:
```
📍 Jodhpur District
   NDVI: 0.40-0.50 range (realistic for semi-arid)
   Change: -5% to -15% (demonstrates alerts)
   Area: 50-200 hectares loss

📍 Bikaner District
   NDVI: 0.35-0.45 range (realistic for arid)
   Similar analysis structure
```

### Dashboard View:
- Gauges showing NDVI (0-1 scale)
- Bar charts for changes
- Line graphs for trends
- Color-coded alerts (red = loss, green = stable)

---

## 🎯 After Testing

Once you've tested and verified:

1. **For development/learning:**
   - Keep using demo mode
   - Experiment with parameters
   - Explore dashboard features

2. **For production use:**
   - Authenticate Earth Engine
   - Run real analysis weekly
   - Monitor actual vegetation changes

---

## 📚 More Information

- **Full testing guide:** `TESTING_GUIDE.md`
- **Setup help:** `SETUP_COMPLETE.md`
- **Usage guide:** `QUICKSTART.md`
- **Technical details:** `TECHNICAL_DETAILS.md`

---

## 🚀 Ready? Run This Now!

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate
python demo_mode.py
```

**Takes 10 seconds. Shows complete working system.** ✅

---

**Questions? Check TESTING_GUIDE.md for detailed explanations!**
