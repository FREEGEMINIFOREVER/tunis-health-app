import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات الصفحة واللون الأخضر (Hex Code: #28a745)
st.set_page_config(page_title="بوابة الصحة التونسية الرقمية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; }
    
    /* فرض اللون الأخضر على زر الترسيم وزر التحميل */
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        height: 3em;
        font-weight: bold;
        width: 100%;
    }
    div.stDownloadButton > button {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 10px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة حفظ البيانات
def save_to_database(f_name, l_name, id_no, ph, dept, pr, t_id):
    file_name = 'hospital_records.csv'
    new_entry = pd.DataFrame([[datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), f_name, l_name, id_no, ph, dept, pr, t_id]], 
                            columns=['التاريخ', 'الاسم', 'اللقب', 'الهوية', 'الهاتف', 'القسم', 'المعلوم', 'رقم التذكرة'])
    if not os.path.isfile(file_name):
        new_entry.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        new_entry.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')

st.title("🏥 المنظومة الرقمية المتكاملة للصحة")
tab1, tab2 = st.tabs(["📝 تسجيل مريض جديد", "📋 سجل المستشفى"])

with tab1:
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("👤 الاسم")
            id_card = st.text_input("🪪 رقم بطاقة التعريف")
        with col2:
            last_name = st.text_input("👤 اللقب")
            phone = st.text_input("📞 رقم الهاتف")
        
        dept = st.selectbox("🏥 القسم المطلوب", ["الاستعجالي", "طب العيون", "طب الأطفال", "قسم الجراحة"])
        prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "قسم الجراحة": "20.000"}
        st.metric("معلوم الكشف", f"{prices[dept]} DT")
        
        submitted = st.form_submit_button("تأكيد الترسيم واستخراج التذكرة")

    if submitted:
        if first_name and last_name and id_card and phone:
            t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}"
            save_to_database(first_name, last_name, id_card, phone, dept, prices[dept], t_id)
            
            # حفظ البيانات في جلسة العمل لتبقى ظاهرة
            st.session_state.qr_data = f"المريض: {first_name} {last_name}\nالهوية: {id_card}\nالتذكرة: {t_id}"
            st.session_state.ticket_ready = True
            st.session_state.f_name = first_name

    # عرض النتائج والإشعار (خارج الـ form لضمان التفاعل)
    if st.session_state.get('ticket_ready'):
        st.success(f"✅ تم التسجيل! رقم تذكرتك: {t_id}")
        qr_img = qrcode.make(st.session_state.qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        
        col_img, col_txt = st.columns(2)
        with col_img:
            st.image(buf.getvalue(), width=200)
        with col_txt:
            # إضافة نظام الإشعار عند الضغط
            st.download_button(
                label="📥 اضغط هنا لتحميل التذكرة (PNG)",
                data=buf.getvalue(),
                file_name=f"Ticket_{st.session_state.f_name}.png",
                mime="image/png",
                on_click=lambda: st.toast("✅ رائع! تم حفظ التذكرة في مجلد التحميلات بهاتفك", icon="💾")
            )
            st.info("💡 بمجرد الضغط، سيظهر إشعار في أسفل الشاشة يؤكد التحميل.")

with tab2:
    if os.path.exists('hospital_records.csv'):
        st.dataframe(pd.read_csv('hospital_records.csv'), use_container_width=True)
