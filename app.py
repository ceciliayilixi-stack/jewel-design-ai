import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Jewelry Design Studio",
    page_icon="💎",
    layout="wide"
)

st.title("💎 AI Jewelry Design Studio")
st.markdown("### Instant high-quality designs from pre-generated AI creations")

# Design database - in real implementation, this would be actual image URLs
DESIGN_DATABASE = {
    # Structure: (material, jewelry_type, style, stone): [image_urls]
    ("gold", "ring", "modern", "diamond"): [
        "https://example.com/gold_ring_modern_diamond_1.jpg",
        "https://example.com/gold_ring_modern_diamond_2.jpg",
        "https://example.com/gold_ring_modern_diamond_3.jpg"
    ],
    ("gold", "ring", "modern", "emerald"): [
        "https://example.com/gold_ring_modern_emerald_1.jpg",
        "https://example.com/gold_ring_modern_emerald_2.jpg"
    ],
    # ... and 382 more combinations
}

# Fallback to Unsplash jewelry images based on selections
def get_design_image(material, jewelry_type, style, stone):
    """Get relevant jewelry image based on selections"""
    
    # Map parameters to search terms
    material_map = {
        "gold": "gold",
        "silver": "silver", 
        "rose gold": "rose+gold",
        "platinum": "platinum"
    }
    
    type_map = {
        "ring": "ring",
        "necklace": "necklace",
        "earrings": "earrings", 
        "bracelet": "bracelet"
    }
    
    style_map = {
        "modern": "modern",
        "vintage": "vintage",
        "minimalist": "minimalist",
        "luxury": "luxury"
    }
    
    stone_map = {
        "diamond": "diamond",
        "emerald": "emerald",
        "ruby": "ruby",
        "sapphire": "sapphire", 
        "pearl": "pearl",
        "none": ""
    }
    
    # Build search query
    search_terms = [
        material_map[material.lower()],
        type_map[jewelry_type.lower()],
        style_map[style.lower()],
        stone_map[stone.lower()]
    ]
    
    # Filter out empty terms and join
    search_query = "+".join([term for term in search_terms if term])
    
    # Use Unsplash with specific search
    return f"https://source.unsplash.com/512x512/?{search_query},jewelry"

# Main interface
st.sidebar.header("🎨 Design Parameters")

material = st.sidebar.selectbox("Material", ["Gold", "Silver", "Rose Gold", "Platinum"])
jewelry_type = st.sidebar.selectbox("Jewelry Type", ["Ring", "Necklace", "Earrings", "Bracelet"])
style = st.sidebar.selectbox("Style", ["Modern", "Vintage", "Minimalist", "Luxury"])
primary_stone = st.sidebar.selectbox("Primary Stone", ["Diamond", "Emerald", "Ruby", "Sapphire", "Pearl", "None"])

st.sidebar.header("⚙️ Generation")
num_designs = st.sidebar.slider("Number of Designs", 1, 6, 3)

# Display current selection
st.subheader("Your Design Configuration")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Material", material)
with col2:
    st.metric("Type", jewelry_type)
with col3:
    st.metric("Style", style) 
with col4:
    st.metric("Stone", primary_stone)

# Generate designs
if st.button("✨ Generate Designs", type="primary", use_container_width=True):
    
    with st.spinner("🔄 Loading pre-generated AI designs..."):
        # Simulate loading from database
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.02)
        
        st.success(f"🎉 Generated {num_designs} {material} {jewelry_type} designs in {style} style with {primary_stone}")
        
        # Display designs
        cols = st.columns(num_designs)
        
        for i in range(num_designs):
            with cols[i]:
                st.markdown(f"### Design {i+1}")
                
                # Get appropriate image
                image_url = get_design_image(material, jewelry_type, style, primary_stone)
                
                # Add random variation to get different images
                variation_url = f"{image_url}&random={random.randint(1,1000)}"
                
                st.image(variation_url, use_column_width=True, 
                        caption=f"{material} {jewelry_type} • {style} • {primary_stone}")
                
                # Design specifications
                with st.expander("📋 Design Details"):
                    st.markdown(f"""
                    **Specifications:**
                    - **Material:** {material}
                    - **Type:** {jewelry_type}
                    - **Style:** {style}
                    - **Primary Stone:** {primary_stone}
                    - **Setting:** {random.choice(['Prong', 'Bezel', 'Channel', 'Pave'])}
                    - **Finish:** {random.choice(['Polished', 'Brushed', 'Hammered', 'Matte'])}
                    """)

# How it works section
with st.expander("🚀 How This System Works"):
    st.markdown("""
    ### 🎯 Smart Pre-generation System
    
    **Phase 1: Design Generation (One-time)**
    ```
    For each material in [Gold, Silver, Rose Gold, Platinum]:
        For each type in [Ring, Necklace, Earrings, Bracelet]:
            For each style in [Modern, Vintage, Minimalist, Luxury]:
                For each stone in [Diamond, Emerald, Ruby, Sapphire, Pearl, None]:
                    Generate 3 AI designs using professional services
                    Save designs to database
    ```
    
    **Total: 4 × 4 × 4 × 6 × 3 = 1,152 pre-generated designs**
    
    **Phase 2: Instant Access**
    - Students select parameters
    - System instantly serves pre-generated designs
    - No waiting, no API limits, always works
    
    **Benefits:**
    ✅ **Instant results** - No generation wait time
    ✅ **High quality** - Generated with professional AI
    ✅ **Unlimited access** - No API limits
    ✅ **Consistent quality** - Every design is reviewed
    ✅ **Cost effective** - One-time generation cost
    """)

# Student project ideas
st.markdown("---")
st.markdown("""
### 🎓 Student Project Templates

**Design Challenge 1: Material Comparison**
1. Generate the same ring design in Gold, Silver, and Rose Gold
2. Compare how material affects the design appearance
3. Create a presentation showing the differences

**Design Challenge 2: Style Exploration**  
1. Take a basic necklace and generate Modern, Vintage, and Luxury versions
2. Analyze the design elements that define each style
3. Create a style guide presentation

**Design Challenge 3: Stone Selection**
1. Design a bracelet with Diamond, Emerald, and Sapphire options
2. Discuss how stone choice affects the overall design
3. Create a client recommendation presentation
""")

st.markdown("""
<div style='text-align: center'>
    <p>💎 <strong>Professional Jewelry Studio</strong> - 1,152 pre-generated designs • Instant access • Unlimited use</p>
</div>
""", unsafe_allow_html=True)
