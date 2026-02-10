# 🧪 Complete Testing Guide

## How to Test the Rajasthan Green Cover Monitoring App

---

## Quick Reference

| Test Type | Auth Needed? | Time | Command |
|-----------|--------------|------|---------|
| **Demo Mode** | ❌ No | 10 sec | `python demo_mode.py` |
| **Component Test** | ❌ No | 30 sec | `python test_setup.py` |
| **Web Dashboard** | ❌ No* | 1 min | `streamlit run frontend/app.py` |
| **Real Analysis** | ✅ Yes | 3 min | `python backend/cli.py --quick` |

*Dashboard works without auth but shows demo data only

---

## 🎯 Testing Options

### Option 1: Demo Mode (No Authentication - Recommended First Test)

**Best for:** Immediate testing without setup

```bash
cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate
python demo_mode.py
```

**What it does:**
- ✅ Generates realistic simulated data
- ✅ Shows complete analysis output
- ✅ Demonstrates alert system
- ✅ Creates JSON files in `data/` folder
- ✅ Tests all calculations and formatting

**Output Example:**
```
📍 Jodhpur District
   Mean NDVI: 0.4066
   NDVI Change: -0.0585 (-12.58%)
   ⚠️ ALERT: 12.59% vegetation change detected!
   Vegetation Loss Area: 154.17 hectares
```

**Time:** 10 seconds

---

### Option 2: Component Testing (No Authentication)

**Best for:** Verifying installation

```bash
source venv/bin/activate
python test_setup.py
```

**What it tests:**
- ✅ All Python packages imported correctly
- ✅ Configuration files loaded
- ✅ Earth Engine API available
- ✅ Project structure valid

**Output:**
```
✓ Earth Engine API - OK
✓ NumPy - OK
✓ Pandas - OK
✓ Matplotlib - OK
✓ Streamlit - OK
[... 10 packages total ...]

Results: 10 passed, 0 failed
✅ All packages installed successfully!
```

**Time:** 30 seconds

---

### Option 3: Web Dashboard Test (No Auth for Demo Data)

**Best for:** Visual interface testing

```bash
source venv/bin/activate
streamlit run frontend/app.py
```

**What happens:**
- Opens browser at `http://localhost:8501`
- Shows dashboard interface
- If no auth: Displays demo/historical data
- If authenticated: Can run live analysis

**Features to test:**
- 📊 Interactive charts and gauges
- 📈 Historical trend graphs
- 🗺️ District selection
- 📥 Data export
- ⚠️ Alert notifications

**Time:** 1 minute to launch, explore as long as you want

---

### Option 4: Command-Line Quick Check (Requires Authentication)

**Best for:** Fast real data analysis

**First, authenticate:**
```bash
source venv/bin/activate
earthengine authenticate
```
(Opens browser, sign in with Google, grant access)

**Then run:**
```bash
python backend/cli.py --quick
```

**What it does:**
- ✅ Fetches real Sentinel-2 satellite data
- ✅ Analyzes Jodhpur and Bikaner
- ✅ Calculates actual NDVI values
- ✅ Detects real vegetation changes
- ✅ Generates alerts if needed

**Output:**
```
📍 Jodhpur District:
   NDVI: 0.4523 (-5.17%)
   ⚠️ ALERT: 5.17% vegetation loss!

📍 Bikaner District:
   NDVI: 0.3812 (-2.34%)
   ✓ No alerts
```

**Time:** 2-3 minutes (downloads satellite data)

---

### Option 5: Detailed Analysis (Requires Authentication)

**Best for:** Complete analysis with all metrics

```bash
source venv/bin/activate
python backend/vegetation_monitor.py
```

**What it does:**
- ✅ Full statistical analysis
- ✅ All NDVI metrics (mean, median, std, percentiles)
- ✅ Detailed change detection
- ✅ Area calculations
- ✅ Saves complete JSON output

**Output:**
```
📊 VEGETATION ANALYSIS SUMMARY - Jodhpur
============================================================
Current Week NDVI Statistics:
   Mean NDVI: 0.4523
   Median NDVI: 0.4612
   Std Dev: 0.1234
   10th Percentile: 0.3201
   90th Percentile: 0.6234

Week-over-Week Change:
   NDVI Change: -0.0234 (-5.17%)
   Min Change: -0.1234
   Max Change: +0.0567
   Vegetation Loss Area: 125.67 hectares

⚠️ 5.17% vegetation change detected!
============================================================
```

**Time:** 3-5 minutes

---

### Option 6: Jupyter Notebook (Interactive Testing)

**Best for:** Learning and experimentation

```bash
source venv/bin/activate
jupyter notebook notebooks/quick_analysis.ipynb
```

**What you can do:**
- Step-by-step analysis
- Modify parameters
- Create custom visualizations
- Experiment with data
- Save custom outputs

**Time:** As long as you want to explore

---

### Option 7: Complete Workflow Example (Requires Authentication)

**Best for:** Understanding the full pipeline

```bash
source venv/bin/activate
python examples/complete_workflow.py
```

**What it demonstrates:**
- Complete analysis flow
- Both districts
- Comparison logic
- Export process
- Recommendations based on results

**Time:** 5-7 minutes

---

## 🎯 Recommended Testing Sequence

### For First-Time Users (Without Auth)

**1. Component Test (30 sec)**
```bash
python test_setup.py
```
Verify: All packages work

**2. Demo Mode (10 sec)**
```bash
python demo_mode.py
```
See: How the system works

**3. Web Dashboard (1 min)**
```bash
streamlit run frontend/app.py
```
Explore: Visual interface with demo data

**Total: ~2 minutes**

---

### For Production Use (With Auth)

**1. Authenticate (one-time, 2 min)**
```bash
earthengine authenticate
```

**2. Quick Analysis (3 min)**
```bash
python backend/cli.py --quick
```

**3. Dashboard (ongoing)**
```bash
streamlit run frontend/app.py
```
Then click "Run Analysis" for live data

**Total: ~5 minutes initial setup**

---

## 📊 What to Check During Testing

### ✅ Demo Mode Checklist

- [ ] Script runs without errors
- [ ] Two districts analyzed (Jodhpur, Bikaner)
- [ ] NDVI values realistic (0.15 - 0.6 range)
- [ ] Change percentages calculated
- [ ] Alerts triggered (sometimes)
- [ ] JSON file created in `data/` folder
- [ ] Data format looks correct

### ✅ Dashboard Checklist

- [ ] Opens in browser at localhost:8501
- [ ] Shows district selection
- [ ] Displays NDVI gauges
- [ ] Shows metrics (current NDVI, change %)
- [ ] Historical trend charts appear
- [ ] Can switch between districts
- [ ] Responsive interface

### ✅ Real Analysis Checklist (After Auth)

- [ ] Authentication successful
- [ ] Satellite data downloads
- [ ] Analysis completes without errors
- [ ] Realistic NDVI values for Rajasthan
- [ ] Change detection works
- [ ] JSON files saved
- [ ] Alerts trigger when appropriate

---

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Earth Engine not initialized" (for real analysis)
```bash
earthengine authenticate
```

### Issue: Dashboard won't start
```bash
# Check if port 8501 is busy
lsof -ti:8501 | xargs kill -9

# Then restart
streamlit run frontend/app.py
```

### Issue: "No data available"
- **If using demo mode:** Check if `data/` folder has JSON files
- **If using real data:** Wait 2-3 days (cloud cover issue) or check Earth Engine status

---

## 🎓 Understanding the Output

### NDVI Values

| Range | Vegetation Type | Expected for Rajasthan |
|-------|----------------|------------------------|
| 0.8-1.0 | Very dense forest | Rare |
| 0.6-0.8 | Dense vegetation | Uncommon |
| 0.4-0.6 | Moderate vegetation | **Common** |
| 0.2-0.4 | Sparse vegetation | **Very common** |
| 0.0-0.2 | Bare soil/sand | Common |

### Change Detection

- **>5% loss:** Significant (triggers alert)
- **2-5% loss:** Moderate (monitor)
- **<2% change:** Normal variation
- **Positive change:** Growth/recovery

### Area Metrics

- **Small change:** <10 hectares (local)
- **Moderate change:** 10-100 hectares (concerning)
- **Large change:** >100 hectares (investigate immediately)

---

## 📝 Test Results Template

After testing, record your results:

```
Date: ___________
Test Type: ___________

✓ Installation: [ ] Pass [ ] Fail
✓ Demo Mode: [ ] Pass [ ] Fail
✓ Dashboard: [ ] Pass [ ] Fail
✓ Real Analysis: [ ] Pass [ ] Fail [ ] Not tested

Notes:
_________________________________
_________________________________

Issues Found:
_________________________________
_________________________________
```

---

## 🚀 Next Steps After Testing

### If Demo Mode Works ✅
- System is installed correctly
- Ready for Earth Engine authentication
- Can explore dashboard with demo data

### If Real Analysis Works ✅
- Full system operational
- Can start weekly monitoring
- Schedule automated runs

### If Tests Fail ❌
- Check `QUICKSTART.md` troubleshooting
- Verify Python version (3.8+)
- Re-run `pip install -r requirements.txt`
- Check error messages

---

## 💡 Pro Tips

1. **Start with demo mode** - No auth needed, instant results
2. **Use dashboard for visualization** - Easier than command line
3. **Save your results** - JSON files in `data/` folder
4. **Test weekly** - Verify system stays working
5. **Compare seasons** - NDVI varies naturally

---

## 📞 Need Help?

- **Setup issues:** See `SETUP_COMPLETE.md`
- **Usage questions:** See `QUICKSTART.md`
- **Technical details:** See `TECHNICAL_DETAILS.md`
- **Feature overview:** See `README.md`

---

**Ready to test?** Start with demo mode:

```bash
cd rajasthan-tree-monitor
source venv/bin/activate
python demo_mode.py
```

Then explore the dashboard:
```bash
streamlit run frontend/app.py
```

**Happy testing!** 🧪
