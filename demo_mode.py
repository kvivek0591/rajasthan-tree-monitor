"""
Demo mode - Test the system without Earth Engine authentication
Generates simulated data to demonstrate functionality
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path


def generate_demo_data():
    """Generate realistic demo data for testing"""

    # Simulate realistic NDVI values for Rajasthan districts
    # Jodhpur: Semi-arid, typically 0.2-0.5
    # Bikaner: Arid, typically 0.15-0.45

    districts = {
        "Jodhpur": {
            "base_ndvi": 0.45,
            "variation": 0.08
        },
        "Bikaner": {
            "base_ndvi": 0.38,
            "variation": 0.06
        }
    }

    results = {}

    for district_name, config in districts.items():
        # Generate current week data
        current_ndvi = config["base_ndvi"] + random.uniform(-0.05, 0.05)

        # Simulate a scenario: 70% normal, 30% vegetation loss alert
        has_alert = random.random() < 0.3

        if has_alert:
            # Simulate vegetation loss
            previous_ndvi = current_ndvi + random.uniform(0.03, 0.08)
            ndvi_change = current_ndvi - previous_ndvi
            loss_area = random.uniform(50, 200)  # hectares
        else:
            # Normal variation
            previous_ndvi = current_ndvi + random.uniform(-0.02, 0.02)
            ndvi_change = current_ndvi - previous_ndvi
            loss_area = random.uniform(5, 25)  # hectares

        change_pct = (ndvi_change / previous_ndvi) * 100 if previous_ndvi else 0

        end_date = datetime.now()
        start_current = end_date - timedelta(days=7)
        start_previous = end_date - timedelta(days=14)

        results[district_name] = {
            "district": district_name,
            "analysis_date": end_date.strftime('%Y-%m-%d'),
            "current_week": {
                "start": start_current.strftime('%Y-%m-%d'),
                "end": end_date.strftime('%Y-%m-%d'),
                "ndvi_mean": round(current_ndvi, 4),
                "ndvi_std": round(random.uniform(0.08, 0.15), 4),
                "ndvi_p10": round(current_ndvi - 0.15, 4),
                "ndvi_median": round(current_ndvi + 0.01, 4),
                "ndvi_p90": round(current_ndvi + 0.12, 4),
            },
            "previous_week": {
                "start": start_previous.strftime('%Y-%m-%d'),
                "end": start_current.strftime('%Y-%m-%d'),
                "ndvi_mean": round(previous_ndvi, 4),
            },
            "change": {
                "ndvi_change_mean": round(ndvi_change, 4),
                "ndvi_change_min": round(ndvi_change - 0.05, 4),
                "ndvi_change_max": round(ndvi_change + 0.03, 4),
                "vegetation_loss_area_hectares": round(loss_area, 2),
            }
        }

        # Add alert if significant change
        if abs(change_pct) > 5:
            results[district_name]["alert"] = {
                "triggered": True,
                "type": "vegetation_loss" if change_pct < 0 else "vegetation_gain",
                "change_percentage": round(change_pct, 2),
                "message": f"⚠️ {abs(change_pct):.2f}% vegetation change detected!"
            }

    return results


def print_summary(results):
    """Print demo analysis summary"""
    print("=" * 70)
    print("🌳 DEMO MODE - Rajasthan Green Cover Monitoring")
    print("=" * 70)
    print("⚠️  Note: Using simulated data for testing (Earth Engine not authenticated)")
    print("=" * 70)

    for district_name, data in results.items():
        print(f"\n📍 {district_name} District")
        print("-" * 70)
        print(f"Analysis Date: {data['analysis_date']}")
        print(f"\n📈 Current Week NDVI Statistics:")
        print(f"   Mean NDVI: {data['current_week']['ndvi_mean']:.4f}")
        print(f"   Median NDVI: {data['current_week']['ndvi_median']:.4f}")
        print(f"   Std Dev: {data['current_week']['ndvi_std']:.4f}")
        print(f"   Range: {data['current_week']['ndvi_p10']:.4f} to {data['current_week']['ndvi_p90']:.4f}")

        print(f"\n📉 Week-over-Week Change:")
        change_pct = (data['change']['ndvi_change_mean'] /
                     data['previous_week']['ndvi_mean']) * 100
        print(f"   NDVI Change: {data['change']['ndvi_change_mean']:+.4f} ({change_pct:+.2f}%)")
        print(f"   Min Change: {data['change']['ndvi_change_min']:.4f}")
        print(f"   Max Change: {data['change']['ndvi_change_max']:.4f}")
        print(f"   Vegetation Loss Area: {data['change']['vegetation_loss_area_hectares']:.2f} hectares")

        if "alert" in data and data["alert"]["triggered"]:
            print(f"\n⚠️  ALERT: {data['alert']['message']}")
            print(f"   Type: {data['alert']['type'].replace('_', ' ').title()}")
        else:
            print(f"\n✓ No significant alerts")

        print("=" * 70)


def save_demo_data(results):
    """Save demo data to file"""
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f'demo_analysis_{timestamp}.json'

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Demo data saved to: {output_file}")
    return output_file


def main():
    """Run demo mode"""
    print("\n🧪 Starting Demo Mode...\n")

    # Generate demo data
    results = generate_demo_data()

    # Print summary
    print_summary(results)

    # Save to file
    output_file = save_demo_data(results)

    # Next steps
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE")
    print("=" * 70)
    print("\n📝 What this demonstrates:")
    print("   ✓ Data structure and format")
    print("   ✓ NDVI calculations and metrics")
    print("   ✓ Change detection logic")
    print("   ✓ Alert system triggers")
    print("   ✓ JSON export format")

    print("\n🚀 To use REAL satellite data:")
    print("   1. Authenticate with Earth Engine:")
    print("      earthengine authenticate")
    print("   2. Run actual analysis:")
    print("      python backend/cli.py --quick")

    print("\n📊 To view this demo data in the dashboard:")
    print("   streamlit run frontend/app.py")
    print("   (The dashboard will show this demo data)")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
