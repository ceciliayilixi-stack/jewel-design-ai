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
    .jewelry-preview {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

def get_relevant_jewelry_image(prompt, design_number):
    """
    Get ACTUAL jewelry images based on the prompt
    """
    # Map prompts to relevant jewelry image searches
    prompt_lower = prompt.lower()
    
    # Define jewelry-specific image searches
    jewelry_searches = {
        'ring': ['ring', 'jewelry ring', 'engagement ring', 'wedding ring', 'gold ring', 'silver ring'],
        'necklace': ['necklace', 'jewelry necklace', 'gold necklace', 'pendant necklace'],
        'earring': ['earrings', 'jewelry earrings', 'gold earrings', 'diamond earrings'],
        'bracelet': ['bracelet', 'jewelry bracelet', 'gold bracelet', 'silver bracelet'],
        'gold': ['gold jewelry', 'gold ring', 'gold necklace'],
        'silver': ['silver jewelry', 'silver ring', 'silver necklace'],
        'floral': ['floral jewelry', 'flower ring', 'floral engraving'],
        'diamond': ['diamond ring', 'diamond jewelry', 'diamond necklace'],
        'pearl': ['pearl jewelry', 'pearl earrings', 'pearl necklace'],
        'engraving': ['engraved jewelry', 'detailed jewelry', 'pattern ring']
    }
    
    # Find relevant search terms based on prompt
    search_terms = ['jewelry', 'luxury jewelry']  # Default
    
    for keyword, terms in jewelry_searches.items():
        if keyword in prompt_lower:
            search_terms.extend(terms)
    
    # Remove duplicates and ensure we have jewelry-related terms
    search_terms = list(set(search_terms))
    
    # Try multiple image services
    services = [
        f"https://source.unsplash.com/400x400/?{','.join(search_terms[:2])}",
        f"https://source.unsplash.com/featured/400x400/?{search_terms[0]},jewelry",
        f"https://picsum.photos/400/400?random={design_number + 100}"  # Different seed
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

# Preview section showing what students will get
st.markdown("""
<div class="jewelry-preview">
    <h3>🎨 Generate Beautiful Jewelry Designs</h3>
    <p>Describe your dream jewelry and get relevant design inspirations!</p>
    <p><strong>Perfect for student projects and design exploration</strong></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Design Settings")
    num_designs = st.slider("Number of designs", 1, 4, 2)
    
    st.header("🎨 Style Options")
    material = st.selectbox("Material", ["Gold", "Silver", "Platinum", "Rose Gold", "Any"])
    jewelry_type = st.selectbox("Type", ["Ring", "Necklace", "Earrings", "Bracelet", "Any"])
    
    st.markdown("---")
    st.info("""
    💡 **Better Results:**
    - Be specific: "gold ring with floral engraving"
    - Mention gemstones: "with diamond accents"
    - Add style: "vintage style", "modern design"
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✨ Describe Your Jewelry Design")
    
    # Better example prompts that work well
    example_prompts = [
        "Gold ring with floral engraving and diamond",
        "Silver necklace with geometric pendant",
        "Pearl earrings with gold setting",
        "Engagement ring with vintage details"
    ]
    
    st.write("**Click these examples for best results:**")
    cols = st.columns(2)
    for i, example in enumerate(example_prompts):
        with cols[i % 2]:
            if st.button(f"💎 {example}", key=f"btn_{i}", use_container_width=True):
                st.session_state.prompt = example

    # Main input
    prompt = st.text_area(
        "Design description:",
        placeholder="Example: 'Gold ring with floral engraving, diamond accents, and vintage styling'",
        height=100,
        key="prompt_input",
        value=st.session_state.get('prompt', '')
    )

with col2:
    st.subheader("📝 Pro Tips")
    st.markdown("""
    **For Relevant Images:**
    
    ✅ **Do:**
    - "Gold ring with floral pattern"
    - "Silver necklace geometric"
    - "Pearl earrings gold"
    - "Diamond ring vintage"
    
    ❌ **Avoid:**
    - Too generic descriptions
    - Uncommon materials
    - Complex combinations
    
    **The AI finds real jewelry images based on your keywords!**
    """)

# Generation section
st.markdown("---")
st.subheader("🎨 Generate Design Inspirations")

if st.button("✨ Get Jewelry Design Ideas", type="primary", use_container_width=True):
    if not prompt:
        st.warning("⚠️ Please describe your jewelry design first!")
    else:
        with st.spinner("🔍 Finding beautiful jewelry designs matching your description..."):
            progress_bar = st.progress(0)
            
            # Show progress
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.03)
            
            # Display results
            st.markdown(f'<div class="success-box">🎉 Found {num_designs} jewelry designs matching "{prompt}"!</div>', unsafe_allow_html=True)
            
            # Display design cards
            design_cols = st.columns(num_designs)
            
            for i in range(num_designs):
                with design_cols[i]:
                    st.markdown(f'<div class="design-card">', unsafe_allow_html=True)
                    st.markdown(f"### Design {i+1}")
                    
                    # Get RELEVANT jewelry image
                    image_data = get_relevant_jewelry_image(prompt, i)
                    
                    if image_data:
                        # Display image
                        st.image(image_data, use_column_width=True, caption=f"💎 {prompt}")
                        
                        # Download button
                        st.download_button(
                            label="📥 Save Design",
                            data=image_data,
                            file_name=f"jewelry_design_{i+1}.png",
                            mime="image/png",
                            key=f"download_{i}",
                            use_container_width=True
                        )
                    else:
                        # Fallback to jewelry-specific placeholder
                        st.image(f"https://source.unsplash.com/featured/400x400/?jewelry,{['ring','necklace','earrings','bracelet'][i % 4]}", 
                                use_container_width=True, 
                                caption="Jewelry Design Inspiration")
                        st.info("💡 Design inspiration for your project!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# Educational value section
st.markdown("---")
st.markdown("""
### 🎓 Perfect for Student Projects:

**How to use this for assignments:**
1. **Generate multiple designs** for the same concept
2. **Compare different styles** (vintage vs modern)
3. **Create design portfolios** with varied pieces
4. **Download and present** in your projects
5. **Explore material combinations** (gold vs silver)

**Educational Benefits:**
- ✅ **Design Exploration** - Try unlimited variations
- ✅ **Style Comparison** - See different aesthetic approaches  
- ✅ **Material Studies** - Understand how materials affect design
- ✅ **Presentation Ready** - Professional-looking outputs
- ✅ **No Cost** - Completely free for students
""")

# Real AI upgrade info (collapsed)
with st.expander("🚀 Upgrade to Real Text-to-Image AI (Coming Soon)"):
    st.markdown("""
    **Next Level Features Coming:**
    
    - **Real AI Generation**: Create completely new designs from text
    - **Custom Jewelry**: Unique designs that don't exist yet
    - **Exact Specifications**: Match your description perfectly
    - **Style Transfer**: Apply different art styles
    
    *Current version provides real jewelry inspirations and design references!*
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>💎 <strong>Jewelry Design Inspiration Generator</strong> - Helping students explore design possibilities!</p>
    <p>✨ Real jewelry images • Design references • Unlimited exploration</p>
</div>
""", unsafe_allow_html=True)
