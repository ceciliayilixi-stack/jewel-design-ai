import streamlit as st
import json
import time
from datetime import datetime

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
    .design-spec-card {
        border: 2px solid #f0f0f0;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .spec-item {
        background: #f8f9fa;
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 8px;
        border-left: 4px solid #FF6B6B;
    }
    .material-gold { background: #ffd700; color: black; padding: 5px 10px; border-radius: 5px; }
    .material-silver { background: #c0c0c0; color: black; padding: 5px 10px; border-radius: 5px; }
    .material-rosegold { background: #b76e79; color: white; padding: 5px 10px; border-radius: 5px; }
    .material-platinum { background: #e5e4e2; color: black; padding: 5px 10px; border-radius: 5px; }
    
    .stone-diamond { background: linear-gradient(45deg, #e6f7ff, #b3e0ff); padding: 5px 10px; border-radius: 5px; }
    .stone-emerald { background: linear-gradient(45deg, #90EE90, #32CD32); padding: 5px 10px; border-radius: 5px; }
    .stone-ruby { background: linear-gradient(45deg, #ffcccc, #ff6666); padding: 5px 10px; border-radius: 5px; }
    .stone-sapphire { background: linear-gradient(45deg, #ccccff, #6666ff); padding: 5px 10px; border-radius: 5px; }
    
    .style-modern { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 5px 10px; border-radius: 5px; }
    .style-vintage { background: linear-gradient(45deg, #f093fb, #f5576c); color: white; padding: 5px 10px; border-radius: 5px; }
    .style-minimalist { background: linear-gradient(45deg, #4facfe, #00f2fe); color: white; padding: 5px 10px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Design Templates Database
DESIGN_TEMPLATES = {
    "rings": {
        "solitaire": {
            "name": "Classic Solitaire Ring",
            "description": "Single prominent stone in simple elegant setting",
            "elements": ["Center stone", "Prong setting", "Simple band", "Four or six prongs"],
            "best_for": ["Engagement", "Everyday wear", "Minimalist style"]
        },
        "vintage_floral": {
            "name": "Vintage Floral Ring", 
            "description": "Intricate floral patterns with milgrain details",
            "elements": ["Floral engraving", "Milgrain edges", "Small accent stones", "Scrolling patterns"],
            "best_for": ["Vintage lovers", "Detailed craftsmanship", "Romantic style"]
        },
        "modern_geometric": {
            "name": "Modern Geometric Ring",
            "description": "Clean lines, geometric shapes, and contemporary design",
            "elements": ["Angular shapes", "Clean lines", "Asymmetric design", "Mixed materials"],
            "best_for": ["Modern style", "Architectural inspiration", "Bold statements"]
        },
        "three_stone": {
            "name": "Three-Stone Ring",
            "description": "Three stones representing past, present, and future",
            "elements": ["Three main stones", "Channel or prong setting", "Graduated stones", "Symbolic meaning"],
            "best_for": ["Anniversaries", "Meaningful gifts", "Balanced design"]
        }
    },
    "necklaces": {
        "pendant": {
            "name": "Classic Pendant Necklace",
            "description": "Elegant chain with meaningful centerpiece",
            "elements": ["Chain", "Pendant", "Lobster clasp", "Adjustable length"],
            "best_for": ["Personalization", "Layering", "Everyday wear"]
        },
        "statement": {
            "name": "Statement Collar Necklace",
            "description": "Bold design that makes an impact",
            "elements": ["Wide design", "Multiple elements", "Dramatic presence", "Neck-hugging fit"],
            "best_for": ["Evening wear", "Special occasions", "Fashion statements"]
        }
    }
}

# Material properties
MATERIALS = {
    "Gold": {"color": "yellow", "properties": ["Malleable", "Doesn't tarnish", "Traditional"], "class": "material-gold"},
    "Silver": {"color": "silver", "properties": ["Bright white", "Affordable", "Versatile"], "class": "material-silver"}, 
    "Rose Gold": {"color": "pink", "properties": ["Romantic", "Modern", "Durable"], "class": "material-rosegold"},
    "Platinum": {"color": "white", "properties": ["Heavy", "Hypoallergenic", "Prestigious"], "class": "material-platinum"}
}

# Stone properties
STONES = {
    "Diamond": {"color": "clear", "properties": ["Hardest stone", "Brilliant sparkle", "Traditional"], "class": "stone-diamond"},
    "Emerald": {"color": "green", "properties": ["Vivid green", "Inclusions common", "Luxurious"], "class": "stone-emerald"},
    "Ruby": {"color": "red", "properties": ["Deep red", "Rare", "Passionate"], "class": "stone-ruby"},
    "Sapphire": {"color": "blue", "properties": ["Royal blue", "Durable", "Elegant"], "class": "stone-sapphire"}
}

# App title
st.markdown('<h1 class="main-header">💎 Jewelry Design Specification Studio</h1>', unsafe_allow_html=True)
st.markdown("### Create Detailed Jewelry Design Specifications for Student Projects")

st.info("""
**🎯 This tool creates detailed design specifications** that students can use to:
- **Sketch their designs** based on exact specifications
- **Understand material properties** and design elements
- **Create professional design briefs** for portfolios
- **Learn real jewelry design principles**
""")

# Design Creation Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎨 Design Configuration")
    
    jewelry_type = st.selectbox(
        "Jewelry Type:",
        ["rings", "necklaces", "earrings", "bracelets"]
    )
    
    design_style = st.selectbox(
        "Design Style:",
        list(DESIGN_TEMPLATES.get(jewelry_type, {}).keys())
    )
    
    material = st.selectbox("Primary Material:", list(MATERIALS.keys()))
    primary_stone = st.selectbox("Primary Stone:", list(STONES.keys()))
    
    # Additional customizations
    st.subheader("🔧 Additional Details")
    engraving = st.text_input("Engraving/Pattern:", placeholder="e.g., Floral vines, Geometric lines")
    setting_type = st.selectbox("Setting Style:", ["Prong", "Bezel", "Channel", "Pave", "Tension"])
    target_audience = st.selectbox("Target Audience:", ["Bridal", "Everyday", "Luxury", "Fashion", "Vintage"])

with col2:
    st.subheader("📐 Technical Specifications")
    
    if jewelry_type == "rings":
        ring_size = st.slider("Ring Size (US):", 3, 13, 7)
        band_width = st.selectbox("Band Width:", ["Thin (2mm)", "Standard (4mm)", "Wide (6mm)", "Extra Wide (8mm+)"])
        
    elif jewelry_type == "necklaces":
        chain_length = st.selectbox("Chain Length:", 
            ["Choker (14-16\")", "Princess (18\")", "Matinee (20-24\")", "Opera (28-36\")", "Rope (37\"+)"])
        pendant_size = st.selectbox("Pendant Size:", ["Small (<1cm)", "Medium (1-3cm)", "Large (3-5cm)", "Extra Large (5cm+)"])
    
    # Budget range
    budget = st.selectbox("Target Price Range:", 
        ["Student Budget (<$100)", "Mid-range ($100-$500)", "Luxury ($500-$2000)", "High Jewelry ($2000+)"])
    
    production_time = st.selectbox("Production Complexity:",
        ["Quick (1-2 weeks)", "Standard (3-4 weeks)", "Complex (1-2 months)", "Masterpiece (3+ months)"])

# Generate Design Specification
if st.button("🎨 Generate Detailed Design Specification", type="primary", use_container_width=True):
    
    with st.spinner("Creating your professional design specification..."):
        time.sleep(2)
        
        # Get template details
        template = DESIGN_TEMPLATES[jewelry_type][design_style]
        material_info = MATERIALS[material]
        stone_info = STONES[primary_stone]
        
        st.markdown("---")
        st.markdown(f'<div class="design-spec-card">', unsafe_allow_html=True)
        
        # Header
        st.markdown(f"## 🎨 {template['name']} - Design Specification")
        st.markdown(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        col_spec1, col_spec2 = st.columns(2)
        
        with col_spec1:
            st.markdown("### 📋 Design Overview")
            st.markdown(f'<div class="spec-item"><strong>Style:</strong> {template["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-item"><strong>Description:</strong> {template["description"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-item"><strong>Best For:</strong> {", ".join(template["best_for"])}</div>', unsafe_allow_html=True)
            
            st.markdown("### 🛠️ Design Elements")
            for element in template["elements"]:
                st.markdown(f"✅ {element}")
        
        with col_spec2:
            st.markdown("### 🎨 Materials & Stones")
            
            # Material with color coding
            st.markdown(f'<div class="spec-item"><strong>Primary Material:</strong> <span class="{material_info["class"]}">{material}</span></div>', unsafe_allow_html=True)
            st.markdown(f"**Properties:** {', '.join(material_info['properties'])}")
            
            # Stone with color coding  
            st.markdown(f'<div class="spec-item"><strong>Primary Stone:</strong> <span class="{stone_info["class"]}">{primary_stone}</span></div>', unsafe_allow_html=True)
            st.markdown(f"**Properties:** {', '.join(stone_info['properties'])}")
            
            # Additional details
            if engraving:
                st.markdown(f'<div class="spec-item"><strong>Engraving:</strong> {engraving}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-item"><strong>Setting:</strong> {setting_type}</div>', unsafe_allow_html=True)
        
        # Technical specs
        st.markdown("### 📐 Technical Specifications")
        col_tech1, col_tech2 = st.columns(2)
        
        with col_tech1:
            st.markdown(f'<div class="spec-item"><strong>Target Audience:</strong> {target_audience}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-item"><strong>Price Range:</strong> {budget}</div>', unsafe_allow_html=True)
        
        with col_tech2:
            st.markdown(f'<div class="spec-item"><strong>Production Time:</strong> {production_time}</div>', unsafe_allow_html=True)
            if jewelry_type == "rings":
                st.markdown(f'<div class="spec-item"><strong>Ring Size:</strong> US {ring_size}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="spec-item"><strong>Band Width:</strong> {band_width}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Student instructions
        st.markdown("---")
        st.subheader("🎓 Student Project Instructions")
        
        st.markdown(f"""
        **Your Design Challenge:**
        Create sketches and technical drawings based on this specification for **{template['name']}**.
        
        **What to Deliver:**
        1. **Concept Sketches** (3 variations based on this spec)
        2. **Technical Drawing** with measurements
        3. **Material Board** showing {material} and {primary_stone}
        4. **Design Rationale** explaining your choices
        
        **Design Focus Areas:**
        - How the {', '.join(template['elements']).lower()} work together
        - Why {material} and {primary_stone} are appropriate
        - How this design appeals to {target_audience.lower()} audience
        """)
        
        # Export option
        spec_data = {
            "design_name": template["name"],
            "description": template["description"],
            "materials": material,
            "stones": primary_stone,
            "specifications": {
                "style": design_style,
                "target_audience": target_audience,
                "budget": budget,
                "production_time": production_time
            }
        }
        
        st.download_button(
            "📥 Download Specification as JSON",
            json.dumps(spec_data, indent=2),
            file_name=f"jewelry_design_spec_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

# Educational content
st.markdown("---")
st.markdown("""
## 🎓 Why This Approach Works for Students:

### ✅ **Real Design Education**
- Learn actual jewelry design principles
- Understand material properties and combinations
- Practice creating technical specifications

### ✅ **Professional Skills**
- Create design briefs like professional jewelers
- Learn to specify materials and techniques
- Develop critical thinking about design choices

### ✅ **Portfolio Ready**
- Generate professional design specifications
- Build a portfolio of design concepts
- Demonstrate understanding of jewelry design

### ✅ **No Fake AI**
- Honest approach that actually teaches design
- Consistent, reliable results
- Focus on learning rather than technology limitations
""")

st.markdown("""
<div style='text-align: center; margin-top: 40px;'>
    <p>💎 <strong>Real Jewelry Design Education</strong> - No more fake AI, just real learning!</p>
</div>
""", unsafe_allow_html=True)
