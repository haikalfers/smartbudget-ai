"""
responsive_utils.py
Utility functions untuk responsive design dan mobile detection
"""

import streamlit as st

def get_columns_config():
    """
    Return responsive column configuration
    Menggunakan CSS media queries, bukan JavaScript detection
    """
    # Desktop: 4 columns
    # Tablet (768px): 2 columns (handled by CSS)
    # Mobile (480px): 1 column (handled by CSS)
    return {
        "metrics": 4,  # Will be responsive via CSS
        "charts": 2,
        "form": 2,
    }

def get_metric_columns(count=4):
    """
    Create responsive metric columns
    Always use 2 columns on Python side, CSS handles mobile stacking
    """
    if count <= 2:
        return st.columns(count)
    else:
        # Return as pairs - CSS media queries will handle single column on mobile
        return st.columns(2)

def inject_mobile_css():
    """
    Inject meta viewport tag for proper mobile scaling
    This is already in Streamlit by default, but ensuring it's there
    """
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """, unsafe_allow_html=True)

def get_form_columns():
    """Return responsive form column layout"""
    return st.columns([1, 1], gap="large")

def get_filter_columns():
    """Return responsive filter column layout"""
    # Always use 2 columns on Python side, CSS handles mobile
    return st.columns(2)
