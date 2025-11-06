import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Jewelry Design Studio",
    page_icon="💎",
    layout="wide"
)

# Custom CSS
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
    .template-option {
        border: 2px solid transparent;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        cursor: pointer;
    }
    .template-option.selected {
        border-color: #FF6B6B;
        background-color: #FFF5F5;
    }
    .feature-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)

# ACTUAL JEWELRY DESIGN TEMPLATES
JEWELRY_TEMPLATES = {
    "rings": [
        {"name": "Classic Solitaire Ring", "description": "Simple elegant ring with center stone", "prompt": "solitaire diamond ring"},
        {"name": "Vintage Floral Ring", "description": "Intricate floral patterns with gem accents", "prompt": "vintage floral ring with engraving"},
        {"name": "Modern Geometric Ring", "description": "Clean lines and geometric shapes", "prompt": "geometric modern ring"},
        {"name": "Art Deco Ring", "description": "1920s inspired geometric patterns", "prompt": "art deco ring with geometric patterns"},
        {"name": "Nature Inspired Ring", "description": "Leaf and vine motifs", "prompt": "nature inspired leaf ring"},
        {"name": "Three-Stone Ring", "description": "Three diamonds in elegant setting", "prompt": "three stone diamond ring"},
        {"name": "Halo Ring", "description": "Center stone surrounded by smaller diamonds", "prompt": "halo diamond ring"},
        {"name": "Celtic Knot Ring", "description": "Intricate Celtic knotwork design", "prompt": "celtic knot ring"}
    ],
    "necklaces": [
        {"name": "Pendant Necklace", "description": "Elegant chain with center pendant", "prompt": "pendant necklace"},
        {"name": "Statement Collar", "description": "Bold wide necklace", "prompt": "statement collar necklace"},
        {"name": "Choker Necklace", "description": "Short necklace sitting at base of neck", "prompt": "choker necklace"},
        {"name": "Y-Necklace", "description": "Y-shaped pendant design", "prompt": "y necklace"},
        {"name": "Lariat Necklace", "description": "Long necklace with no clasp", "prompt": "lariat necklace"},
        {"name": "Multi-Strand Necklace", "description": "Layered necklace effect", "prompt": "multi strand necklace"}
    ],
    "earrings": [
        {"name": "Stud Earrings", "description": "Simple elegant studs", "prompt": "diamond stud earrings"},
        {"name": "Hoop Earrings", "description": "Classic circular hoops", "prompt": "hoop earrings"},
        {"name": "Drop Earrings", "description": "Elegant dangling design", "prompt": "drop earrings"},
        {"name": "Chandelier Earrings", "description": "Multi-tiered dramatic design", "prompt": "chandelier earrings"},
        {"name": "Huggie Earrings", "description": "Small hoops that hug the earlobe", "prompt": "huggie earrings"}
    ],
    "bracelets": [
        {"name": "Tennis Bracelet", "description": "Line of diamonds in flexible setting", "prompt": "tennis bracelet"},
        {"name": "Bangle Bracelet", "description": "Rigid circular bracelet", "prompt": "gold bangle bracelet"},
        {"name": "Charm Bracelet", "description": "Bracelet with hanging charms", "prompt": "charm bracelet"},
        {"name": "Cuff Bracelet", "description": "Open-ended bold bracelet", "prompt": "cuff bracelet"},
        {"name": "Chain Bracelet", "description": "Simple chain design", "prompt": "chain bracelet"}
    ]
}

# ACTUAL JEWELRY IMAGE URLs (these are real jewelry images)
JEWELRY_IMAGES = {
    "solitaire diamond ring": [
        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400",  # Diamond ring
        "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400",  # Ring
    ],
    "vintage floral ring with engraving": [
        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400",
        "https://images.unsplash.com/photo-1594736797933-d0401ba94693?w=400",
    ],
    "geometric modern ring": [
        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400",
        "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400",
    ],
    "pendant necklace": [
        "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400",  # Necklace
        "https://images.unsplash.com/photo-1588444650700-6c7f0c89d36b?w=400",
    ],
    "diamond stud earrings": [
        "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400",  # Earrings
        "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400",
    ],
    "tennis bracelet": [
        "https://images.unsplash.com/photo-1622434641406-a158123450f9?w=400",  # Bracelet
        "https://images.unsplash.com/photo-1588444917187-fdc45259c35f?w=400",
    ]
}

# Fallback to ensure we always have images
FALLBACK_IMAGES = {
    "rings": [
        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400",  # Ring
        "https://images.unsplash.com/photo-1594736797933-d0401ba94693?w=400",  # Ring
    ],
    "necklaces": [
        "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400",  # Necklace
        "https://images.unsplash.com/photo-1588444650700-6c7f0c89d36b?w=400",  # Necklace
    ],
    "earrings": [
        "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400",  # Earrings
        "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400",  # Earrings
    ],
    "bracelets": [
        "https://images.unsplash.com/photo-1622434641406-a158123450f9?w=400",  # Bracelet
        "https://images.unsplash.com/photo-1588444917187-fdc45259c35f?w=400",  # Bracelet
    ]
}

def get_jewelry_image(category, design_name, prompt):
    """Get relevant jewelry images"""
    if prompt in JEWELRY_IMAGES:
        return random.choice(JEWELRY_IMAGES[prompt])
    else:
        return random.choice(FALLBACK_IMAGES[category])

# App title
st.markdown('<h1 class="main-header">💎 Jewelry Design Studio</h1>', unsafe_allow_html=True)
st.markdown("### Professional Jewelry Templates for Student Projects")

# Sidebar
with st.sidebar:
    st.header("🎯 Design Setup")
    
    jewelry_type = st.selectbox(
        "Choose Jewelry Type:",
        ["rings", "necklaces", "earrings", "bracelets"]
    )
    
    st.header("⚙️ Customization")
    material = st.selectbox("Material:", ["Gold", "Silver", "Rose Gold", "Platinum", "Mixed Metals"])
    primary_stone = st.selectbox("Primary Stone:", ["Diamond", "Emerald", "Ruby", "Sapphire", "Pearl", "No Stone"])
    style = st.selectbox("Style:", ["Modern", "Vintage", "Minimalist", "Luxury", "Bohemian"])
    
    st.markdown("---")
    st.success("✅ **Ready to Design!**")

# Main content
st.subheader(f"✨ {jewelry_type.title()} Design Templates")

# Show template options
templates = JEWELRY_TEMPLATES[jewelry_type]
cols = st.columns(3)

for i, template in enumerate(templates):
    with cols[i % 3]:
        if st.button(f"**{template['name']}**\n\n{template['description']}", 
                    key=f"template_{i}", 
                    use_container_width=True):
            st.session_state.selected_template = template

# Selected template display
if 'selected_template' in st.session_state:
    template = st.session_state.selected_template
    
    st.markdown("---")
    st.subheader(f"🎨 Customizing: {template['name']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Design Preview:**")
        image_url = get_jewelry_image(jewelry_type, template['name'], template['prompt'])
        st.image(image_url, width=300)
        
        # Customization summary
        st.markdown("**Your Customization:**")
        st.write(f"- **Material**: {material}")
        st.write(f"- **Primary Stone**: {primary_stone}")
        st.write(f"- **Style**: {style}")
        st.write(f"- **Design**: {template['name']}")
    
    with col2:
        st.markdown("**Design Description:**")
        st.info(f"""
        **{template['name']}**
        
        {template['description']}
        
        This design features:
        - {material.lower()} construction
        - {primary_stone.lower()} as primary stone
        - {style.lower()} styling
        - Professional jewelry craftsmanship
        """)
        
        # Generate design card
        if st.button("🖨️ Generate Design Card", type="primary", use_container_width=True):
            with st.spinner("Creating your design presentation..."):
                time.sleep(2)
                
                st.markdown("---")
                st.subheader("🎉 Your Custom Jewelry Design")
                
                # Design card
                st.markdown(f"""
                <div style='border: 2px solid #f0f0f0; border-radius: 15px; padding: 25px; background: white; text-align: center;'>
                    <h3>💎 {template['name']}</h3>
                    <img src='{image_url}' width='250' style='border-radius: 10px; margin: 15px 0;'>
                    <div style='text-align: left; margin: 20px;'>
                        <p><strong>Material:</strong> {material}</p>
                        <p><strong>Primary Stone:</strong> {primary_stone}</p>
                        <p><strong>Style:</strong> {style}</p>
                        <p><strong>Description:</strong> {template['description']}</p>
                        <p><strong>Student Project Ready!</strong></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ Design ready for your project! Take a screenshot or use in your presentation.")

# Educational content
st.markdown("---")
st.markdown("""
### 🎓 Perfect for Student Projects:

<div class="feature-box">
<strong>✅ Real Jewelry Designs</strong><br>
Professional templates based on actual jewelry styles
</div>

<div class="feature-box">
<strong>✅ Customizable Options</strong><br>
Mix and match materials, stones, and styles
</div>

<div class="feature-box">
<strong>✅ Design Education</strong><br>
Learn about different jewelry styles and techniques
</div>

<div class="feature-box">
<strong>✅ Presentation Ready</strong><br>
Generate professional design cards for projects
</div>

<div class="feature-box">
<strong>✅ No AI Dependence</strong><br>
Reliable, consistent results every time
</div>
""")

# Project ideas
with st.expander("💡 Student Project Ideas"):
    st.markdown("""
    **Design Portfolio Projects:**
    
    1. **Collection Design**: Create 5 matching pieces (ring, necklace, earrings, bracelet)
    2. **Style Comparison**: Design the same piece in 3 different styles (modern, vintage, minimalist)
    3. **Material Study**: Show how different materials change the same design
    4. **Cultural Inspiration**: Design jewelry inspired by different cultures
    5. **Historical Eras**: Create designs inspired by different time periods
    
    **Each project includes:**
    - Design specifications
    - Material choices
    - Style descriptions
    - Visual representations
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>✨ <strong>Jewelry Design Studio</strong> - Practical design tool for students</p>
    <p>💎 Real templates • Professional results • Educational value</p>
</div>
""", unsafe_allow_html=True)
