import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات الصفحة والتصميم (استعادة اللون الأخضر وتحسين الواجهة)
st.set_page_config(page_title="بوابة الصحة التونسية الرقمية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; }
    
    /* 1. اللون الأخضر لزر الترسيم كما طلبت */
    .stButton>button {
        width: 100%; 
        background-color: #28a745; 
        color: white;
        font-weight: bold; 
        border-radius: 10px;
        border: none;
        padding: 0.7rem;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #218838;
        box-shadow: 0px 4px 15px rgba(40, 167, 69, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة حفظ البيانات المطورة (إضافة الخانات الجديدة)
def save_to_database(first_name, last_name, id_card, phone, dept, price, t_id):
    file_name = 'hospital_records.csv'
    new_entry = pd.DataFrame([[
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
        first_name, last_name, id_card, phone, dept, price, t_id
    ]], columns=['التاريخ', 'الاسم', 'اللقب', 'الهوية', 'الهاتف', 'القسم', 'المعلوم', 'رقم التذكرة'])
    
    if not os.path.isfile(file_name):
        new_entry.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        new_entry.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')

# 3. واجهة التطبيق
st.title("🏥 المنظومة الرقمية المتكاملة للصحة")
tab1, tab2 = st.tabs(["📝 تسجيل مريض جديد", "📋 سجل المستشفى"])

with tab1:
    st.subheader("الرجاء إدخال البيانات الشخصية")
    with st.form("patient_registration"):
        # 2. الخانات المطلوبة (الاسم، اللقب، بطاقة التعريف، الهاتف)
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("👤 الاسم")
            id_card = st.text_input("🪪 رقم بطاقة التعريف الوطنية")
        with col2:
            last_name = st.text_input("👤 اللقب")
            phone = st.text_input("📞 رقم الهاتف")
        
        col3, col4 = st.columns(2)
        with col3:
            dept = st.selectbox("🏥 القسم المطلوب", 
                                ["الاستعجالي", "طب العيون", "طب الأطفال", "قسم الجراحة", "الأمراض الباطنية"])
        with col4:
            prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "قسم الجراحة": "20.000", "الأمراض الباطنية": "12.000"}
            current_price = f"{prices[dept]} DT"
            st.metric("معلوم الكشف", current_price)

        submitted = st.form_submit_button("تأكيد الترسيم واستخراج التذكرة")

    if submitted:
        if first_name and last_name and id_card and phone:
            t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}-{id_card[-3:]}"
            save_to_database(first_name, last_name, id_card, phone, dept, current_price, t_id)
            
            # توليد الـ QR Code
            qr_content = f"المريض: {first_name} {last_name}\nالهوية: {id_card}\nالهاتف: {phone}\nالقسم: {dept}\nالمرجع: {t_id}"
            qr = qrcode.make(qr_content)
            buf = BytesIO()
            qr.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.success(f"✅ تم التسجيل بنجاح! رقم التذكرة الخاص بك هو: {t_id}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.image(byte_im, caption="رمز QR الخاص بالتذكرة", width=250)
            with c2:
                st.info(f"المريض: {first_name} {last_name}\n\nالقسم: {dept}\n\nالمبلغ: {current_price}")
                
                # 3. حل مشكلة الإشعار عند التنزيل
                # عند الضغط على هذا الزر، سيعرف المريض أن العملية تمت
                if st.download_button(
                    label="📥 تحميل التذكرة الرقمية على الهاتف",
                    data=byte_im,
                    file_name=f"Ticket_{first_name}_{last_name}.png",
                    mime="image/png"
                ):
                    st.balloons() # إشعار بصري (بالونات) عند الضغط
                    st.toast("تم بدء تحميل التذكرة بنجاح!", icon='💾')
        else:
            st.error("⚠️ يرجى التأكد من ملء جميع الخانات (الاسم، اللقب، الهوية، والهاتف)")

with tab2:
    st.subheader("📊 سجل المعاملات (للإدارة)")
    file_path = 'hospital_records.csv'
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            st.dataframe(df, use_container_width=True)
            
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            st.download_button("📥 تحميل السجل الكامل (CSV)", data=csv_buffer.getvalue(), file_name="hospital_report.csv", mime="text/csv")
        except Exception:
            st.info("السجل قيد التحديث.. قم بأول عملية تسجيل للمريض الجديد.")
    else:
        st.info("لا توجد سجلات بعد.")
