import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات التصميم (إصلاح الألوان لتكون واضحة جداً)
st.set_page_config(page_title="بوابة الصحة الرقمية", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* جعل كل النصوص باللون الأسود الواضح */
    label, p, span, div { 
        color: #1a1a1a !important; 
        font-weight: 500 !important;
    }
    
    /* تنسيق العنوان الرئيسي */
    h1 { color: #004085 !important; text-align: center; font-size: 2.5rem; }
    h3 { color: #0056b3 !important; text-align: center; }

    /* تكبير وتنسيق صورة الطبيب */
    .doc-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 300px;
        border-radius: 15px;
    }

    /* الزر الأخضر الواضح */
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        width: 100% !important;
        border: none !important;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة حفظ البيانات
def save_data_safely(f_name, l_name, id_no, ph, dept, pr, t_id):
    file_name = 'hospital_records.csv'
    header = ['التاريخ', 'الاسم', 'الالقب', 'الهوية', 'الهاتف', 'القسم', 'المعلوم', 'رقم التذكرة']
    new_data = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), f_name, l_name, id_no, ph, dept, pr, t_id]
    try:
        if not os.path.isfile(file_name):
            pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')
        else:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
            df = pd.concat([df, pd.DataFrame([new_data], columns=header)], ignore_index=True)
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
    except:
        pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')

# --- الواجهة الرئيسية ---
# عرض صورة الطبيب بشكل كبير في المنتصف
st.markdown('<img src="https://img.freepik.com/free-photo/smiling-doctor-with-stethoscope-isolated-grey_651396-974.jpg" class="doc-img">', unsafe_allow_html=True)

st.title("🏥 مرحبا بك في بوابة الصحة الرقمية")
st.subheader("نحن هنا لخدمتكم وتسهيل إجراءاتكم")

with st.form("main_registration_form"):
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
    
    st.write(f"💰 المعلوم المطلوب: **{prices[dept]} DT**")
    
    submitted = st.form_submit_button("تأكيد التسجيل واستخراج التذكرة ✅")

if submitted:
    if first_name and last_name and id_card:
        t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}"
        save_data_safely(first_name, last_name, id_card, phone, dept, prices[dept], t_id)
        
        qr_img = qrcode.make(f"Patient: {first_name} {last_name}\nID: {id_card}\nTicket: {t_id}")
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        
        st.balloons()
        st.success(f"شكرًا لك {first_name}! تم التسجيل بنجاح.")
        st.image(buf.getvalue(), width=200)
        
        st.download_button(
            label="📥 اضغط هنا لحفظ التذكرة على هاتفك",
            data=buf.getvalue(),
            file_name=f"Ticket_{t_id}.png",
            mime="image/png",
            on_click=lambda: st.toast("تم الحفظ بنجاح!", icon='💾')
        )
    else:
        st.error("الرجاء تعمير كافة البيانات المطلوبة")

# زر الإدارة مخفي في الأسفل تماماً
with st.expander("🔐 لوحة التحكم (للموظفين فقط)"):
    pw = st.text_input("كلمة السر", type="password")
    if pw == "2026":
        if os.path.exists('hospital_records.csv'):
            st.dataframe(pd.read_csv('hospital_records.csv', encoding='utf-8-sig'))
