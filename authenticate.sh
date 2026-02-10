#!/bin/bash

# Earth Engine Authentication Helper Script

echo "🔐 Google Earth Engine Authentication"
echo "======================================"
echo ""
echo "This will open your browser to authenticate with Google Earth Engine."
echo "You'll need to:"
echo "  1. Sign in with your Google account"
echo "  2. Grant permissions to Earth Engine"
echo "  3. Complete the authorization"
echo ""
echo "Press Enter to continue..."
read

cd /Users/vivekkhandelwal/Desktop/Claude\ code/GetCogniSwitch/Agents/rajasthan-tree-monitor
source venv/bin/activate

echo ""
echo "Starting authentication process..."
echo ""

# Run authentication
earthengine authenticate

echo ""
echo "======================================"
echo "✅ Authentication complete!"
echo ""
echo "Next steps:"
echo "  1. Go back to your browser: http://localhost:8501"
echo "  2. Click '🚀 Run Analysis' button again"
echo "  3. Wait 2-3 minutes for real satellite data"
echo ""
