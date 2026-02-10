"""
Earth Engine Authentication Module
Supports both local authentication and service account (for Streamlit Cloud)
"""

import ee
import json
import os
from pathlib import Path


def initialize_earth_engine():
    """
    Initialize Earth Engine with appropriate authentication method

    Tries in order:
    1. Streamlit secrets (for cloud deployment)
    2. Local credentials (for local development)
    3. Raises error if neither available
    """

    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            print("🔐 Using Streamlit service account credentials...")
            credentials = ee.ServiceAccountCredentials(
                email=st.secrets["gcp_service_account"]["client_email"],
                key_data=json.dumps(dict(st.secrets["gcp_service_account"]))
            )
            ee.Initialize(credentials)
            print("✓ Earth Engine initialized with service account")
            return True
    except ImportError:
        pass  # Streamlit not available (local development)
    except KeyError:
        pass  # Secrets not configured yet
    except Exception as e:
        print(f"⚠️  Streamlit secrets failed: {e}")

    # Try local credentials (for local development)
    try:
        ee.Initialize()
        print("✓ Earth Engine initialized with local credentials")
        return True
    except Exception as e:
        print(f"⚠️  Local credentials failed: {e}")

    # Neither method worked
    raise Exception(
        "Earth Engine authentication failed. Please either:\n"
        "1. For local: Run 'earthengine authenticate'\n"
        "2. For Streamlit Cloud: Add service account to app secrets"
    )


def is_authenticated():
    """Check if Earth Engine is authenticated"""
    try:
        ee.Initialize()
        # Try a simple operation to verify
        ee.Number(1).getInfo()
        return True
    except Exception:
        return False
