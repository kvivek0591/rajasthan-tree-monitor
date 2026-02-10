"""
Streamlit Web Dashboard for Rajasthan Green Cover Monitoring
Interactive visualization of vegetation changes
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from pathlib import Path
import sys

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / 'backend'))

try:
    import ee
    from vegetation_monitor import VegetationMonitor
    from config import DISTRICTS, NDVI_THRESHOLDS
    EE_AVAILABLE = True
except Exception as e:
    EE_AVAILABLE = False
    print(f"Earth Engine not available: {e}")

# Page configuration
st.set_page_config(
    page_title="Rajasthan Green Cover Monitor",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .danger-alert {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def load_historical_data():
    """Load historical analysis results"""
    data_dir = Path(__file__).parent.parent / 'data'
    if not data_dir.exists():
        return []

    results = []
    for file in sorted(data_dir.glob('analysis_*.json'), reverse=True):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                data['timestamp'] = file.stem.split('_', 1)[1]
                results.append(data)
        except Exception as e:
            st.warning(f"Could not load {file.name}: {e}")

    return results


def create_ndvi_gauge(ndvi_value, title="NDVI"):
    """Create a gauge chart for NDVI value"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ndvi_value,
        title={'text': title},
        delta={'reference': 0.5},
        gauge={
            'axis': {'range': [0, 1]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 0.2], 'color': "#d73027"},
                {'range': [0.2, 0.4], 'color': "#fc8d59"},
                {'range': [0.4, 0.6], 'color': "#fee08b"},
                {'range': [0.6, 0.8], 'color': "#91cf60"},
                {'range': [0.8, 1], 'color': "#1a9850"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.4
            }
        }
    ))
    fig.update_layout(height=250)
    return fig


def create_trend_chart(historical_data, district):
    """Create trend chart for historical NDVI values"""
    if not historical_data:
        return None

    dates = []
    ndvi_values = []

    for record in reversed(historical_data):
        if district in record:
            try:
                date_str = record[district]['analysis_date']
                ndvi = record[district]['current_week']['ndvi_mean']
                if ndvi is not None:
                    dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
                    ndvi_values.append(ndvi)
            except (KeyError, ValueError):
                continue

    if not dates:
        return None

    df = pd.DataFrame({'Date': dates, 'NDVI': ndvi_values})

    fig = px.line(df, x='Date', y='NDVI',
                  title=f'NDVI Trend - {district}',
                  markers=True)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="NDVI",
        yaxis_range=[0, 1],
        hovermode='x unified'
    )
    fig.add_hline(y=0.4, line_dash="dash", line_color="orange",
                  annotation_text="Moderate Vegetation Threshold")

    return fig


def display_district_analysis(district_name, results):
    """Display analysis results for a district"""
    st.subheader(f"📍 {district_name} District")

    if results is None:
        st.warning(f"No data available for {district_name}")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ndvi_current = results['current_week']['ndvi_mean']
        st.metric(
            label="Current NDVI",
            value=f"{ndvi_current:.4f}" if ndvi_current else "N/A"
        )

    with col2:
        ndvi_change = results['change']['ndvi_change_mean']
        ndvi_prev = results['previous_week']['ndvi_mean']
        if ndvi_change and ndvi_prev:
            change_pct = (ndvi_change / ndvi_prev) * 100
            st.metric(
                label="Week Change",
                value=f"{change_pct:+.2f}%",
                delta=f"{ndvi_change:+.4f}"
            )
        else:
            st.metric(label="Week Change", value="N/A")

    with col3:
        loss_area = results['change']['vegetation_loss_area_hectares']
        st.metric(
            label="Vegetation Loss",
            value=f"{loss_area:.2f} ha"
        )

    with col4:
        ndvi_median = results['current_week']['ndvi_median']
        vegetation_type = "Dense" if ndvi_median and ndvi_median > 0.6 else \
                         "Moderate" if ndvi_median and ndvi_median > 0.4 else \
                         "Sparse" if ndvi_median and ndvi_median > 0.2 else "Low"
        st.metric(
            label="Vegetation Density",
            value=vegetation_type
        )

    # Alert box
    if 'alert' in results and results['alert']['triggered']:
        alert_type = results['alert']['type']
        change_pct = results['alert']['change_percentage']

        if alert_type == 'vegetation_loss':
            st.markdown(f"""
            <div class="danger-alert">
                <strong>⚠️ ALERT: Significant Vegetation Loss Detected</strong><br>
                {abs(change_pct):.2f}% decrease in green cover compared to last week.<br>
                This may indicate tree cutting or land clearing activities.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-box">
                <strong>✓ Notice: Vegetation Increase Detected</strong><br>
                {abs(change_pct):.2f}% increase in green cover compared to last week.
            </div>
            """, unsafe_allow_html=True)

    # NDVI Gauge
    if ndvi_current:
        st.plotly_chart(
            create_ndvi_gauge(ndvi_current, f"{district_name} Current NDVI"),
            use_container_width=True
        )

    # Details expander
    with st.expander("📊 Detailed Statistics"):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Current Week:**")
            st.write(f"- Period: {results['current_week']['start']} to {results['current_week']['end']}")
            st.write(f"- Mean NDVI: {results['current_week']['ndvi_mean']:.4f}" if results['current_week']['ndvi_mean'] else "- Mean NDVI: N/A")
            st.write(f"- Median NDVI: {results['current_week']['ndvi_median']:.4f}" if results['current_week']['ndvi_median'] else "- Median NDVI: N/A")
            st.write(f"- Std Dev: {results['current_week']['ndvi_std']:.4f}" if results['current_week']['ndvi_std'] else "- Std Dev: N/A")

        with col2:
            st.write("**Change Analysis:**")
            st.write(f"- Min Change: {results['change']['ndvi_change_min']:.4f}" if results['change']['ndvi_change_min'] else "- Min Change: N/A")
            st.write(f"- Max Change: {results['change']['ndvi_change_max']:.4f}" if results['change']['ndvi_change_max'] else "- Max Change: N/A")
            st.write(f"- Loss Area: {results['change']['vegetation_loss_area_hectares']:.2f} hectares")


def main():
    """Main application"""

    # Header
    st.markdown('<h1 class="main-header">🌳 Rajasthan Green Cover Monitoring</h1>',
                unsafe_allow_html=True)

    st.markdown("""
    **Monitor week-over-week vegetation changes in Jodhpur and Bikaner districts**

    This tool uses Sentinel-2 satellite imagery to detect changes in green cover,
    helping communities protect trees from illegal cutting.
    """)

    # Sidebar
    st.sidebar.title("⚙️ Settings")

    # Check Earth Engine availability
    if not EE_AVAILABLE:
        st.sidebar.error("❌ Google Earth Engine not initialized")
        st.sidebar.info("Run: `earthengine authenticate` in terminal")
        analysis_mode = "historical"
    else:
        analysis_mode = st.sidebar.radio(
            "Analysis Mode",
            ["Live Analysis", "Historical Data"]
        ).lower().replace(" ", "_")

    selected_districts = st.sidebar.multiselect(
        "Select Districts",
        ["Jodhpur", "Bikaner"],
        default=["Jodhpur", "Bikaner"]
    )

    # Main content
    if analysis_mode == "live_analysis" and EE_AVAILABLE:
        st.info("🔄 Running live satellite analysis... This may take a few minutes.")

        if st.button("🚀 Run Analysis", type="primary"):
            try:
                monitor = VegetationMonitor()

                for district in selected_districts:
                    with st.spinner(f"Analyzing {district}..."):
                        results = monitor.analyze_district(district)
                        display_district_analysis(district, results)

                st.success("✅ Analysis complete!")

            except Exception as e:
                st.error(f"❌ Error running analysis: {e}")
                st.info("Make sure you've authenticated with Google Earth Engine")

    else:
        # Load and display historical data
        historical_data = load_historical_data()

        if not historical_data:
            st.warning("📂 No historical data found. Run a live analysis first.")
        else:
            st.success(f"📊 Loaded {len(historical_data)} historical records")

            # Display latest results
            latest = historical_data[0]

            for district in selected_districts:
                if district in latest:
                    display_district_analysis(district, latest[district])

            # Historical trends
            st.markdown("---")
            st.subheader("📈 Historical Trends")

            col1, col2 = st.columns(2)

            with col1:
                if "Jodhpur" in selected_districts:
                    trend_chart = create_trend_chart(historical_data, "Jodhpur")
                    if trend_chart:
                        st.plotly_chart(trend_chart, use_container_width=True)

            with col2:
                if "Bikaner" in selected_districts:
                    trend_chart = create_trend_chart(historical_data, "Bikaner")
                    if trend_chart:
                        st.plotly_chart(trend_chart, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Data Source: Sentinel-2 Satellite Imagery (ESA)</p>
        <p>NDVI: Normalized Difference Vegetation Index | Updated Weekly</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
