"""
Complete workflow example demonstrating all features
Run this after setup to test the entire system
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / 'backend'))

import ee
from vegetation_monitor import VegetationMonitor
from config import DISTRICTS
import json
from datetime import datetime


def main():
    """
    Complete workflow demonstrating:
    1. Initialization
    2. Data collection
    3. Analysis
    4. Visualization
    5. Export
    """

    print("=" * 70)
    print("🌳 RAJASTHAN GREEN COVER MONITORING - COMPLETE WORKFLOW")
    print("=" * 70)

    # Step 1: Initialize
    print("\n[Step 1] Initializing Earth Engine...")
    try:
        ee.Initialize()
        print("✓ Earth Engine initialized")
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        print("Run: earthengine authenticate")
        return

    # Step 2: Create monitor instance
    print("\n[Step 2] Creating monitor instance...")
    monitor = VegetationMonitor()
    print("✓ Monitor created")

    # Step 3: Analyze both districts
    print("\n[Step 3] Analyzing districts...")
    results = {}

    for district_name in ['Jodhpur', 'Bikaner']:
        print(f"\n   Analyzing {district_name}...")
        try:
            district_results = monitor.analyze_district(district_name)
            results[district_name] = district_results
            print(f"   ✓ {district_name} analyzed")

            # Quick summary
            ndvi = district_results['current_week']['ndvi_mean']
            change = district_results['change']['ndvi_change_mean']
            print(f"      NDVI: {ndvi:.4f}, Change: {change:+.4f}")

        except Exception as e:
            print(f"   ✗ Error: {e}")

    # Step 4: Print detailed summaries
    print("\n[Step 4] Generating detailed reports...")
    for district_name, district_results in results.items():
        monitor.print_summary(district_results)

    # Step 5: Comparison
    print("\n[Step 5] District Comparison...")
    print("=" * 70)

    if len(results) == 2:
        jodhpur_ndvi = results['Jodhpur']['current_week']['ndvi_mean']
        bikaner_ndvi = results['Bikaner']['current_week']['ndvi_mean']

        print(f"Jodhpur NDVI: {jodhpur_ndvi:.4f}")
        print(f"Bikaner NDVI: {bikaner_ndvi:.4f}")

        if jodhpur_ndvi > bikaner_ndvi:
            diff = jodhpur_ndvi - bikaner_ndvi
            print(f"\n→ Jodhpur has {diff:.4f} higher vegetation density")
        else:
            diff = bikaner_ndvi - jodhpur_ndvi
            print(f"\n→ Bikaner has {diff:.4f} higher vegetation density")

    # Step 6: Alert summary
    print("\n[Step 6] Alert Summary...")
    print("=" * 70)

    alerts_found = False
    for district_name, district_results in results.items():
        if 'alert' in district_results and district_results['alert']['triggered']:
            alerts_found = True
            alert = district_results['alert']
            print(f"\n⚠️  ALERT: {district_name}")
            print(f"   Type: {alert['type'].replace('_', ' ').title()}")
            print(f"   Change: {alert['change_percentage']:+.2f}%")
            print(f"   Message: {alert['message']}")

    if not alerts_found:
        print("✓ No alerts triggered")

    # Step 7: Export results
    print("\n[Step 7] Exporting results...")

    # Remove image objects for JSON serialization
    json_results = {}
    for district, data in results.items():
        json_data = data.copy()
        json_data.pop('images', None)
        json_results[district] = json_data

    # Save to file
    output_dir = Path(__file__).parent.parent / 'data'
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f'analysis_{timestamp}.json'

    with open(output_file, 'w') as f:
        json.dump(json_results, f, indent=2)

    print(f"✓ Results saved to: {output_file}")

    # Step 8: Generate summary statistics
    print("\n[Step 8] Summary Statistics...")
    print("=" * 70)

    total_loss_area = sum(
        r['change']['vegetation_loss_area_hectares']
        for r in results.values()
    )

    print(f"Total Vegetation Loss Area: {total_loss_area:.2f} hectares")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Districts Analyzed: {len(results)}")

    # Step 9: Recommendations
    print("\n[Step 9] Recommendations...")
    print("=" * 70)

    if total_loss_area > 50:
        print("⚠️  Significant vegetation loss detected!")
        print("   → Conduct ground survey in affected areas")
        print("   → Document with photographs and GPS coordinates")
        print("   → Report to forest department")
    elif total_loss_area > 10:
        print("⚠️  Moderate vegetation loss detected")
        print("   → Monitor area for additional changes")
        print("   → Consider field verification")
    else:
        print("✓ Vegetation loss within normal range")
        print("   → Continue regular weekly monitoring")

    # Final summary
    print("\n" + "=" * 70)
    print("✅ WORKFLOW COMPLETE")
    print("=" * 70)
    print("\nNext Steps:")
    print("  1. Review the detailed reports above")
    print("  2. Check the exported JSON file for data")
    print("  3. Run the web dashboard: streamlit run frontend/app.py")
    print("  4. Schedule weekly monitoring")
    print("\n🌳 Thank you for protecting Rajasthan's trees!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
