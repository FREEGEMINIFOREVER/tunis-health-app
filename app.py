import streamlit as st
import qrcode
from io import BytesIO

# التنسيق النهائي: بسيط، أنيق، وواضح
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    /* صورة الطبيب كبيرة في المركز */
    .centered-img { display: block; margin: auto; width: 250px; border-radius: 15px; border: 2px solid #28a745; }
    /* نصوص الخانات بيضاء ناصعة */
    input { color: white !important; background-color: #1e1e1e !important; }
    /* ثمن التسجيل بارز */
    .price-tag { text-align: center; color: #28a745; font-size: 28px; font-weight: bold; padding: 10px; border: 1px solid #28a745; border-radius: 10px; margin: 20px 0; }
    /* زر أخضر عريض */
    .stButton>button { background-color: #28a745 !important; color: white !important; width: 100%; height: 55px; font-size: 20px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 1. الصورة الرئيسية (طبيب)
st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png" class="centered-img">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>بوابة تسجيل المرضى</h1>", unsafe_allow_html=True)

# 2. البيانات بالترتيب المطلوب
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("1. الاسم")
    cin = st.text_input("3. رقم بطاقة التعريف")
with col2:
    prenom = st.text_input("2. اللقب")
    phone = st.text_input("4. رقم الهاتف")

dept = st.selectbox("القسم المطلوب", ["قسم العظام", "قسم القلب", "الجراحة العامة"])

# 3. الثمن
st.markdown('<div class="price-tag">المبلغ المطلوب: 20.000 د.ت</div>', unsafe_allow_html=True)

# 4. التنفيذ والـ QR والإشعار
if st.button("الترسيم والاستخلاص"):
    if nome and prenom and cin:
        # توليد الكود
        qr_img = qrcode.make(f"المريض: {nome} {prenom}\nالتعريف: {cin}\nالقسم: {dept}")
        buf = BytesIO()
        qr_img.save(buf)
        
        # إشعار التنزيل الفوري
        st.toast("✅ تم تنزيل كود الترسيم بنجاح على هاتفك", icon='📥')
        
        st.download_button(label="📥 اضغط هنا لتحميل الكود", data=buf.getvalue(), file_name="patient_qr.png", mime="image/png")
    else:
        st.error("الرجاء إكمال البيانات")
