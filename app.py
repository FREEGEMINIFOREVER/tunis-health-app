import streamlit as st
import qrcode
from io import BytesIO
import datetime

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="بوابة المريض التونسي الرقمية", layout="centered")

# تصميم الواجهة (CSS) لجعلها تبدو كأنظمة المستشفيات الحديثة
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; font-family: 'Arial'; }
    .stButton>button {
        width: 100%;
        background-color: #00d4ff;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 بوابة المريض التونسي الرقمية")
st.write("---")

# نموذج إدخال البيانات المطور
with st.container():
    name = st.text_input("👤 الاسم واللقب الكامل")
    id_card = st.text_input("🪪 رقم بطاقة التعريف الوطنية")
    
    col1, col2 = st.columns(2)
    with col1:
        dept = st.selectbox("🏥 القسم المطلوب", 
                            ["الاستعجالي", "طب العيون", "طب الأطفال", "قسم الجراحة", "الأمراض الباطنية"])
    with col2:
        # نظام تسعير آلي بناءً على القسم
        prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "قسم الجراحة": "20.000", "الأمراض الباطنية": "12.000"}
        st.metric("معلوم الكشف", f"{prices[dept]} DT")

    st.write("---")
    submitted = st.button("تأكيد الترسيم واستخراج التذكرة")

if submitted:
    if name and id_card:
        # إنشاء معرف فريد للتذكرة
        timestamp = datetime.datetime.now().strftime("%y%m%d%H%M")
        ticket_id = f"T-TN-{timestamp}-{id_card[-3:]}"
        
        # تحضير بيانات الـ QR المتقدمة
        qr_content = f"المؤسسة: وزارة الصحة التونسية\nالمريض: {name}\nالهوية: {id_card}\nالقسم: {dept}\nالمرجع: {ticket_id}"
        
        # توليد الـ QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # حفظ الصورة في الذاكرة للتحميل
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # عرض النتائج للمستخدم
        st.success(f"✅ تم تأكيد موعدك بنجاح! رقم المرجع: {ticket_id}")
        st.image(byte_im, caption="امسح الرمز عند وصولك للمستشفى", width=300)
        
        # زر التحميل الفوري
        st.download_button(
            label="📥 تحميل التذكرة الرقمية (PNG)",
            data=byte_im,
            file_name=f"Ticket_{name}.png",
            mime="image/png"
        )
    else:
        st.error("⚠️ يرجى التأكد من ملء جميع الخانات")
