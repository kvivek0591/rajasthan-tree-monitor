#!/usr/bin/env python3
"""
Simple CLI tool for quick vegetation monitoring checks
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    from vegetation_monitor import VegetationMonitor
    from config import DISTRICTS
except ImportError:
    print("Error: Could not import modules. Make sure you're in the correct directory.")
    sys.exit(1)


def format_alert(results):
    """Format alert message"""
    if 'alert' not in results or not results['alert']['triggered']:
        return "✓ No alerts"

    alert = results['alert']
    if alert['type'] == 'vegetation_loss':
        return f"⚠️  ALERT: {abs(alert['change_percentage']):.2f}% vegetation loss!"
    else:
        return f"✓ {abs(alert['change_percentage']):.2f}% vegetation increase"


def quick_check(district=None):
    """Quick check with minimal output"""
    monitor = VegetationMonitor()

    districts_to_check = [district] if district else list(DISTRICTS.keys())

    print("🌳 Quick Vegetation Check")
    print("=" * 60)

    for dist in districts_to_check:
        try:
            results = monitor.analyze_district(dist)

            ndvi = results['current_week']['ndvi_mean']
            change = results['change']['ndvi_change_mean']
            prev = results['previous_week']['ndvi_mean']

            change_pct = (change / prev * 100) if prev else 0
            alert_msg = format_alert(results)

            print(f"\n📍 {dist}:")
            print(f"   NDVI: {ndvi:.4f} ({change_pct:+.2f}%)")
            print(f"   {alert_msg}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)


def detailed_report(district):
    """Detailed report for specific district"""
    monitor = VegetationMonitor()

    try:
        results = monitor.analyze_district(district)
        monitor.print_summary(results)
    except Exception as e:
        print(f"❌ Error analyzing {district}: {e}")
        sys.exit(1)


def compare_districts():
    """Compare both districts side by side"""
    monitor = VegetationMonitor()

    print("🌳 District Comparison")
    print("=" * 60)

    results = {}
    for district in DISTRICTS.keys():
        try:
            results[district] = monitor.analyze_district(district)
        except Exception as e:
            print(f"❌ Error analyzing {district}: {e}")
            continue

    if len(results) < 2:
        print("❌ Could not compare districts")
        return

    # Compare NDVI
    print("\n📊 Current NDVI:")
    for district, data in results.items():
        ndvi = data['current_week']['ndvi_mean']
        print(f"   {district:12s}: {ndvi:.4f}")

    # Compare changes
    print("\n📈 Week-over-Week Change:")
    for district, data in results.items():
        change = data['change']['ndvi_change_mean']
        prev = data['previous_week']['ndvi_mean']
        change_pct = (change / prev * 100) if prev else 0
        print(f"   {district:12s}: {change_pct:+.2f}%")

    # Compare alerts
    print("\n⚠️  Alerts:")
    for district, data in results.items():
        alert_msg = format_alert(data)
        print(f"   {district:12s}: {alert_msg}")

    print("=" * 60)


def list_history():
    """List historical analysis files"""
    data_dir = Path(__file__).parent.parent / 'data'

    if not data_dir.exists():
        print("📂 No data directory found")
        return

    files = sorted(data_dir.glob('analysis_*.json'), reverse=True)

    if not files:
        print("📂 No analysis files found")
        return

    print("📂 Analysis History:")
    print("=" * 60)

    for i, file in enumerate(files[:10], 1):  # Show last 10
        timestamp = file.stem.split('_', 1)[1]
        try:
            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            print(f"{i:2d}. {dt.strftime('%Y-%m-%d %H:%M:%S')} - {file.name}")
        except ValueError:
            print(f"{i:2d}. {file.name}")

    if len(files) > 10:
        print(f"\n... and {len(files) - 10} more files")


def main():
    parser = argparse.ArgumentParser(
        description='Rajasthan Green Cover Monitoring CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --quick              # Quick check all districts
  %(prog)s --quick --district Jodhpur  # Quick check one district
  %(prog)s --detailed Jodhpur   # Detailed report for Jodhpur
  %(prog)s --compare            # Compare both districts
  %(prog)s --history            # List historical analyses
        """
    )

    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Quick check with minimal output'
    )

    parser.add_argument(
        '--detailed', '-d',
        metavar='DISTRICT',
        choices=['Jodhpur', 'Bikaner'],
        help='Detailed report for specific district'
    )

    parser.add_argument(
        '--compare', '-c',
        action='store_true',
        help='Compare both districts'
    )

    parser.add_argument(
        '--district',
        choices=['Jodhpur', 'Bikaner'],
        help='Specify district for quick check'
    )

    parser.add_argument(
        '--history',
        action='store_true',
        help='List historical analysis files'
    )

    args = parser.parse_args()

    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Execute commands
    try:
        if args.history:
            list_history()
        elif args.quick:
            quick_check(args.district)
        elif args.detailed:
            detailed_report(args.detailed)
        elif args.compare:
            compare_districts()
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
