import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات التصميم (تحويل للأبيض والأزرق المريح)
st.set_page_config(page_title="بوابة الصحة الرقمية التونسية", layout="centered")

st.markdown("""
    <style>
    /* تغيير الخلفية للأبيض المريح */
    .stApp { background-color: #f0f7ff; }
    
    /* تنسيق العناوين باللون الأزرق الطبي */
    h1 { color: #0056b3; text-align: center; font-family: 'Arial'; }
    h3 { color: #444; text-align: center; }

    /* تنسيق الخانات لتكون واضحة */
    .stTextInput>div>div>input {
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }

    /* الزر الأخضر الجميل */
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        height: 3.5em !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة حفظ البيانات الآمنة
def save_data_safely(f_name, l_name, id_no, ph, dept, pr, t_id):
    file_name = 'hospital_records.csv'
    header = ['التاريخ', 'الاسم', 'اللقب', 'الهوية', 'الهاتف', 'القسم', 'المعلوم', 'رقم التذكرة']
    new_data = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), f_name, l_name, id_no, ph, dept, pr, t_id]
    try:
        if not os.path.isfile(file_name):
            pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')
        else:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
            df = pd.concat([df, pd.DataFrame([new_data], columns=header)], ignore_index=True)
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
    except Exception:
        pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')

# --- الجانب المخفي للإدارة ---
with st.sidebar:
    st.header("⚙️ الإدارة")
    show_admin = st.checkbox("لوحة الموظفين")
    admin_pass = ""
    if show_admin:
        admin_pass = st.text_input("كلمة السر", type="password")

# --- الواجهة الرئيسية (واجهة المريض المبهجة) ---
# إضافة صورة طبيب (رابط صورة تعبيرية)
st.image("https://img.freepik.com/free-photo/smiling-doctor-with-stethoscope-isolated-grey_651396-974.jpg", width=150)

st.title("🏥 مرحبا بك في بوابة الصحة الرقمية")
st.subheader("نحن هنا لخدمتكم وتسهيل إجراءاتكم")

with st.container():
    with st.form("happy_patient_form"):
        # الترتيب: اسم -> لقب -> بطاقة تعريف -> هاتف
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("👤 الاسم الأول")
            id_card = st.text_input("🪪 رقم بطاقة التعريف")
        with col2:
            last_name = st.text_input("👤 اللقب")
            phone = st.text_input("📞 رقم الهاتف")
        
        dept = st.selectbox("🏥 القسم المطلوب مراجعته", ["الاستعجالي", "طب العيون", "طب الأطفال", "الجراحة العامة"])
        prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "الجراحة العامة": "20.000"}
        
        st.write(f"💵 المعلوم المطلوب: **{prices[dept]} DT**")
        
        submitted = st.form_submit_button("✅ تأكيد التسجيل واستخراج التذكرة")

if submitted:
    if first_name and last_name and id_card:
        t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}"
        save_data_safely(first_name, last_name, id_card, phone, dept, prices[dept], t_id)
        
        # إنشاء QR Code
        qr_img = qrcode.make(f"Patient: {first_name} {last_name}\nID: {id_card}\nTicket: {t_id}")
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        
        st.balloons() # احتفال بسيط بالنجاح
        st.success(f"ممتاز يا {first_name}! تم حجز موعدك بنجاح. رقم تذكرتك: {t_id}")
        
        st.image(buf.getvalue(), width=200, caption="تذكرتك الرقمية")
        
        st.download_button(
            label="📥 حفظ التذكرة في هاتفك",
            data=buf.getvalue(),
            file_name=f"Hospital_Ticket_{t_id}.png",
            mime="image/png",
            on_click=lambda: st.toast("تم الحفظ بنجاح! تمنياتنا بالشفاء العاجل", icon='💙')
        )
    else:
        st.error("الرجاء إكمال البيانات الأساسية")

# لوحة الإدارة (محمية)
if show_admin and admin_pass == "2026":
    st.divider()
    st.subheader("📋 سجل المراجعات اليومي")
    if os.path.exists('hospital_records.csv'):
        st.dataframe(pd.read_csv('hospital_records.csv', encoding='utf-8-sig'), use_container_width=True)
