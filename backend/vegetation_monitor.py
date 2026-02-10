"""
Core vegetation monitoring module using Google Earth Engine
Monitors week-over-week green cover changes in Rajasthan districts
"""

import ee
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, List
import json
from pathlib import Path

from config import DISTRICTS, SATELLITE_CONFIG, NDVI_THRESHOLDS, ALERT_CONFIG
from ee_auth import initialize_earth_engine


class VegetationMonitor:
    """Monitor vegetation changes using Sentinel-2 satellite imagery"""

    def __init__(self):
        """Initialize Earth Engine and load configuration"""
        try:
            initialize_earth_engine()
            print("✓ Google Earth Engine initialized successfully")
        except Exception as e:
            print(f"✗ Earth Engine initialization failed: {e}")
            print("Run 'earthengine authenticate' first or add service account to Streamlit secrets")
            raise

        self.districts = DISTRICTS
        self.satellite_config = SATELLITE_CONFIG

    def get_sentinel2_image(self, bbox: List[float], start_date: str, end_date: str) -> ee.Image:
        """
        Fetch Sentinel-2 imagery for specified area and date range

        Args:
            bbox: [min_lon, min_lat, max_lon, max_lat]
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format

        Returns:
            ee.Image: Median composite of Sentinel-2 images
        """
        region = ee.Geometry.Rectangle(bbox)

        collection = ee.ImageCollection(self.satellite_config['collection']) \
            .filterBounds(region) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',
                                  self.satellite_config['cloud_cover_max']))

        # Return median composite to reduce cloud influence
        return collection.median().clip(region)

    def calculate_ndvi(self, image: ee.Image) -> ee.Image:
        """
        Calculate NDVI (Normalized Difference Vegetation Index)
        NDVI = (NIR - Red) / (NIR + Red)

        Args:
            image: Sentinel-2 image

        Returns:
            ee.Image: NDVI image with values from -1 to 1
        """
        nir = image.select('B8')  # Near Infrared band
        red = image.select('B4')  # Red band

        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        return ndvi

    def analyze_district(self, district_name: str, weeks_back: int = 2) -> Dict:
        """
        Analyze vegetation changes for a district

        Args:
            district_name: Name of district ('Jodhpur' or 'Bikaner')
            weeks_back: Number of weeks to look back for comparison

        Returns:
            Dict containing analysis results
        """
        if district_name not in self.districts:
            raise ValueError(f"District {district_name} not found")

        district = self.districts[district_name]
        bbox = district['bbox']

        # Define time periods
        end_date = datetime.now()
        start_current_week = end_date - timedelta(days=7)
        start_previous_week = end_date - timedelta(days=14)

        print(f"\n📍 Analyzing {district_name} District...")
        print(f"   Current week: {start_current_week.date()} to {end_date.date()}")
        print(f"   Previous week: {start_previous_week.date()} to {start_current_week.date()}")

        # Fetch imagery for both weeks
        current_week_img = self.get_sentinel2_image(
            bbox,
            start_current_week.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )

        previous_week_img = self.get_sentinel2_image(
            bbox,
            start_previous_week.strftime('%Y-%m-%d'),
            start_current_week.strftime('%Y-%m-%d')
        )

        # Calculate NDVI for both weeks
        ndvi_current = self.calculate_ndvi(current_week_img)
        ndvi_previous = self.calculate_ndvi(previous_week_img)

        # Calculate change
        ndvi_change = ndvi_current.subtract(ndvi_previous).rename('NDVI_Change')

        # Calculate statistics
        region = ee.Geometry.Rectangle(bbox)
        scale = self.satellite_config['scale']

        stats_current = ndvi_current.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                ee.Reducer.stdDev(), '', True
            ).combine(
                ee.Reducer.percentile([10, 50, 90]), '', True
            ),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()

        stats_previous = ndvi_previous.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()

        stats_change = ndvi_change.reduceRegion(
            reducer=ee.Reducer.mean().combine(
                ee.Reducer.min(), '', True
            ).combine(
                ee.Reducer.max(), '', True
            ),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()

        # Calculate vegetation loss areas
        vegetation_loss = ndvi_change.lt(-0.1)  # Significant loss threshold
        loss_area_pixels = vegetation_loss.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=region,
            scale=scale,
            maxPixels=1e9
        ).getInfo()

        # Convert to hectares (10m pixel = 100 sq m = 0.01 hectares)
        loss_area_hectares = loss_area_pixels.get('NDVI_Change', 0) * 0.01

        # Compile results
        results = {
            'district': district_name,
            'analysis_date': end_date.strftime('%Y-%m-%d'),
            'current_week': {
                'start': start_current_week.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'ndvi_mean': stats_current.get('NDVI_mean', None),
                'ndvi_std': stats_current.get('NDVI_stdDev', None),
                'ndvi_p10': stats_current.get('NDVI_p10', None),
                'ndvi_median': stats_current.get('NDVI_p50', None),
                'ndvi_p90': stats_current.get('NDVI_p90', None),
            },
            'previous_week': {
                'start': start_previous_week.strftime('%Y-%m-%d'),
                'end': start_current_week.strftime('%Y-%m-%d'),
                'ndvi_mean': stats_previous.get('NDVI_mean', None),
            },
            'change': {
                'ndvi_change_mean': stats_change.get('NDVI_Change_mean', None),
                'ndvi_change_min': stats_change.get('NDVI_Change_min', None),
                'ndvi_change_max': stats_change.get('NDVI_Change_max', None),
                'vegetation_loss_area_hectares': loss_area_hectares,
            },
            'images': {
                'ndvi_current': ndvi_current,
                'ndvi_previous': ndvi_previous,
                'ndvi_change': ndvi_change,
            }
        }

        # Check for alerts
        if results['change']['ndvi_change_mean'] is not None:
            change_pct = (results['change']['ndvi_change_mean'] /
                         results['previous_week']['ndvi_mean'] * 100)

            if abs(change_pct) > ALERT_CONFIG['vegetation_loss_threshold']:
                results['alert'] = {
                    'triggered': True,
                    'type': 'vegetation_loss' if change_pct < 0 else 'vegetation_gain',
                    'change_percentage': change_pct,
                    'message': f"⚠️ {abs(change_pct):.2f}% vegetation change detected!"
                }

        return results

    def generate_map_url(self, image: ee.Image, vis_params: Dict, region: List[float]) -> str:
        """Generate a URL for visualizing the image"""
        map_id = image.getMapId(vis_params)
        return map_id['tile_fetcher'].url_format

    def print_summary(self, results: Dict):
        """Print analysis summary to console"""
        print(f"\n{'='*60}")
        print(f"📊 VEGETATION ANALYSIS SUMMARY - {results['district']}")
        print(f"{'='*60}")
        print(f"Analysis Date: {results['analysis_date']}")
        print(f"\n📈 Current Week NDVI Statistics:")
        print(f"   Mean NDVI: {results['current_week']['ndvi_mean']:.4f}")
        print(f"   Median NDVI: {results['current_week']['ndvi_median']:.4f}")
        print(f"   Std Dev: {results['current_week']['ndvi_std']:.4f}")

        print(f"\n📉 Week-over-Week Change:")
        change_mean = results['change']['ndvi_change_mean']
        if change_mean is not None and results['previous_week']['ndvi_mean'] is not None:
            change_pct = (change_mean / results['previous_week']['ndvi_mean']) * 100
            print(f"   NDVI Change: {change_mean:+.4f} ({change_pct:+.2f}%)")

        print(f"   Min Change: {results['change']['ndvi_change_min']:.4f}")
        print(f"   Max Change: {results['change']['ndvi_change_max']:.4f}")
        print(f"   Vegetation Loss Area: {results['change']['vegetation_loss_area_hectares']:.2f} hectares")

        if 'alert' in results and results['alert']['triggered']:
            print(f"\n{results['alert']['message']}")

        print(f"{'='*60}\n")


def main():
    """Main execution function"""
    print("🌳 Rajasthan Green Cover Monitoring System")
    print("=" * 60)

    monitor = VegetationMonitor()

    # Analyze both districts
    results = {}
    for district in ['Jodhpur', 'Bikaner']:
        try:
            results[district] = monitor.analyze_district(district)
            monitor.print_summary(results[district])
        except Exception as e:
            print(f"✗ Error analyzing {district}: {e}")

    # Save results to JSON
    output_dir = Path('../data')
    output_dir.mkdir(exist_ok=True)

    # Remove ee.Image objects before JSON serialization
    json_results = {}
    for district, data in results.items():
        json_data = data.copy()
        json_data.pop('images', None)  # Remove image objects
        json_results[district] = json_data

    output_file = output_dir / f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w') as f:
        json.dump(json_results, f, indent=2)

    print(f"✓ Results saved to {output_file}")


if __name__ == "__main__":
    main()
