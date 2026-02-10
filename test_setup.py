"""
Test script to verify installation without Earth Engine authentication
"""

import sys

def test_imports():
    """Test all required packages can be imported"""
    print("🧪 Testing Package Imports...")
    print("=" * 60)

    tests = [
        ("Earth Engine API", "ee"),
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
        ("Matplotlib", "matplotlib"),
        ("Plotly", "plotly"),
        ("Streamlit", "streamlit"),
        ("GeoPandas", "geopandas"),
        ("Shapely", "shapely"),
        ("Rasterio", "rasterio"),
        ("Folium", "folium"),
    ]

    passed = 0
    failed = 0

    for name, module in tests:
        try:
            __import__(module)
            print(f"✓ {name:20s} - OK")
            passed += 1
        except ImportError as e:
            print(f"✗ {name:20s} - FAILED: {e}")
            failed += 1

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n✅ All packages installed successfully!")
        return True
    else:
        print(f"\n❌ {failed} packages failed to import")
        return False


def test_configuration():
    """Test configuration files"""
    print("\n🔧 Testing Configuration...")
    print("=" * 60)

    try:
        sys.path.insert(0, 'backend')
        from config import DISTRICTS, SATELLITE_CONFIG, NDVI_THRESHOLDS

        print(f"✓ Configuration loaded")
        print(f"  Districts configured: {list(DISTRICTS.keys())}")
        print(f"  Satellite: {SATELLITE_CONFIG['collection']}")
        print(f"  Resolution: {SATELLITE_CONFIG['scale']}m")

        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def check_earth_engine():
    """Check Earth Engine authentication status"""
    print("\n🌍 Checking Earth Engine Status...")
    print("=" * 60)

    try:
        import ee
        ee.Initialize()
        print("✓ Earth Engine authenticated and initialized")
        return True
    except Exception as e:
        print("⚠️  Earth Engine not yet authenticated")
        print(f"   Error: {str(e)[:100]}...")
        print("\n📝 To authenticate Earth Engine:")
        print("   1. Visit this URL in your browser:")
        print("   https://code.earthengine.google.com/register")
        print("\n   2. Sign up/sign in with Google account")
        print("\n   3. Run this command in terminal:")
        print("      source venv/bin/activate")
        print("      earthengine authenticate")
        print("\n   4. Follow the browser authentication flow")
        return False


def main():
    """Run all tests"""
    print("🌳 Rajasthan Green Cover Monitoring - Setup Test")
    print("=" * 60)
    print()

    # Test imports
    imports_ok = test_imports()

    # Test configuration
    config_ok = test_configuration()

    # Check Earth Engine
    ee_ok = check_earth_engine()

    # Final summary
    print("\n" + "=" * 60)
    print("📊 SETUP STATUS SUMMARY")
    print("=" * 60)
    print(f"Package Installation:     {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Configuration:            {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Earth Engine Auth:        {'✅ PASS' if ee_ok else '⚠️  PENDING'}")
    print("=" * 60)

    if imports_ok and config_ok:
        if ee_ok:
            print("\n🎉 Setup complete! You're ready to run analysis.")
            print("\nNext steps:")
            print("  python backend/cli.py --quick")
            print("  streamlit run frontend/app.py")
        else:
            print("\n⚠️  Almost ready! Just need Earth Engine authentication.")
            print("\nTo complete setup:")
            print("  1. Run: source venv/bin/activate")
            print("  2. Run: earthengine authenticate")
            print("  3. Follow browser prompts")
            print("\nAfter authentication:")
            print("  python backend/cli.py --quick")
    else:
        print("\n❌ Setup incomplete. Please fix the errors above.")

    return imports_ok and config_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
