import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# إعدادات الصفحة
st.set_page_config(page_title="بوابة الصحة التونسية - نظام البيانات", layout="wide")

# دالة لحفظ البيانات في ملف
def save_data(name, id_card, dept, t_id):
    file_name = 'hospital_records.csv'
    new_data = pd.DataFrame([[datetime.datetime.now(), name, id_card, dept, t_id]], 
                            columns=['التاريخ', 'الاسم', 'الهوية', 'القسم', 'رقم التذكرة'])
    
    if not os.path.isfile(file_name):
        new_data.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')

st.title("🏥 نظام إدارة المرضى المطور")

tab1, tab2 = st.tabs(["📑 استخراج تذكرة", "📊 سجل البيانات (للمسؤولين)"])

with tab1:
    with st.form("main_form"):
        name = st.text_input("الاسم واللقب")
        id_card = st.text_input("رقم بطاقة التعريف")
        dept = st.selectbox("القسم", ["الاستعجالي", "العيون", "الأطفال"])
        submit = st.form_submit_button("تأكيد التسجيل")

    if submit and name and id_card:
        t_id = f"TN-{id_card[-3:]}-{datetime.datetime.now().second}"
        save_data(name, id_card, dept, t_id) # حفظ في قاعدة البيانات
        st.success(f"تم حفظ البيانات واستخراج التذكرة: {t_id}")
        
        # توليد QR Code (نفس الكود السابق)
        qr_content = f"ID: {t_id} | Name: {name}"
        qr = qrcode.make(qr_content)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=200)

with tab2:
    st.subheader("سجل المرضى المسجلين اليوم")
    if os.path.isfile('hospital_records.csv'):
        df = pd.read_csv('hospital_records.csv')
        st.dataframe(df) # عرض الجدول للمسؤول
    else:
        st.info("لا توجد بيانات مسجلة بعد.")
