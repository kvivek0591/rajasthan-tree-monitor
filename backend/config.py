"""
Configuration file for Rajasthan Green Cover Monitoring System
"""

# District Boundaries (approximate bounding boxes)
# Format: [min_lon, min_lat, max_lon, max_lat]

DISTRICTS = {
    "Jodhpur": {
        "bbox": [72.8, 26.0, 73.5, 27.0],
        "center": [73.02, 26.28],
        "name": "Jodhpur District"
    },
    "Bikaner": {
        "bbox": [72.8, 27.5, 73.8, 28.5],
        "center": [73.31, 28.01],
        "name": "Bikaner District"
    }
}

# Satellite Configuration
SATELLITE_CONFIG = {
    "collection": "COPERNICUS/S2_SR_HARMONIZED",  # Sentinel-2 Surface Reflectance
    "cloud_cover_max": 20,  # Maximum cloud cover percentage
    "scale": 10,  # 10 meter resolution
}

# Vegetation Indices
NDVI_THRESHOLDS = {
    "no_vegetation": 0.0,
    "sparse": 0.2,
    "moderate": 0.4,
    "dense": 0.6,
    "very_dense": 0.8
}

# Alert Settings
ALERT_CONFIG = {
    "vegetation_loss_threshold": 5,  # % loss to trigger alert
    "min_area_hectares": 0.1,  # Minimum area to consider (hectares)
}

# Time Settings
ANALYSIS_INTERVAL_DAYS = 7  # Weekly analysis
HISTORICAL_MONTHS = 6  # How far back to analyze

# Color Maps for Visualization
NDVI_COLORS = {
    "palette": ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850']
}

# Export Settings
EXPORT_CONFIG = {
    "format": "GeoTIFF",
    "folder": "rajasthan_vegetation_monitoring",
    "crs": "EPSG:4326"
}
