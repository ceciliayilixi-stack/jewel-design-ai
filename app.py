import streamlit as st
import requests
from PIL import Image
import io
import base64
import time

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
    }
    .generated-image {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">💎 AI Jewel Design Generator</h1>', unsafe_allow_html=True)
st.markdown("### Create unlimited jewelry designs with AI - No downloads required!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Design Settings")
    num_designs = st.slider("Number of designs", 1, 4, 2)
    
    st.header("🎨 Style Options")
    material = st.selectbox("Material", ["Silver", "Gold", "Platinum", "Rose Gold", "Any"])
    jewelry_type = st.selectbox("Type", ["Ring", "Necklace", "Earrings", "Bracelet", "Any"])
    
    st.markdown("---")
    st.info("💡 **Tip**: Be specific! Mention gemstones, patterns, and style for better results.")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✨ Describe Your Dream Jewelry")
    
    # Quick prompts
    example_prompts = [
        "Silver ring with leaf engraving and small diamonds",
        "Gold necklace with geometric patterns",
        "Rose gold earrings with pearl drops",
        "Platinum bracelet with art deco design"
    ]
    
    st.write("**Quick ideas:**")
    cols = st.columns(4)
    for i, example in enumerate(example_prompts):
        with cols[i]:
            if st.button(example[:15] + "...", key=f"btn_{i}"):
                st.session_state.prompt = example

    # Main input
    prompt = st.text_area(
        "Design description:",
        placeholder="Example: 'A silver ring with leaf engraving, small diamond accents, and vintage styling'",
        height=100,
        key="prompt_input"
    )

with col2:
    st.subheader("📝 Design Guide")
    st.markdown("""
    **Include in your description:**
    - 💍 Jewelry type
    - ✨ Material
    - 💎 Gemstones
    - 🎨 Patterns
    - 📐 Style
    - 🔍 Details
    """)

# Generation section
st.markdown("---")
st.subheader("🎨 Generate Your Designs")

if st.button("✨ Create Jewelry Designs", type="primary", use_container_width=True):
    if not prompt:
        st.warning("⚠️ Please describe your jewelry design first!")
    else:
        # Enhanced prompt for better results
        enhanced_prompt = f"{prompt}, {material if material != 'Any' else ''} {jewelry_type if jewelry_type != 'Any' else 'jewelry'}, professional jewelry design, high quality, detailed"
        
        with st.spinner("🔄 AI is creating your unique jewelry designs..."):
            progress_bar = st.progress(0)
            
            # Simulate AI generation process
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.02)
            
            st.success(f"✅ Generated {num_designs} unique design(s)!")
            
            # Display design cards
            design_cols = st.columns(num_designs)
            
            for i in range(num_designs):
                with design_cols[i]:
                    st.markdown(f'<div class="design-card">', unsafe_allow_html=True)
                    st.markdown(f"**Design {i+1}**")
                    
                    # Placeholder image (will replace with AI later)
                    placeholder_url = f"https://picsum.photos/300/300?random={i}&grayscale"
                    st.image(placeholder_url, use_column_width=True, caption="Your AI-generated design")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Design",
                        data="Placeholder image data - real AI coming soon!",
                        file_name=f"jewelry_design_{i+1}.png",
                        mime="image/png",
                        key=f"download_{i}"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎓 <strong>For Students:</strong> Generate unlimited jewelry designs for your projects!</p>
    <p>💫 No software downloads required • Works entirely in your browser</p>
</div>
""", unsafe_allow_html=True)
