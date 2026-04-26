import streamlit as st
import qrcode
import pandas as pd
from io import BytesIO
import datetime
import os

# 1. إعدادات التصميم (فرض اللون الأخضر على جميع الأزرار)
st.set_page_config(page_title="بوابة الصحة التونسية الرقمية", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; }
    
    /* فرض اللون الأخضر على زر الترسيم وزر التحميل */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.7rem !important;
        width: 100% !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #218838 !important;
        box-shadow: 0px 4px 15px rgba(40, 167, 69, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة حفظ البيانات (مرتبة حسب طلبك)
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
    except Exception:
        # إعادة بناء الملف في حال حدوث ParserError
        pd.DataFrame([new_data], columns=header).to_csv(file_name, index=False, encoding='utf-8-sig')

# 3. واجهة التطبيق
st.title("🏥 المنظومة الرقمية المتكاملة للصحة")
tab1, tab2 = st.tabs(["📝 تسجيل مريض جديد", "📋 سجل المستشفى"])

with tab1:
    st.subheader("الرجاء إدخال بيانات المريض")
    with st.form("patient_form"):
        # ترتيب الخانات: الاسم -> اللقب -> الهوية -> الهاتف
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("👤 الاسم")
            id_card = st.text_input("🪪 رقم بطاقة التعريف الوطنية")
        with col2:
            last_name = st.text_input("👤 اللقب")
            phone = st.text_input("📞 رقم الهاتف")
        
        dept = st.selectbox("🏥 القسم المطلوب", ["الاستعجالي", "طب العيون", "طب الأطفال", "قسم الجراحة", "الأمراض الباطنية"])
        prices = {"الاستعجالي": "15.000", "طب العيون": "10.000", "طب الأطفال": "10.000", "قسم الجراحة": "20.000", "الأمراض الباطنية": "12.000"}
        st.metric("معلوم الكشف", f"{prices[dept]} DT")

        # زر التسجيل (سيكون باللون الأخضر)
        submitted = st.form_submit_button("تأكيد الترسيم واستخراج التذكرة")

    if submitted:
        if first_name and last_name and id_card:
            t_id = f"TN-{datetime.datetime.now().strftime('%M%S')}"
            save_data_safely(first_name, last_name, id_card, phone, dept, prices[dept], t_id)
            
            # إنشاء الـ QR Code
            qr_content = f"المريض: {first_name} {last_name}\nالهوية: {id_card}\nالقسم: {dept}\nالتذكرة: {t_id}"
            qr_img = qrcode.make(qr_content)
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            
            st.success(f"✅ تم التسجيل بنجاح! رقم التذكرة: {t_id}")
            
            c_qr, c_info = st.columns(2)
            with c_qr:
                st.image(buf.getvalue(), caption="رمز التذكرة الرقمية", width=200)
            with c_info:
                st.info(f"المريض: {first_name} {last_name}\nالقسم: {dept}")
                # زر التحميل (باللون الأخضر أيضاً مع إشعار)
                st.download_button(
                    label="📥 تحميل التذكرة على الهاتف",
                    data=buf.getvalue(),
                    file_name=f"Ticket_{first_name}.png",
                    mime="image/png",
                    on_click=lambda: st.toast("✅ تم تحميل التذكرة بنجاح!", icon='💾')
                )
        else:
            st.error("⚠️ يرجى إدخال الاسم واللقب ورقم الهوية")

with tab2:
    if os.path.exists('hospital_records.csv'):
        try:
            df_view = pd.read_csv('hospital_records.csv', encoding='utf-8-sig')
            st.dataframe(df_view, use_container_width=True)
        except Exception:
            st.info("السجل قيد التحديث..")
