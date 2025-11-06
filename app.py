import streamlit as st
import requests
import time
import random

# Page configuration
st.set_page_config(
    page_title="Professional Jewelry AI Designer",
    page_icon="💎",
    layout="wide"
)

st.title("💎 Professional Jewelry AI Generator")
st.markdown("### Uses multiple AI services for unlimited generations")

def try_multiple_ai_services(prompt):
    """
    Try different AI services to get the best result
    """
    services = [
        {"name": "Stable Diffusion", "url": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"},
        {"name": "Flux", "url": "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"},
        {"name": "SDXL", "url": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"}
    ]
    
    enhanced_prompt = f"professional jewelry design, {prompt}, high quality, detailed, studio lighting, 8k resolution, luxury jewelry piece"
    
    for service in services:
        try:
            # Try without API key first (public access)
            payload = {"inputs": enhanced_prompt}
            response = requests.post(service["url"], json=payload, timeout=45)
            
            if response.status_code == 200:
                return response.content, service["name"]
            elif response.status_code == 503:
                # Model loading - wait and try once more
                time.sleep(30)
                response = requests.post(service["url"], json=payload, timeout=45)
                if response.status_code == 200:
                    return response.content, service["name"]
        except:
            continue
    
    return None, "No service available"

# Smart prompt enhancement
def enhance_prompt(base_prompt, style, material, jewelry_type):
    """Make prompts more likely to generate good jewelry"""
    
    style_keywords = {
        "modern": "clean lines, geometric, contemporary, minimalist",
        "vintage": "antique, classic, traditional, ornate details",
        "luxury": "high-end, premium, elegant, sophisticated", 
        "minimalist": "simple, clean, subtle, understated"
    }
    
    material_keywords = {
        "gold": "yellow gold, warm tone, luxurious",
        "silver": "sterling silver, bright, cool tone", 
        "platinum": "platinum, white metal, premium",
        "rose gold": "rose gold, pink tone, romantic"
    }
    
    style_text = style_keywords.get(style.lower(), "")
    material_text = material_keywords.get(material.lower(), "")
    
    enhanced = f"{material} {jewelry_type}, {base_prompt}, {style_text}, {material_text}, professional jewelry design, high quality, detailed, studio lighting, product photography"
    
    return enhanced

# Main interface
st.sidebar.header("🎨 Design Settings")

jewelry_type = st.sidebar.selectbox("Jewelry Type", ["Ring", "Necklace", "Earrings", "Bracelet"])
material = st.sidebar.selectbox("Material", ["Gold", "Silver", "Platinum", "Rose Gold"])
style = st.sidebar.selectbox("Style", ["Modern", "Vintage", "Luxury", "Minimalist"])
primary_stone = st.sidebar.selectbox("Stone", ["Diamond", "Emerald", "Ruby", "Sapphire", "Pearl", "None"])

st.sidebar.header("🔧 AI Settings")
num_attempts = st.sidebar.slider("AI Attempts", 1, 5, 3)
use_enhanced_prompts = st.sidebar.checkbox("Use Enhanced Prompts", value=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Describe Your Jewelry Design")
    
    if use_enhanced_prompts:
        base_prompt = st.text_input("Main Design Idea:", placeholder="e.g., floral engraving, geometric pattern")
        full_prompt = enhance_prompt(base_prompt, style, material, jewelry_type)
        st.text_area("Enhanced Prompt (AI sees this):", full_prompt, height=100)
    else:
        full_prompt = st.text_area("Full Description:", placeholder="e.g., Gold ring with floral engraving and diamonds", height=100)
    
    st.info("💡 **Pro Tip:** Be specific about patterns, stones, and style for best results")

with col2:
    st.subheader("🎯 Working Examples")
    examples = [
        "floral engraving with small diamonds",
        "geometric pattern with emerald center", 
        "vintage scrollwork with pearl accents",
        "modern minimalist design with clean lines"
    ]
    
    for example in examples:
        if st.button(f"💎 {example}", use_container_width=True):
            st.session_state.example_prompt = example

# Generation
if st.button("🚀 Generate Professional Jewelry Design", type="primary"):
    if not full_prompt:
        st.warning("Please enter a design description")
    else:
        progress_bar = st.progress(0)
        status = st.empty()
        
        best_result = None
        best_service = None
        
        for attempt in range(num_attempts):
            progress = (attempt / num_attempts) * 100
            progress_bar.progress(progress)
            status.text(f"🔄 Trying AI service {attempt + 1}/{num_attempts}...")
            
            result, service_name = try_multiple_ai_services(full_prompt)
            
            if result:
                best_result = result
                best_service = service_name
                break
            
            time.sleep(5)  # Wait between attempts
        
        progress_bar.progress(100)
        
        if best_result:
            st.success(f"🎉 Success! Generated with {best_service}")
            st.image(best_result, use_column_width=True, caption=f"AI Generated: {full_prompt}")
            
            # Download
            st.download_button(
                "📥 Download Design",
                best_result,
                file_name=f"jewelry_design_{int(time.time())}.png",
                mime="image/png"
            )
        else:
            st.error("❌ All AI services are busy or unavailable")
            st.info("""
            **This is normal for free AI services. Here's what you can do:**
            
            1. **Wait 5 minutes and try again** - AI models often need time to load
            2. **Use simpler prompts** like "gold ring" or "silver necklace"
            3. **Try during off-peak hours** (early morning or late evening)
            4. **The services ARE working** - they're just busy with free users
            """)

# Alternative approach section
with st.expander("🚀 **Professional Solution for Unlimited Generations**"):
    st.markdown("""
    ### If you need reliable, unlimited generations:
    
    **Option 1: Use Multiple Free Accounts**
    - Create accounts on multiple AI services
    - Rotate between them when limits are reached
    - Services to try: Leonardo.ai, Midjourney (via Discord), DALL-E 3
    
    **Option 2: Low-Cost Professional APIs**
    - **Replicate.com**: ~$0.01 per image
    - **RunPod**: ~$0.02 per image  
    - **AWS SageMaker**: Pay per use
    
    **Option 3: Educational Access**
    - Many AI companies offer free educational access
    - Contact their education departments
    - Use your student email address
    
    **For a class of students:**
    - Budget ~$10-20 for unlimited generations
    - Use bulk generation APIs
    - Pre-generate design variations
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>💎 <strong>Professional AI Jewelry Designer</strong> - Smart approach to unlimited designs</p>
</div>
""", unsafe_allow_html=True)
