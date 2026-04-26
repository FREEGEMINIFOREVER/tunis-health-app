import streamlit as st
import qrcode
from io import BytesIO
import random

# إعدادات الصفحة الأساسية لضمان السرعة والتوافق مع الهواتف
st.set_page_config(page_title="وزارة الصحة - الترسيم الرقمي", page_icon="🏥", layout="centered")

# تنسيق المظهر العام (CSS) ليكون احترافياً ويدعم اللغة العربية من اليمين لليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 8px; width: 100%; height: 3em; font-weight: bold; }
    .ticket-container { border: 2px solid #007bff; border-radius: 15px; padding: 20px; background-color: #f8f9fa; color: black; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# عرض الشعار (رابط مباشر لشعار الوزارة) والعناوين
st.image("https://seeklogo.com/images/M/ministere-de-la-sante-tunisie-logo-7E61A1D205-seeklogo.com.png", width=120)
st.title("نظام الترسيم والاستخلاص الموحد")
st.subheader("بوابة المريض التونسي الرقمية")

# استمارة التسجيل الإلكتروني
with st.container():
    name = st.text_input("الأسم واللقب")
    card_id = st.text_input("رقم بطاقة التعريف الوطنية")
    department = st.selectbox("اختر القسم المطلوب", ["الاستعجالي", "القلب", "العيون", "الأشعة"])
    
    st.info("معلوم الكشف: 15.000 DT (يتم الخصم إلكترونياً)")
    
    if st.button("تأكيد الترسيم والحصول على التذكرة"):
        if name and card_id:
            # توليد رقم تذكرة عشوائي لضمان التنظيم
            t_num = random.randint(100, 999)
            
            # إنشاء الـ QR Code الذي يحتوي على بيانات المريض
            qr_content = f"Name: {name} | ID: {card_id} | Dept: {department} | Ticket: {t_num}"
            img = qrcode.make(qr_content)
            buf = BytesIO()
            img.save(buf, format="PNG")
            
            # عرض رسالة النجاح والتذكرة الرقمية
            st.success("تمت عملية الاستخلاص بنجاح!")
            st.markdown(f"""
                <div class="ticket-container">
                    <h2 style="color: #007bff;">تذكرة مراجع رقمية</h2>
                    <p><b>السيد(ة):</b> {name}</p>
                    <p><b>القسم:</b> {department}</p>
                    <p><b>رقم التذكرة:</b> <span style="font-size: 24px;">#{t_num}</span></p>
                    <hr>
                    <p>يرجى الاستظهار بالكود أدناه عند مكتب الاستقبال</p>
                </div>
            """, unsafe_allow_html=True)
            st.image(buf.getvalue(), use_column_width=False, width=250)
            st.balloons() # حركة احتفالية بسيطة
        else:
            st.error("الرجاء إدخال كافة البيانات المطلوبة")
