import streamlit as st
import requests
import time
import base64

# Page configuration
st.set_page_config(
    page_title="AI Jewel Design Generator",
    page_icon="💎",
    layout="wide"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4A4A4A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .design-card {
        border: 2px solid #f0f0f0;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        background: white;
        transition: transform 0.2s;
    }
    .design-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .stButton button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
    }
    .success-box {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 20px;
       
