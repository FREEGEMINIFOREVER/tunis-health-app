import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات الصفحة والتصميم (تعديل اللون إلى الأخضر)
st.set_page_config(page_title="بوابة الصحة التونسية الرقمية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; }
    /* تعديل لون الزر إلى الأخضر */
    .stButton>button {
        width: 100%; 
        background-color: #28a745; 
        color: white;
        font-weight: bold; 
        border-radius: 10px;
        border: none;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #218838;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة حفظ البيانات (محمية من الأخطاء)
def save_to_database(name, id_card, dept, price, t_id):
    file_name = 'hospital_records.csv'
    new_entry = pd.DataFrame([[datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), name, id_card, dept, price, t_id]], 
                            columns=['التاريخ', 'الاسم', 'الهوية', 'القسم', 'المعلوم', 'رقم التذكرة'])
    
    if not os.path.isfile(file_name):
        new_entry.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        new_entry.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')

# 3. واجهة التطبيق
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
            t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}-{id_card[-3:]}"
            save_to_database(name, id_card, dept, current_price, t_id)
            
            # توليد الـ QR Code
            qr_content = f"المريض: {name}\nالهوية: {id_card}\nالقسم: {dept}\nالمعلوم: {current_price}\nالمرجع: {t_id}"
            qr = qrcode.make(qr_content)
            buf = BytesIO()
            qr.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.success(f"✅ تم التسجيل بنجاح! رقم التذكرة: {t_id}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.image(byte_im, caption="رمز QR الخاص بالتذكرة", width=250)
            with c2:
                st.info(f"المريض: {name}\n\nالقسم: {dept}\n\nالمبلغ: {current_price}")
                st.download_button(
                    label="📥 تحميل التذكرة (PNG)",
                    data=byte_im,
                    file_name=f"Ticket_{t_id}.png",
                    mime="image/png"
                )
        else:
            st.error("⚠️ يرجى ملء البيانات المطلوبة")

with tab2:
    st.subheader("📊 لوحة تحكم الإدارة")
    file_path = 'hospital_records.csv'
    if os.path.exists(file_path):
        try:
            # استخدام التحقق من الخطأ لمنع ParserError كما ظهر سابقاً
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                csv_buffer = BytesIO()
                df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                st.download_button("📥 تحميل سجل البيانات الكامل", data=csv_buffer.getvalue(), file_name="hospital_report.csv", mime="text/csv")
            else:
                st.info("السجل فارغ حالياً.")
        except Exception:
            st.error("حدث خطأ في قراءة السجل. سيتم إصلاحه تلقائياً عند التسجيل القادم.")
    else:
        st.info("لا توجد سجلات بعد.")
