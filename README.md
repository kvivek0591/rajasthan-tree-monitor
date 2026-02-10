# 🌳 Rajasthan Green Cover Monitoring System

**Monitor week-over-week vegetation changes in Jodhpur and Bikaner districts using free satellite imagery**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Earth Engine](https://img.shields.io/badge/Google-Earth%20Engine-green.svg)](https://earthengine.google.com/)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Documentation](#-documentation)
- [Technical Stack](#-technical-stack)
- [How It Works](#-how-it-works)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)

---

## 🚨 Problem Statement

Villages in Rajasthan are facing **illegal tree cutting** for solar plant construction:

- **Issue**: Government incentivizes solar plants → Builders buy land → Trees are cut
- **Challenge**: No official record of tree count in areas
- **Tactic**: Trees cut at night to hide evidence
- **Impact**: Communities can't prove trees existed

**Result**: Environmental damage with no accountability

---

## 💡 Solution

This system provides **scientific evidence** of vegetation changes using:

✅ **Free satellite imagery** (Sentinel-2, 10m resolution)
✅ **Automated weekly monitoring** of green cover changes
✅ **Alerts** for significant vegetation loss (>5%)
✅ **Historical tracking** to prove changes over time
✅ **Quantifiable data** (hectares lost, NDVI metrics)

**Empowers communities** with data to:
- Prove trees existed before clearing
- Track illegal deforestation
- Report to authorities with evidence
- Monitor protected areas

---

## ✨ Features

### 🔍 Core Capabilities

- **Week-over-week change detection** using NDVI analysis
- **Two-district coverage**: Jodhpur and Bikaner
- **Automatic cloud filtering** for accurate results
- **Alert system** for significant vegetation loss
- **Historical trend analysis** over months/years
- **Multiple interfaces**: CLI, Web Dashboard, Jupyter Notebook

### 📊 Outputs

- 📈 **Vegetation metrics**: NDVI values, change percentages
- 🗺️ **Interactive maps**: Visual change detection
- 📁 **JSON exports**: Machine-readable data
- 📋 **Reports**: Summary statistics and alerts
- 📉 **Trend charts**: Historical visualization

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Internet connection
- Google account

### Installation (5 minutes)

```bash
# 1. Clone or navigate to the directory
cd rajasthan-tree-monitor

# 2. Run the automated setup script
./setup.sh
```

The setup script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Authenticate with Google Earth Engine
- ✅ Create necessary directories

### First Run

```bash
# Activate environment
source venv/bin/activate

# Run quick analysis
python backend/cli.py --quick

# Or start web dashboard
streamlit run frontend/app.py
```

**📖 See [QUICKSTART.md](QUICKSTART.md) for detailed instructions**

---

## 🎯 Usage

### Option 1: Command Line Interface (Fastest)

```bash
# Quick check all districts
python backend/cli.py --quick

# Detailed analysis for one district
python backend/cli.py --detailed Jodhpur

# Compare both districts
python backend/cli.py --compare

# View history
python backend/cli.py --history
```

### Option 2: Web Dashboard (Recommended)

```bash
streamlit run frontend/app.py
```

Features:
- 📊 Interactive charts and gauges
- 📈 Historical trends
- 🗺️ Visual maps
- ⚠️ Alert notifications
- 📥 Export capabilities

**Access:** Opens at `http://localhost:8501`

### Option 3: Python Script

```bash
# Run full analysis
python backend/vegetation_monitor.py

# Run example workflow
python examples/complete_workflow.py
```

### Option 4: Jupyter Notebook

```bash
jupyter notebook notebooks/quick_analysis.ipynb
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Step-by-step beginner guide |
| [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) | In-depth technical documentation |
| [README.md](README.md) | This file - overview and usage |

---

## 🛠️ Technical Stack

### Data & Analysis

- **Satellite Data**: Sentinel-2 (ESA Copernicus)
- **Resolution**: 10 meters per pixel
- **Update Frequency**: 5 days
- **Coverage**: Global (includes Rajasthan)
- **Cost**: Free and open access

### Backend

- **Python 3.8+**
- **Google Earth Engine API**: Satellite data access
- **NumPy, Pandas**: Data processing
- **GeoPandas**: Geospatial operations

### Frontend

- **Streamlit**: Web dashboard
- **Plotly**: Interactive visualizations
- **Folium**: Map rendering
- **Jupyter**: Notebook interface

---

## 🔬 How It Works

### 1. NDVI Calculation

**NDVI** = (NIR - Red) / (NIR + Red)

- **Healthy vegetation**: High NDVI (0.6-1.0)
- **Sparse vegetation**: Medium NDVI (0.2-0.5)
- **Bare soil**: Low NDVI (0.0-0.2)

### 2. Change Detection

```
NDVI_change = NDVI_current_week - NDVI_previous_week
```

- **Negative change**: Vegetation loss (potential tree cutting)
- **Positive change**: Vegetation gain (growth/recovery)

### 3. Alert System

```
Change_percentage = (NDVI_change / NDVI_previous) × 100%

If |Change_percentage| > 5%:
    TRIGGER ALERT
```

### 4. Area Calculation

```
Area (hectares) = Changed_pixels × 100m² / 10,000
```

**📖 See [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) for complete methodology**

---

## 🖼️ Screenshots

### Web Dashboard
*(Coming soon - add screenshots after running)*

- Main dashboard with metrics
- Historical trend charts
- Alert notifications
- District comparison

---

## 🗺️ District Coverage

### Jodhpur District
- **Area**: ~22,850 km²
- **Center**: 26.28°N, 73.02°E
- **Climate**: Semi-arid
- **Typical NDVI**: 0.2 - 0.5

### Bikaner District
- **Area**: ~27,244 km²
- **Center**: 28.01°N, 73.31°E
- **Climate**: Arid
- **Typical NDVI**: 0.15 - 0.45

---

## 📊 Output Examples

### Console Output

```
📍 Jodhpur District:
   NDVI: 0.4523 (-5.17%)
   ⚠️ ALERT: 5.17% vegetation loss!

📍 Bikaner District:
   NDVI: 0.3812 (-2.34%)
   ✓ No alerts
```

### JSON Export

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

**Weekly Monitoring Routine:**

1. **Monday Morning**: Run analysis
   ```bash
   python backend/vegetation_monitor.py
   ```

2. **Check Results**: Review console output

3. **If Alert Triggered**:
   - Open web dashboard for details
   - Check specific areas on map
   - Export report with evidence
   - Share with authorities/community

4. **Track Trends**: Compare with previous weeks

---

## 🆘 Troubleshooting

### Common Issues

**"Earth Engine not initialized"**
```bash
earthengine authenticate
```

**"No data available"**
- Possible cloud cover issue
- Wait 2-3 days for clearer imagery
- Check [Earth Engine Status](https://status.earthengine.google.com/)

**"Module not found"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🤝 Contributing

This is a community tool. Contributions welcome:

- 🐛 Report bugs via issues
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests

---

## 📜 License

MIT License - Free to use, modify, and distribute

---

## 🙏 Acknowledgments

- **European Space Agency (ESA)**: Sentinel-2 satellite data
- **Google Earth Engine**: Data processing platform
- **Rajasthan Communities**: For highlighting this critical issue

---

## 📞 Support

- **Technical Issues**: See [Troubleshooting](#-troubleshooting)
- **Earth Engine Help**: [Forum](https://groups.google.com/g/google-earth-engine-developers)
- **Documentation**: [QUICKSTART.md](QUICKSTART.md) | [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md)

---

## 🎯 Impact

**This tool helps:**
- 🌳 Protect trees from illegal cutting
- 📊 Provide scientific evidence
- ⚖️ Hold violators accountable
- 🌍 Support environmental conservation

**Your monitoring makes a difference!**

---

<div align="center">

**🌳 Together we can protect Rajasthan's trees 🌳**

Made with ❤️ for environmental conservation

</div>
