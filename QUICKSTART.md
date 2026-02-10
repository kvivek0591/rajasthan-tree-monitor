# 🚀 Quick Start Guide

## Rajasthan Green Cover Monitoring System

This tool helps monitor vegetation changes in Jodhpur and Bikaner districts using free satellite imagery.

---

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection (for satellite data)
- Google account (for Earth Engine)

---

## ⚡ Installation (5 minutes)

### Step 1: Run Setup Script

```bash
cd rajasthan-tree-monitor
./setup.sh
```

This will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Authenticate with Google Earth Engine
- ✅ Create necessary directories

### Step 2: Activate Environment

```bash
source venv/bin/activate
```

---

## 🎯 Usage Options

### Option 1: Quick Command Line Analysis (Fastest)

```bash
python backend/vegetation_monitor.py
```

**Output:**
- Console report with NDVI statistics
- Week-over-week change analysis
- Alerts for significant vegetation loss
- JSON file saved to `data/` folder

**Time:** ~2-3 minutes per district

---

### Option 2: Interactive Web Dashboard (Recommended)

```bash
streamlit run frontend/app.py
```

**Features:**
- 📊 Visual charts and graphs
- 📈 Historical trend analysis
- 🗺️ Interactive metrics
- ⚠️ Alert notifications
- 📥 Downloadable reports

**Access:** Opens automatically in your browser at `http://localhost:8501`

---

### Option 3: Jupyter Notebook (For Data Scientists)

```bash
jupyter notebook notebooks/quick_analysis.ipynb
```

**Features:**
- Step-by-step analysis
- Custom visualizations
- Data exploration
- Export capabilities

---

## 📊 Understanding the Results

### NDVI (Normalized Difference Vegetation Index)

NDVI measures vegetation health on a scale from -1 to 1:

| NDVI Range | Vegetation Type | Color |
|------------|----------------|-------|
| 0.0 - 0.2  | No/Sparse     | Red   |
| 0.2 - 0.4  | Sparse         | Orange|
| 0.4 - 0.6  | Moderate       | Yellow|
| 0.6 - 0.8  | Dense          | Light Green|
| 0.8 - 1.0  | Very Dense     | Dark Green|

### Week-over-Week Change

- **Negative change**: Vegetation loss (potential tree cutting)
- **Positive change**: Vegetation increase (growth/recovery)
- **Alert threshold**: >5% change triggers notification

### Key Metrics

1. **Mean NDVI**: Average vegetation across the district
2. **Vegetation Loss Area**: Hectares where significant loss occurred
3. **Change Percentage**: Week-over-week difference

---

## 🚨 Alert System

The system automatically detects:

- ⚠️ **Significant vegetation loss** (>5% decrease)
- 📍 **Area affected** (in hectares)
- 📅 **Time period** of change
- 📊 **Quantified impact**

---

## 📁 Output Files

Results are saved in `data/` folder:

```
data/
├── analysis_20260210_151230.json  # Latest analysis
├── analysis_20260203_142015.json  # Previous week
└── analysis_20260127_135500.json  # Historical
```

**JSON Format:**
```json
{
  "Jodhpur": {
    "current_week": {
      "ndvi_mean": 0.4523,
      "ndvi_median": 0.4612
    },
    "change": {
      "ndvi_change_mean": -0.0234,
      "vegetation_loss_area_hectares": 125.67
    },
    "alert": {
      "triggered": true,
      "change_percentage": -5.17
    }
  }
}
```

---

## 🔄 Recommended Workflow

### Weekly Monitoring Routine

**Every Monday Morning:**

1. Run analysis:
   ```bash
   python backend/vegetation_monitor.py
   ```

2. Check for alerts in the output

3. If alert triggered:
   - Open web dashboard for details
   - Export report
   - Share with relevant authorities

4. Document findings:
   - Note any suspicious patterns
   - Compare with ground reports
   - Track specific areas

---

## 🗺️ District Coverage

### Jodhpur District
- **Area**: ~22,850 km²
- **Coordinates**: 26.28°N, 73.02°E
- **Typical NDVI**: 0.2 - 0.5 (semi-arid region)

### Bikaner District
- **Area**: ~27,244 km²
- **Coordinates**: 28.01°N, 73.31°E
- **Typical NDVI**: 0.15 - 0.45 (arid region)

---

## 💡 Tips for Best Results

1. **Cloud Cover**: Analysis automatically filters out cloudy images
2. **Seasonal Variation**: NDVI naturally varies with seasons
   - Summer (Apr-Jun): Lower NDVI (dry season)
   - Monsoon (Jul-Sep): Higher NDVI (green season)
   - Winter (Dec-Feb): Moderate NDVI

3. **Comparing Results**: Always compare similar seasons
4. **Ground Truth**: Combine with local observations
5. **Regular Monitoring**: Run weekly for trend detection

---

## 🆘 Troubleshooting

### Issue: "Earth Engine not initialized"
**Solution:**
```bash
earthengine authenticate
```

### Issue: "No data available"
**Possible causes:**
- Heavy cloud cover in the region
- Satellite data not yet available for recent dates
- Wait 2-3 days and retry

### Issue: "Module not found"
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📞 Support

For issues or questions:
1. Check `README.md` for detailed documentation
2. Review troubleshooting section above
3. Check Earth Engine status: https://status.earthengine.google.com/

---

## 🎯 Next Steps

1. ✅ Run your first analysis
2. ✅ Explore the web dashboard
3. ✅ Set up weekly monitoring routine
4. ✅ Share results with community leaders
5. ✅ Document evidence of illegal tree cutting

---

**Remember:** This tool provides scientific evidence of vegetation changes. Combined with ground observations, it can help protect Rajasthan's precious trees. 🌳
