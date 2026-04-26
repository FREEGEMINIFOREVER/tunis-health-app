import streamlit as st
import qrcode
from io import BytesIO
import time

# 1. إعدادات الصفحة المتقدمة - تنسيق الخلفية والعناصر
# قمنا بوضع صورة الطبيب كخلفية كاملة للشاشة
st.markdown("""
    <style>
    /* خلفية صورة طبيب كبيرة تملأ الشاشة */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1576091160550-2173bdb999ef?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* جعل العناصر تطفو فوق الخلفية بوضوح */
    .main .block-container {
        background-color: rgba(14, 17, 23, 0.85); /* خلفية داكنة نصف شفافة */
        padding: 3rem;
        border-radius: 20px;
        margin-top: 2rem;
    }

    /* تنسيق العناوين (بيضاء وبارزة) */
    h1, h2, h3, .stMarkdown, label {
        color: #ffffff !important;
        font-weight: bold !important;
        text-align: center;
    }

    /* تخصيص خانات الإدخال */
    .stTextInput input, div[data-baseweb="select"] > div {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #4caf50 !important;
        border-radius: 10px !important;
    }

    /* تخصيص زر الترسيم والاستخلاص الأخضر */
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 12px !important;
        width: 100%;
        height: 55px;
        transition: 0.3s;
        margin-top: 20px;
    }
    div.stButton > button:hover {
        background-color: #218838 !important;
        transform: scale(1.02);
    }

    /* تنسيق قسم الثمن */
    .price-box {
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 15px;
        background-color: rgba(40, 167, 69, 0.1);
        color: white;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الواجهة الرئيسية
st.markdown("<h1 style='color: #4caf50; font-size: 3rem;'>منظومة تسجيل المرضى</h1>", unsafe_allow_html=True)
st.write("---")

# 3. الخانات بالترتيب الدقيق من الصورة
nome = st.text_input("1. الاسم", placeholder="مثال: أحمد")
prenom = st.text_input("2. اللقب", placeholder="مثال: صالحي")
cin = st.text_input("3. رقم بطاقة التعريف", placeholder="8 أرقام")
phone = st.text_input("4. رقم الهاتف", placeholder="+216...")
dept = st.selectbox("القسم المطلوب", ["قسم العظام", "قسم القلب", "الجراحة العامة"])

st.write("---")

# 4. إضافة ثمن التسجيل (جديد)
# قمنا بإنشاء حاوية مخصصة لإظهار الثمن بوضوح
st.markdown("<h3 style='color: white;'>معلومات الدفع</h3>", unsafe_allow_html=True)
st.markdown('<div class="price-box">💰 ثمن التسجيل: 20.000 د.ت</div>', unsafe_allow_html=True)

# 5. منطق الترسيم وتوليد الـ QR Code والإشعارات (الشامل)
if st.button("الترسيم والاستخلاص"):
    if nome and prenom and cin and phone:
        with st.spinner("جاري معالجة البيانات وتوليد الكود..."):
            time.sleep(1.5) # محاكاة المعالجة

            # تجميع البيانات للكود
            data_to_encode = f"المريض: {nome} {prenom}\nبطاقة تعريف: {cin}\nالقسم: {dept}\nالحالة: مدفوع (20 د.ت)"
            
            # إنشاء الـ QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data_to_encode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # تحويل الصورة لصيغة يمكن تنزيلها
            buf = BytesIO()
            img.save(buf)
            byte_im = buf.getvalue()

            # إشعار التنزيل (كما طلبت)
            st.toast(f"✅ تم تنزيل كود الترسيم الخاص بك يا {nome}", icon='📥')
            
            # رسالة نجاح مع زر التحميل
            st.success("تمت عملية التسجيل واستخلاص الثمن بنجاح!")
            
            # زر تنزيل الكود
            st.download_button(
                label="📥 اضغط هنا لحفظ كود الترسيم (QR)",
                data=byte_im,
                file_name=f"registration_{cin}.png",
                mime="image/png"
            )
    else:
        st.warning("الرجاء التأكد من ملء جميع البيانات قبل الترسيم.")
