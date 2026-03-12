import streamlit as st
import qrcode
from io import BytesIO

def show():
    ACCENT = st.session_state.get("accent_color", "#6366f1")
    st.markdown(f"### 📱 QR Code Generator")
    st.markdown("---")
    
    data = st.text_input("Enter URL or Text:", placeholder="https://example.com")
    
    if data:
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to buffer
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        # Display - centered and constrained
        st.markdown("<div style='display:flex; flex-direction:column; align-items:center;'>", unsafe_allow_html=True)
        st.image(byte_im, width=400)
        st.markdown(f"<p style='color:#10b981; font-weight:700;'>✅ QR Code Ready</p>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download QR Code",
            data=byte_im,
            file_name="nova_qr.png",
            mime="image/png",
            use_container_width=False
        )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Enter data above to generate your QR code.")
