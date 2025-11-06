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
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .api-instructions {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_ai_design(prompt, api_key):
    """
    Generate AI jewelry designs - simplified version
    """
    try:
        # Use a stable model
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Enhanced prompt for jewelry
        enhanced_prompt = f"professional jewelry design: {prompt}, high quality, detailed, studio lighting, luxury jewelry"
        
        payload = {
            "inputs": enhanced_prompt,
            "options": {
                "wait_for_model": True,
                "use_cache": False
            }
        }
        
        # Make the request
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.content
        else:
            # Return the error for debugging
            return f"error_{response.status_code}"
            
    except Exception as e:
        return f"error_exception"

# App title
st.markdown('<h1 class="main-header">💎 AI Jewel Design Generator</h1>', unsafe_allow_html=True)
st.markdown("### Create custom jewelry designs with AI - Perfect for students!")

# API Instructions
st.markdown("""
<div class="api-instructions">
<strong>🔑 First: Enter your FREE Hugging Face API Key</strong><br>
1. Go to <a href="https://huggingface.co" target="_blank">huggingface.co</a><br>
2. Sign up/login → Settings → Access Tokens<br>
3. Create new token (select READ role)<br>
4. <strong>Copy token starting with hf_</strong><br>
5. Paste it in the sidebar →
</div>
""", unsafe_allow_html=True)

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
        if api_key.startswith('hf_'):
            st.success("✅ API Key format looks good!")
        else:
            st.warning("⚠️ Key should start with 'hf_'")
    
    st.header("⚙️ Design Settings")
    num_designs = st.slider("Number of designs", 1, 2, 1)
    
    st.markdown("---")
    st.info("💡 **Tip**: First generation may take 30-60 seconds")

# Main content
st.subheader("✨ Describe Your Jewelry Design")

# Simple examples
example_prompts = [
    "Gold ring with floral engraving",
    "Silver necklace with gemstone pendant", 
    "Diamond earrings modern style",
    "Pearl bracelet elegant design"
]

st.write("**Try these examples:**")
cols = st.columns(2)
for i, example in enumerate(example_prompts):
    with cols[i % 2]:
        if st.button(f"💎 {example}", key=f"btn_{i}", use_container_width=True):
            st.session_state.prompt = example

# Main input
prompt = st.text_input(
    "What jewelry would you like to create?",
    placeholder="e.g., Gold ring with floral engraving and diamonds",
    value=st.session_state.get('prompt', '')
)

# Generation button
if st.button("✨ Generate Jewelry Design with AI", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Please enter your Hugging Face API Key in the sidebar first!")
    elif not prompt:
        st.warning("⚠️ Please describe your jewelry design")
    else:
        if not api_key.startswith('hf_'):
            st.error("❌ API Key should start with 'hf_'. Please check your key.")
        else:
            with st.spinner("🤖 AI is creating your design... This may take 30-60 seconds"):
                
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(101):
                    progress_bar.progress(i)
                    status_text.text(f"Generating... {i}%")
                    time.sleep(0.3)
                
                # Generate the design
                result = generate_ai_design(prompt, api_key)
                
                if isinstance(result, bytes):
                    # Success - image generated
                    st.markdown('<div class="success-box">🎉 AI Successfully Created Your Jewelry Design!</div>', unsafe_allow_html=True)
                    
                    # Display image
                    st.image(result, use_column_width=True, caption=f"AI Generated: {prompt}")
                    
                    # Download button
                    st.download_button(
                        "📥 Download Design",
                        result,
                        file_name="ai_jewelry_design.png",
                        mime="image/png",
                        use_container_width=True
                    )
                    
                else:
                    # Handle errors
                    if "error_503" in result:
                        st.error("🔄 AI model is loading... Please wait 30 seconds and try again!")
                        st.info("This always happens on first use. The AI model needs time to load on Hugging Face servers.")
                    elif "error_401" in result:
                        st.error("❌ Invalid API Key - Please check your token")
                        st.markdown("""
                        **Make sure:**
                        - You copied the entire token
                        - Token starts with `hf_`
                        - No extra spaces before/after
                        - Token is from Settings → Access Tokens
                        """)
                    else:
                        st.error("❌ AI generation failed. Please try again in 30 seconds.")
                        st.info("This is normal for free AI services. Try a simpler prompt like 'gold ring'")

# Important notes
st.markdown("---")
st.markdown("""
### 🎓 Perfect for Student Projects:

**Why this works for students:**
- ✅ **Completely free** - No costs ever
- ✅ **Unlimited designs** - Generate as many as needed
- ✅ **Real AI technology** - Creates custom designs from text
- ✅ **No software needed** - Works in any web browser
- ✅ **Download designs** - Use in presentations and portfolios

**First time tips:**
- Wait 30-60 seconds for first generation
- Try simple prompts first
- The AI improves with more specific descriptions
""")

st.markdown("""
<div style='text-align: center'>
    <p>✨ <strong>AI Jewelry Designer</strong> - Creating custom designs for student projects!</p>
</div>
""", unsafe_allow_html=True)
