import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# إعدادات التصميم (إجبار الكتابة البيضاء داخل الخانات السوداء)
st.set_page_config(page_title="بوابة الصحة الرقمية", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    h1, label, p, span, .stMarkdown { color: #000000 !important; font-weight: bold; }
    
    .doc-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 300px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    /* --- الحل النهائي للكتابة البيضاء --- */
    
    /* 1. خانات النص (الاسم، اللقب، إلخ) */
    .stTextInput>div>div>input {
        background-color: #1a1c23 !important;
        color: #ffffff !important; /* أبيض ناصع */
        -webkit-text-fill-color: #ffffff !important; /* لضمان اللون في هواتف أندرويد */
    }

    /* 2. خانة القسم (Selectbox) - إصلاح اللون المفقود */
    div[data-baseweb="select"] > div {
        background-color: #1a1c23 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* 3. زر الترسيم */
    div.stButton > button {
        background-color: #1a1c23 !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* ضمان ظهور النص الأبيض داخل القائمة المنسدلة عند فتحها */
    div[data-baseweb="popover"] li, 
    div[role="listbox"] div {
        color: #ffffff !important;
        background-color: #1a1c23 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة حفظ البيانات
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
    except:
        pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')

# الواجهة
st.markdown('<img src="https://img.freepik.com/free-photo/smiling-doctor-with-stethoscope-isolated-grey_651396-974.jpg" class="doc-img">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>الصحة الرقمية</h1>", unsafe_allow_html=True)

with st.form("all_black_fields_final"):
    first_name = st.text_input("👤 الاسم الأول")
    last_name = st.text_input("👤 اللقب")
    id_card = st.text_input("🪪 رقم بطاقة التعريف")
    phone = st.text_input("📞 رقم الهاتف")
    st.divider()
    dept = st.selectbox("🏥 القسم المطلوب مراجعته", ["الاستعجالي", "طب العيون", "طب الأطفال", "الجراحة العامة"])
    prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "الجراحة العامة": "20.000"}
    st.markdown(f"💰 المعلوم المطلوب: **{prices[dept]} DT**")
    submitted = st.form_submit_button("تأكيد التسجيل واستخراج التذكرة")

if submitted:
    if first_name and last_name and id_card:
        t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}"
        save_data_safely(first_name, last_name, id_card, phone, dept, prices[dept], t_id)
        qr_img = qrcode.make(f"Patient: {first_name} {last_name}\nID: {id_card}\nTicket: {t_id}")
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        st.success("تم التسجيل!")
        st.image(buf.getvalue(), width=200)
        st.download_button("📥 تحميل التذكرة", buf.getvalue(), f"Ticket_{t_id}.png", "image/png")
    else:
        st.error("الرجاء تعمير كافة البيانات")
