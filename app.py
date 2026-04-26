import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# إعدادات التصميم (خلفية بيضاء، خانات سوداء، وزر فاتح كما في الصورة)
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

    /* 1. خانات إدخال البيانات - تظل سوداء بنص أبيض */
    .stTextInput>div>div>input {
        background-color: #1a1c23 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-radius: 10px !important;
    }

    /* 2. خانة اختيار القسم - تظل سوداء بنص أبيض */
    div[data-baseweb="select"] > div {
        background-color: #1a1c23 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-radius: 10px !important;
    }

    /* 3. زر الترسيم - تعديل ليصبح بخلفية فاتحة كما في الصورة الأخيرة */
    div.stButton > button {
        background-color: #f0f2f6 !important; /* خلفية فاتحة مريحة */
        color: #1a1c23 !important;           /* نص داكن واضح */
        border: 1px solid #d1d5db !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        height: 3em !important;
        width: 100% !important;
    }

    /* تنسيق القوائم المنسدلة */
    div[data-baseweb="popover"] li {
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

with st.form("final_form_style"):
    first_name = st.text_input("👤 الاسم الأول")
    last_name = st.text_input("👤 اللقب")
    id_card = st.text_input("🪪 رقم بطاقة التعريف")
    phone = st.text_input("📞 رقم الهاتف")
    st.divider()
    dept = st.selectbox("🏥 القسم المطلوب مراجعته", ["الاستعجالي", "طب العيون", "طب الأطفال", "الجراحة العامة"])
    prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "الجراحة العامة": "20.000"}
    st.markdown(f"💰 المعلوم المطلوب: **{prices[dept]} DT**")
    
    # الزر الآن سيظهر بالشكل الفاتح المطلوب
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
