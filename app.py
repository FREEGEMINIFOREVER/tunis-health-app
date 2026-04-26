import streamlit as st
import qrcode
from io import BytesIO

# 1. إعدادات التصميم الشاملة (CSS) لتخصيص كل عنصر
st.markdown("""
    <style>
    /* تنسيق عام للخلفية */
    .main {
        background-color: #0e1117;
    }
    
    /* توسيط وتنسيق صورة الطبيب */
    .doctor-container {
        display: flex;
        justify-content: center;
        padding: 20px;
    }
    .doctor-img {
        width: 150px;
        border-radius: 50%;
        border: 3px solid #28a745;
    }
    
    /* تخصيص كل خانة إدخال على حدة (الاسم، اللقب، بطاقة التعريف، الهاتف) */
    .stTextInput input {
        color: #ffffff !important; /* نص أبيض ناصع */
        background-color: #1e1e1e !important; /* خلفية داكنة */
        border: 1px solid #444 !important;
        border-radius: 10px !important;
    }

    /* تخصيص خانة اختيار القسم */
    div[data-baseweb="select"] > div {
        color: white !important;
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
    }

    /* تنسيق زر الترسيم والاستخلاص (أخضر كما طلبت) */
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 12px !important;
        width: 100%;
        height: 50px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #218838 !important;
        transform: scale(1.02);
    }

    /* نصوص العناوين بيضاء */
    label {
        color: white !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. صورة الطبيب في الوسط
st.markdown('<div class="doctor-container"><img src="https://cdn-icons-png.flaticon.com/512/3844/3844476.png" class="doctor-img"></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>منظومة تسجيل المرضى</h2>", unsafe_allow_html=True)

# 3. الخانات بالترتيب الدقيق الذي طلبته
st.write("---")
nome = st.text_input("1. الاسم", placeholder="أدخل الاسم هنا...")
prenom = st.text_input("2. اللقب", placeholder="أدخل اللقب هنا...")
cin = st.text_input("3. رقم بطاقة التعريف", placeholder="8 أرقام")
phone = st.text_input("4. رقم الهاتف", placeholder="+216...")

# اختيار القسم مع نص أبيض ناصع
section = st.selectbox("القسم المطلوب", ["قسم الاستعجالي", "قسم العظام", "قسم القلب", "الجراحة العامة"])

st.write("---")

# 4. منطق الترسيم وتوليد الـ QR Code والإشعارات
if st.button("الترسيم والاستخلاص"):
    if nome and prenom and cin and phone:
        # تجميع البيانات للكود
        data_to_encode = f"المريض: {nome} {prenom}\nبطاقة تعريف: {cin}\nالقسم: {section}"
        
        # إنشاء الـ QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data_to_encode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # تحويل الصورة لصيغة يمكن تنزيلها
        buf = BytesIO()
        img.save(buf)
        byte_im = buf.getvalue()

        # إشعار المريض بالتنزيل (كما طلبت)
        st.toast(f"✅ تم تنزيل كود الترسيم لهاتفك يا {nome}", icon='📥')
        st.success("تمت عملية التسجيل بنجاح! يمكنك تحميل الكود أدناه.")
        
        # زر تنزيل الكود
        st.download_button(
            label="📥 اضغط هنا لحفظ كود الترسيم (QR)",
            data=byte_im,
            file_name=f"registration_{cin}.png",
            mime="image/png"
        )
    else:
        st.warning("الرجاء التأكد من ملء جميع البيانات قبل الترسيم.")
