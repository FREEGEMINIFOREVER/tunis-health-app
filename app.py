import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="بوابة الصحة الرقمية", layout="centered")

# 2. تصميم CSS مركز ونظيف (الزر الأبيض هو الأولوية)
st.markdown("""
    <style>
    /* خلفية الموقع */
    .stApp { background-color: #ffffff !important; }
    
    /* النصوص السوداء */
    h1, label, p, span { color: #000000 !important; font-weight: bold; }

    /* تنسيق الخانات (سوداء بنص أبيض) */
    .stTextInput input, div[data-baseweb="select"] > div {
        background-color: #1a1c23 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
    }

    /* --- تنسيق الزر المستهدف (الحل النهائي للرؤية) --- */
    div.stButton > button {
        background-color: #ffffff !important; /* خلفية بيضاء ناصعة */
        color: #000000 !important;           /* نص أسود فاحم */
        border: 3px solid #000000 !important; /* إطار أسود غليظ للوضوح */
        width: 100% !important;
        height: 4em !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.2) !important;
    }

    /* إجبار أي نص داخل الزر على السواد التام */
    div.stButton > button p {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        margin: 0 !important;
    }
    
    /* قائمة الأقسام المنسدلة */
    div[data-baseweb="popover"] li {
        color: #ffffff !important;
        background-color: #1a1c23 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. وظيفة حفظ البيانات
def save_data(f_name, l_name, id_no, ph, dept, pr, t_id):
    file_name = 'hospital_records.csv'
    header = ['التاريخ', 'الاسم', 'اللقب', 'الهوية', 'الهاتف', 'القسم', 'المعلوم', 'رقم التذكرة']
    new_record = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), f_name, l_name, id_no, ph, dept, pr, t_id]
    try:
        df = pd.read_csv(file_name) if os.path.exists(file_name) else pd.DataFrame(columns=header)
        df = pd.concat([df, pd.DataFrame([new_record], columns=header)], ignore_index=True)
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
    except:
        pass

# 4. واجهة المستخدم
st.markdown("<h1 style='text-align: center;'>الصحة الرقمية</h1>", unsafe_allow_html=True)

with st.form("clean_form"):
    # الخانات السوداء
    col1, col2 = st.columns(2)
    with col1:
        f_name = st.text_input("👤 الاسم الأول")
    with col2:
        l_name = st.text_input("👤 اللقب")
        
    id_card = st.text_input("🪪 رقم بطاقة التعريف")
    phone = st.text_input("📞 رقم الهاتف")
    
    st.divider()
    
    # اختيار القسم
    dept = st.selectbox("🏥 القسم المطلوب مراجعته", ["الاستعجالي", "طب العيون", "طب الأطفال", "الجراحة العامة"])
    prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "الجراحة العامة": "20.000"}
    st.markdown(f"💰 المعلوم المطلوب: **{prices[dept]} DT**")
    
    # الزر الأبيض (الذي كان غير مرئي سابقاً)
    submitted = st.form_submit_button("تأكيد التسجيل واستخراج التذكرة")

# 5. معالجة الضغط على الزر
if submitted:
    if f_name and l_name and id_card:
        ticket_id = f"TN-{datetime.datetime.now().strftime('%M%S')}"
        save_data(f_name, l_name, id_card, phone, dept, prices[dept], ticket_id)
        
        qr = qrcode.make(f"ID: {id_card}\nTicket: {ticket_id}")
        buf = BytesIO()
        qr.save(buf, format="PNG")
        
        st.success("تم التسجيل!")
        st.image(buf.getvalue(), width=200)
    else:
        st.error("يرجى ملء البيانات الأساسية")
