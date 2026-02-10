# 🔬 Technical Details

## Rajasthan Green Cover Monitoring System - Technical Documentation

---

## 🛰️ Data Sources

### Sentinel-2 Satellite Imagery

**Provider:** European Space Agency (ESA) via Copernicus Programme

**Specifications:**
- **Resolution:** 10 meters per pixel
- **Revisit Time:** 5 days (with both satellites)
- **Bands Used:**
  - Band 4 (Red): 665 nm - vegetation absorption
  - Band 8 (NIR): 842 nm - vegetation reflection
- **Collection:** COPERNICUS/S2_SR_HARMONIZED (Surface Reflectance)
- **Cost:** Free and open access

**Coverage:**
- Global coverage between latitudes 56°S and 84°N
- Includes all of India/Rajasthan

---

## 📊 NDVI Calculation

### Formula

```
NDVI = (NIR - Red) / (NIR + Red)
```

Where:
- **NIR** = Near Infrared reflectance (Band 8)
- **Red** = Red reflectance (Band 4)

### Physical Basis

**Healthy Vegetation:**
- Absorbs red light (photosynthesis)
- Reflects near-infrared light (leaf structure)
- Result: High NDVI (0.6 - 1.0)

**Bare Soil/Dead Vegetation:**
- Similar reflectance in both bands
- Result: Low NDVI (0.0 - 0.2)

**Semi-arid Regions (Rajasthan):**
- Sparse vegetation with soil background
- Typical NDVI: 0.2 - 0.5

### NDVI Interpretation Table

| NDVI Range | Land Cover Type | Vegetation Density | Color Code |
|------------|----------------|-------------------|------------|
| < 0.0      | Water, clouds  | N/A               | Blue       |
| 0.0 - 0.1  | Bare rock/sand | None              | Brown      |
| 0.1 - 0.2  | Sparse vegetation | Very low       | Red        |
| 0.2 - 0.3  | Shrubs, grassland | Low            | Orange     |
| 0.3 - 0.4  | Sparse trees   | Moderate-low      | Yellow     |
| 0.4 - 0.6  | Moderate forest | Moderate         | Light Green|
| 0.6 - 0.8  | Dense forest   | High              | Green      |
| 0.8 - 1.0  | Very dense forest | Very high      | Dark Green |

---

## 🔍 Change Detection Methodology

### Temporal Comparison

**Process:**
1. Acquire imagery for two time periods (Week N and Week N-1)
2. Calculate NDVI for each period
3. Compute pixel-by-pixel difference: `NDVI_change = NDVI_current - NDVI_previous`

**Interpretation:**
- **Negative change (< -0.1):** Significant vegetation loss
- **Slight negative (-0.1 to 0):** Minor decrease/seasonal variation
- **Slight positive (0 to +0.1):** Minor increase/growth
- **Positive change (> +0.1):** Significant vegetation gain

### Statistical Analysis

**Metrics Calculated:**

1. **Mean NDVI:** Average vegetation across entire district
2. **Median NDVI:** Middle value (less affected by outliers)
3. **Standard Deviation:** Variability in vegetation
4. **Percentiles (10th, 50th, 90th):** Distribution analysis
5. **Change Statistics:**
   - Mean change
   - Minimum change (most loss)
   - Maximum change (most gain)
6. **Area Analysis:**
   - Total pixels with significant loss
   - Conversion to hectares

---

## 🚨 Alert System

### Threshold Logic

**Alert Triggered When:**
```python
change_percentage = (NDVI_change_mean / NDVI_previous_mean) * 100

if abs(change_percentage) > 5%:
    TRIGGER_ALERT
```

**Rationale:**
- 5% threshold filters out seasonal noise
- Detects significant land use changes
- Balances sensitivity vs false positives

### Alert Types

1. **Vegetation Loss Alert:**
   - Change < -5%
   - Indicates potential tree cutting, land clearing
   - Priority: HIGH

2. **Vegetation Gain Alert:**
   - Change > +5%
   - Indicates afforestation, recovery
   - Priority: LOW (informational)

---

## 📐 Spatial Resolution & Accuracy

### Pixel Size: 10m × 10m = 100 m²

**Tree Detection Capability:**
- **Single large tree:** May occupy multiple pixels (detectable)
- **Small trees:** May share pixels with ground (partially detectable)
- **Tree clusters:** Easily detectable as high NDVI zones

### Area Calculation

```
Area (hectares) = Number_of_pixels × 100 m² / 10,000
```

**Example:**
- 1,000 pixels changed = 100,000 m² = 10 hectares

### Accuracy Considerations

**Factors Affecting Accuracy:**
1. **Cloud Cover:** Filtered out (< 20% threshold)
2. **Atmospheric Conditions:** Corrected via surface reflectance product
3. **Soil Background:** Higher in sparse vegetation areas
4. **Shadow Effects:** From terrain/clouds
5. **Seasonal Variation:** Natural NDVI fluctuations

**Expected Accuracy:**
- Tree detection: 80-90% for trees > 5m height
- Change detection: 85-95% for changes > 1 hectare
- NDVI values: ±0.05 typical uncertainty

---

## 🗺️ Geographic Coverage

### District Boundaries (Bounding Boxes)

**Jodhpur District:**
```python
bbox = [72.8°E, 26.0°N, 73.5°E, 27.0°N]
approximate_area = 22,850 km²
center = [73.02°E, 26.28°N]
```

**Bikaner District:**
```python
bbox = [72.8°E, 27.5°N, 73.8°E, 28.5°N]
approximate_area = 27,244 km²
center = [73.31°E, 28.01°N]
```

### Coordinate System

- **CRS:** EPSG:4326 (WGS84 Geographic)
- **Units:** Decimal degrees
- **Projection:** Unprojected (lat/lon)

---

## 💾 Data Processing Pipeline

### Step-by-Step Flow

```
1. User Request
   ↓
2. Define Region of Interest (ROI)
   ↓
3. Query Sentinel-2 Image Collection
   - Filter by date range
   - Filter by cloud cover < 20%
   - Filter by geographic bounds
   ↓
4. Image Preprocessing
   - Select median composite (reduces clouds)
   - Clip to ROI
   ↓
5. Band Selection
   - Extract Band 4 (Red)
   - Extract Band 8 (NIR)
   ↓
6. NDVI Calculation
   - Apply formula: (NIR - Red) / (NIR + Red)
   ↓
7. Temporal Comparison
   - Load previous week's NDVI
   - Calculate difference
   ↓
8. Statistical Analysis
   - Compute mean, median, std, percentiles
   - Identify change areas
   - Calculate loss area
   ↓
9. Alert Evaluation
   - Check change percentage
   - Trigger alerts if threshold exceeded
   ↓
10. Output Generation
    - Console report
    - JSON export
    - Web visualization
```

### Computational Requirements

**Per District Analysis:**
- **Data Volume:** ~100-200 MB satellite imagery
- **Processing Time:** 2-3 minutes
- **Memory:** ~2 GB RAM
- **Storage:** ~10 MB per analysis (JSON output)

---

## 🔧 Technical Stack

### Backend

**Core:**
- **Language:** Python 3.8+
- **Earth Engine API:** earthengine-api
- **Authentication:** OAuth 2.0 via Google

**Data Processing:**
- **NumPy:** Numerical computations
- **Pandas:** Data manipulation
- **Geemap:** Earth Engine utilities

**Geospatial:**
- **GeoPandas:** Vector operations
- **Rasterio:** Raster operations
- **Shapely:** Geometric operations

### Frontend

**Web Dashboard:**
- **Framework:** Streamlit
- **Visualization:** Plotly, Matplotlib
- **Maps:** Folium (interactive)

**Notebook:**
- **Platform:** Jupyter
- **Kernel:** Python 3

---

## 🔒 Security & Privacy

### Data Access

- **Public Data Only:** All satellite imagery is publicly available
- **No Personal Data:** System does not collect user information
- **Authentication:** Required only for Earth Engine API access
- **Local Storage:** All results stored locally on user's machine

### API Quotas

**Google Earth Engine Free Tier:**
- 50,000 requests per day (per user)
- Sufficient for continuous monitoring

**Rate Limits:**
- Our usage: ~10-20 requests per analysis
- Can run analysis ~2,500+ times per day

---

## 📈 Performance Optimization

### Techniques Used

1. **Median Compositing:** Reduces cloud noise
2. **Bounding Box Filtering:** Limits data volume
3. **Cloud Cover Pre-filtering:** Skips unsuitable images
4. **Lazy Evaluation:** Earth Engine processes on-demand
5. **Reduced Scale:** 10m resolution (not native 10m bands used directly)

### Potential Improvements

1. **Caching:** Store intermediate results
2. **Parallel Processing:** Analyze districts concurrently
3. **Higher Resolution:** Use 10m directly (slower, more accurate)
4. **Additional Indices:** EVI, SAVI for better accuracy
5. **Machine Learning:** Train custom tree detection models

---

## 🌍 Alternative Approaches

### Other Satellite Sources

1. **Landsat 8/9:**
   - Resolution: 30m (lower)
   - Revisit: 16 days (longer)
   - Advantage: Longer historical archive

2. **Planet Labs:**
   - Resolution: 3m (higher)
   - Revisit: Daily
   - Disadvantage: Commercial (expensive)

3. **ISRO Cartosat/ResourceSat:**
   - India-specific
   - Various resolutions
   - Limited API access

### Other Vegetation Indices

1. **EVI (Enhanced Vegetation Index):**
   - Better for dense canopy
   - More complex calculation

2. **SAVI (Soil Adjusted VI):**
   - Better for sparse vegetation
   - Reduces soil background influence

3. **NDWI (Normalized Difference Water Index):**
   - Detects water stress
   - Complements NDVI

---

## 🔬 Validation & Ground Truth

### Recommended Validation Methods

1. **Field Surveys:**
   - GPS-tagged tree counts
   - Photo documentation
   - Compare with satellite results

2. **Drone Imagery:**
   - Higher resolution verification
   - 3D canopy structure
   - Targeted suspicious areas

3. **Historical Comparison:**
   - Compare with Google Earth historical imagery
   - Cross-reference with government records
   - Validate against known events

---

## 📚 References & Resources

### Academic Papers

1. Tucker, C.J. (1979). "Red and photographic infrared linear combinations for monitoring vegetation"
2. Rouse et al. (1974). "Monitoring vegetation systems in the Great Plains with ERTS"

### Documentation

- [Sentinel-2 User Guide](https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi)
- [Google Earth Engine Docs](https://developers.google.com/earth-engine)
- [NDVI Theory](https://earthobservatory.nasa.gov/features/MeasuringVegetation/measuring_vegetation_2.php)

### Tools

- [Earth Engine Code Editor](https://code.earthengine.google.com/)
- [Sentinel Hub EO Browser](https://apps.sentinel-hub.com/eo-browser/)

---

## 🛠️ Troubleshooting Common Issues

### Issue: Cloud Cover Affecting Results

**Problem:** High cloud cover in imagery
**Solutions:**
- Wait 5-10 days for clearer imagery
- Expand date range in query
- Use 3-week comparison instead of 1-week

### Issue: Seasonal Variations

**Problem:** Natural NDVI changes mistaken for deforestation
**Solutions:**
- Compare same-season data from different years
- Track long-term trends (months, not weeks)
- Adjust alert thresholds seasonally

### Issue: Mixed Pixels

**Problem:** Small trees in pixels with soil/buildings
**Solutions:**
- Focus on areas with consistent vegetation
- Use time-series analysis
- Combine with higher-resolution data

---

## 🚀 Future Enhancements

### Planned Features

1. **Automated Alerts:** Email/SMS notifications
2. **Mobile App:** Field data collection
3. **Historical Analysis:** Multi-year trends
4. **Heat Maps:** Geographic hotspots of change
5. **Report Generation:** PDF exports with maps
6. **Integration:** Link with forest department databases
7. **Machine Learning:** Automated tree detection
8. **Real-time Monitoring:** Daily checks

---

## 📞 Technical Support

For technical questions:
- Google Earth Engine Forum: https://groups.google.com/g/google-earth-engine-developers
- Sentinel Hub Forum: https://forum.sentinel-hub.com/

---

**Last Updated:** February 2026
**Version:** 1.0
