import streamlit as st
import requests
import time
import base64
import json

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
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .ai-badge {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    .api-help {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_with_proxy_api(prompt, api_key):
    """
    Use a more reliable API approach
    """
    try:
        # Try multiple API endpoints
        endpoints = [
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
            "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        ]
        
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Better prompt for jewelry
        enhanced_prompt = f"professional jewelry design, {prompt}, high quality, detailed, studio lighting, luxury jewelry piece"
        
        payload = {
            "inputs": enhanced_prompt
        }
        
        for endpoint in endpoints:
            try:
                response = requests.post(endpoint, headers=headers, json=payload, timeout=45)
                
                if response.status_code == 200:
                    return response.content
                elif response.status_code == 503:
                    # Model is loading - wait and retry
                    st.info(f"🔄 AI model is loading... This takes 20-60 seconds on first use. Please wait...")
                    time.sleep(30)
                    response = requests.post(endpoint, headers=headers, json=payload, timeout=45)
                    if response.status_code == 200:
                        return response.content
                
            except Exception as e:
                continue
                
        return None
        
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def test_api_key(api_key):
    """
    Test if the API key is valid
    """
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

# App title
st.markdown('<h1 class="main-header">💎 AI Jewel Design Generator</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔑 AI Setup")
    
    api_key = st.text_input(
        "Hugging Face API Key:",
        type="password",
        placeholder="hf_xxxxxxxxxxxxxxxx",
        help="Paste your token that starts with hf_"
    )
    
    if api_key:
        if test_api_key(api_key):
            st.success("✅ API Key is valid!")
        else:
            st.error("❌ Invalid API Key")
            st.markdown("""
            <div class="api-help">
            <strong>How to get your free API key:</strong>
            <ol>
            <li>Go to <a href="https://huggingface.co" target="_blank">huggingface.co</a></li>
            <li>Sign up/login</li>
            <li>Go to Settings → Access Tokens</li>
            <li>Create new token (select READ role)</li>
            <li>Copy token starting with hf_</li>
            <li>Paste it here</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
    
    st.header("⚙️ Settings")
    num_designs = st.slider("Designs to generate", 1, 2, 1)
    
    st.markdown("---")
    if api_key and test_api_key(api_key):
        st.success("Ready for AI generation!")
    else:
        st.info("Enter valid API key to start")

# Main content
st.markdown("### 🎨 Describe Your Jewelry Design")

# Simple prompt input
prompt = st.text_input(
    "What jewelry do you want to create?",
    placeholder="e.g., Gold ring with floral engraving and diamonds"
)

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("✨ Generate with AI", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Hugging Face API Key in the sidebar")
        elif not prompt:
            st.warning("Please describe your jewelry design")
        else:
            with st.spinner("🤖 AI is creating your jewelry design... This may take 30-60 seconds on first use"):
                
                # Show progress
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                    time.sleep(0.3)
                
                # Generate design
                image_data = generate_with_proxy_api(prompt, api_key)
                
                if image_data:
                    st.markdown(f'<div class="success-box">🎉 AI Successfully Created Your Design!</div>', unsafe_allow_html=True)
                    
                    # Display the image
                    st.image(image_data, use_column_width=True, caption=f"AI Generated: {prompt}")
                    
                    # Download button
                    st.download_button(
                        "📥 Download Design",
                        image_data,
                        file_name="ai_jewelry_design.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.error("❌ AI generation failed. Possible reasons:")
                    st.info("""
                    - **First time use**: AI models take 30-60 seconds to load
                    - **API key issues**: Make sure your token is correct
                    - **Rate limits**: Free tier has some limits
                    - **Try again**: The model might be busy
                    """)
                    
                    st.markdown("""
                    **Quick Fixes:**
                    - Wait 1 minute and try again
                    - Check your API key is correct
                    - Try a simpler prompt like "gold ring"
                    """)

with col2:
    st.markdown("### 💡 Tips")
    st.markdown("""
    **Best Prompts:**
    - "Gold ring with floral pattern"
    - "Silver necklace with gemstone"
    - "Diamond earrings modern"
    - "Pearl bracelet elegant"
    
    **First time?** Wait 30-60 seconds for AI to load
    """)

# Alternative if API doesn't work
with st.expander("🔄 Still having issues? Try this:"):
    st.markdown("""
    **If the AI API continues to fail:**
    
    1. **Wait 5 minutes** - Hugging Face models can take time to load
    2. **Verify your token** at huggingface.co/settings/tokens
    3. **Try this exact prompt**: "simple gold ring"
    4. **Contact me** and I'll help debug further
    
    **Remember:** Free AI services can be slow during peak times, but they DO work!
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎓 <strong>For Students</strong> - Generate unlimited jewelry designs for your projects!</p>
</div>
""", unsafe_allow_html=True)
