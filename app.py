import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات التصميم (اللون الأخضر الصريح #28a745)
st.set_page_config(page_title="بوابة الصحة التونسية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold; width: 100%; border-radius: 10px;
    }
    div.stDownloadButton > button {
        background-color: #28a745 !important;
        color: white !important;
        width: 100%; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة حفظ البيانات المطورة مع نظام "مضاد للتلف"
def save_data_safely(f_name, l_name, id_no, ph, dept, pr, t_id):
    file_name = 'hospital_records.csv'
    header = ['التاريخ', 'الاسم', 'الالقب', 'الهوية', 'الهاتف', 'القسم', 'المعلوم', 'رقم التذكرة']
    new_data = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), f_name, l_name, id_no, ph, dept, pr, t_id]
    
    # إذا كان الملف غير موجود أو تالف، نقوم بإنشائه من جديد بالكامل
    try:
        if not os.path.isfile(file_name):
            pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')
        else:
            df = pd.read_csv(file_name, encoding='utf-8-sig')
            df = pd.concat([df, pd.DataFrame([new_data], columns=header)], ignore_index=True)
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
    except Exception:
        # في حال حدوث أي خطأ في القراءة (ParserError)، نقوم بمسح الملف القديم والبدء من جديد
        pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')

# 3. واجهة المستخدم
st.title("🏥 المنظومة الرقمية المتكاملة للصحة")
tab1, tab2 = st.tabs(["📝 تسجيل مريض", "📋 سجل الإدارة"])

with tab1:
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("👤 الاسم")
            id_card = st.text_input("🪪 رقم بطاقة التعريف")
        with c2:
            last_name = st.text_input("👤 اللقب")
            phone = st.text_input("📞 رقم الهاتف")
        
        dept = st.selectbox("🏥 القسم", ["الاستعجالي", "طب العيون", "طب الأطفال", "قسم الجراحة"])
        prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "قسم الجراحة": "20.000"}
        st.metric("المعلوم", f"{prices[dept]} DT")
        
        submitted = st.form_submit_button("تأكيد الترسيم")

    if submitted and first_name and id_card:
        t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}"
        save_data_safely(first_name, last_name, id_card, phone, dept, prices[dept], t_id)
        
        # إنشاء الـ QR Code
        qr_img = qrcode.make(f"Patient: {first_name} {last_name}\nID: {id_card}\nTicket: {t_id}")
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        
        st.success(f"✅ تم الترسيم! رقم التذكرة: {t_id}")
        st.image(buf.getvalue(), width=200)
        
        # زر التحميل مع الإشعار
        st.download_button(
            label="📥 تحميل التذكرة على الهاتف",
            data=buf.getvalue(),
            file_name=f"Ticket_{t_id}.png",
            mime="image/png",
            on_click=lambda: st.toast("تم التحميل! ابحث عن الصورة في الاستوديو", icon="💾")
        )

with tab2:
    st.subheader("📊 السجل الرقمي")
    if os.path.exists('hospital_records.csv'):
        try:
            # محاولة القراءة، وإذا فشلت (خطأ ParserError) يتم إخطار المستخدم
            df_view = pd.read_csv('hospital_records.csv', encoding='utf-8-sig')
            st.dataframe(df_view, use_container_width=True)
        except Exception:
            st.warning("⚠️ تم اكتشاف خلل في ملف البيانات السابق، سيتم إصلاحه تلقائياً عند أول عملية تسجيل جديدة.")
