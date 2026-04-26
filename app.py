import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات الصفحة والتصميم (المحافظة على المظهر الاحترافي)
st.set_page_config(page_title="بوابة الصحة التونسية الرقمية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; }
    .stButton>button {
        width: 100%; background-color: #00d4ff; color: black;
        font-weight: bold; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. وظائف قاعدة البيانات (لحفظ السجلات)
def save_to_database(name, id_card, dept, price, t_id):
    file_name = 'hospital_records.csv'
    new_entry = pd.DataFrame([[datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), name, id_card, dept, price, t_id]], 
                            columns=['التاريخ', 'الاسم', 'الهوية', 'القسم', 'المعلوم', 'رقم التذكرة'])
    
    if not os.path.isfile(file_name):
        new_entry.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        new_entry.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')

# 3. واجهة التطبيق بنظام التبويبات (Tabs)
st.title("🏥 المنظومة الرقمية المتكاملة للصحة")
tab1, tab2 = st.tabs(["📝 تسجيل مريض جديد", "📋 سجل المستشفى"])

with tab1:
    st.subheader("الرجاء إدخال بيانات المريض")
    with st.form("patient_registration"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 الاسم واللقب الكامل")
            id_card = st.text_input("🪪 رقم بطاقة التعريف الوطنية")
        with col2:
            dept = st.selectbox("🏥 القسم المطلوب", 
                                ["الاستعجالي", "طب العيون", "طب الأطفال", "قسم الجراحة", "الأمراض الباطنية"])
            prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "قسم الجراحة": "20.000", "الأمراض الباطنية": "12.000"}
            current_price = f"{prices[dept]} DT"
            st.metric("معلوم الكشف التقديري", current_price)

        submitted = st.form_submit_button("تأكيد الترسيم واستخراج التذكرة")

    if submitted:
        if name and id_card:
            # توليد رقم تذكرة فريد
            t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}-{id_card[-3:]}"
            
            # حفظ البيانات في ملف CSV (قاعدة البيانات)
            save_to_database(name, id_card, dept, current_price, t_id)
            
            # توليد الـ QR Code
            qr_content = f"المريض: {name}\nالهوية: {id_card}\nالقسم: {dept}\nالمعلوم: {current_price}\nالمرجع: {t_id}"
            qr = qrcode.make(qr_content)
            buf = BytesIO()
            qr.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # عرض النتائج
            st.success(f"✅ تم التسجيل بنجاح! رقم تذكرتك: {t_id}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.image(byte_im, caption="رمز QR الخاص بالتذكرة", width=250)
            with c2:
                st.info(f"المريض: {name}\n\nالقسم: {dept}\n\nالمبلغ: {current_price}")
                # إعادة ميزة تحميل التذكرة التي فُقدت
                st.download_button(
                    label="📥 تحميل التذكرة (PNG)",
                    data=byte_im,
                    file_name=f"Ticket_{t_id}.png",
                    mime="image/png"
                )
        else:
            st.error("⚠️ يرجى ملء البيانات المطلوبة")

with tab2:
    st.subheader("📊 لوحة تحكم الإدارة (سجل المعاملات)")
    if os.path.isfile('hospital_records.csv'):
        df = pd.read_csv('hospital_records.csv')
        st.dataframe(df, use_container_width=True)
        # ميزة إضافية: تحميل السجل الكامل للإدارة
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        st.download_button("📥 تحميل سجل البيانات الكامل (Excel/CSV)", data=csv_buffer.getvalue(), file_name="hospital_report.csv", mime="text/csv")
    else:
        st.info("لا توجد سجلات مسجلة حتى الآن.")
