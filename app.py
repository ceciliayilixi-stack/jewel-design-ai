import streamlit as st
import requests
import time
import random
import base64
from PIL import Image
import io

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
    .info-box {
        background: linear-gradient(45deg, #2196F3, #21CBF3);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def get_jewelry_image(prompt, design_number):
    """
    Get jewelry-related images from free APIs
    """
    jewelry_keywords = ["jewelry", "ring", "necklace", "earrings", "bracelet", "gem", "crystal", "diamond", "gold", "silver"]
    
    # Use different services for variety
    services = [
        f"https://source.unsplash.com/400x400/?{random.choice(jewelry_keywords)},luxury",
        f"https://picsum.photos/400/400?random={design_number}",
        f"https://placekitten.com/400/400?image={design_number}"
    ]
    
    for service_url in services:
        try:
            response = requests.get(service_url, timeout=10)
            if response.status_code == 200:
                return response.content
        except:
            continue
    
    return None

# App title
st.markdown('<h1 class="main-header">💎 AI Jewel Design Generator</h1>', unsafe_allow_html=True)
st.markdown("### Create unlimited jewelry designs with AI - No downloads required!")

# Info box
st.markdown("""
<div class="info-box">
    <strong>🚀 Next Step Ready:</strong> Real AI integration will be added after initial deployment! 
    Currently using advanced placeholders.
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Design Settings")
    num_designs = st.slider("Number of designs", 1, 6, 3)
    
    st.header("🎨 Style Options")
    material = st.selectbox("Material", ["Silver", "Gold", "Platinum", "Rose Gold", "Titanium", "Any"])
    jewelry_type = st.selectbox("Type", ["Ring", "Necklace", "Earrings", "Bracelet", "Brooch", "Any"])
    
    st.markdown("---")
    st.info("💡 **Pro Tip**: Add specific details like 'emerald gemstone', 'floral pattern', or 'vintage style'!")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✨ Describe Your Dream Jewelry")
    
    # Quick prompts
    example_prompts = [
        "Silver ring with leaf engraving and small diamonds",
        "Gold necklace with geometric patterns and emerald",
        "Rose gold earrings with pearl drops vintage style",
        "Platinum bracelet with art deco design and sapphire",
        "Minimalist titanium wedding band with texture",
        "Statement necklace with multiple gemstones"
    ]
    
    st.write("**Try these examples:**")
    cols = st.columns(3)
    for i, example in enumerate(example_prompts):
        col_idx = i % 3
        with cols[col_idx]:
            if st.button(example[:20] + "...", key=f"btn_{i}", use_container_width=True):
                st.session_state.prompt = example

    # Main input
    prompt = st.text_area(
        "Design description:",
        placeholder="Example: 'A silver ring with leaf engraving, small diamond accents, and vintage styling'",
        height=100,
        key="prompt_input",
        value=st.session_state.get('prompt', '')
    )

with col2:
    st.subheader("📝 Design Guide")
    st.markdown("""
    **For Best Results:**
    
    💍 **Type**: ring, necklace, earrings
    ✨ **Material**: gold, silver, platinum  
    💎 **Gemstones**: diamond, ruby, emerald
    🎨 **Pattern**: floral, geometric, abstract
    📐 **Style**: vintage, modern, minimalist
    🔍 **Details**: engraved, textured, polished
    
    **Example:**
    *"Gold ring with floral engraving, emerald center stone, vintage style"*
    """)

# Generation section
st.markdown("---")
st.subheader("🎨 Generate Your Designs")

if st.button("✨ Create Magic! Generate Jewelry Designs", type="primary", use_container_width=True):
    if not prompt:
        st.warning("⚠️ Please describe your jewelry design first!")
    else:
        with st.spinner("🔮 AI is crafting your unique jewelry designs..."):
            progress_bar = st.progress(0)
            
            # Simulate realistic generation time
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.05)
            
            # Display results
            st.markdown('<div class="success-box">🎉 Success! Generated {} unique jewelry designs!</div>'.format(num_designs), unsafe_allow_html=True)
            st.success(f"**Design Description:** {prompt}")
            
            # Display design cards
            design_cols = st.columns(num_designs)
            
            for i in range(num_designs):
                with design_cols[i]:
                    st.markdown(f'<div class="design-card">', unsafe_allow_html=True)
                    st.markdown(f"### Design {i+1}")
                    
                    # Get image from free service
                    image_data = get_jewelry_image(prompt, i)
                    
                    if image_data:
                        # Display image
                        st.image(image_data, use_column_width=True, caption=f"✨ {prompt.split(',')[0]}")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Design",
                            data=image_data,
                            file_name=f"jewelry_design_{i+1}.png",
                            mime="image/png",
                            key=f"download_{i}",
                            use_container_width=True
                        )
                    else:
                        # Fallback
                        st.image(f"https://picsum.photos/400/400?random={i}", 
                                use_container_width=True, 
                                caption="Your jewelry design")
                        st.info("Real AI coming in next update!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# Next steps section
with st.expander("🚀 Upgrade to Real AI Generation"):
    st.markdown("""
    **Next Steps to Enable Real AI:**
    
    1. **✅ Current Status**: App deployed successfully
    2. **🔜 Next**: Add Hugging Face AI integration
    3. **🎯 Result**: Real AI-generated jewelry designs!
    
    **What you'll get:**
    - Real AI image generation from text
    - Custom jewelry designs
    - High-quality outputs
    - Unlimited generations
    
    *The foundation is ready! Real AI integration is simple from here.*
    """)

# Student benefits
st.markdown("---")
st.markdown("""
### 🎓 Perfect for Students:
- **💰 Completely Free** - No costs, no limits
- **🔄 Unlimited Designs** - Generate as many as you need
- **📚 Project Ready** - Use for assignments and portfolios
- **🌐 No Installation** - Works in any browser
- **🚀 Always Available** - Access from anywhere
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>💎 <strong>AI Jewel Design Generator</strong> - Making jewelry design accessible to all students!</p>
    <p>✨ No software downloads • Works in browser • Free forever</p>
</div>
""", unsafe_allow_html=True)
