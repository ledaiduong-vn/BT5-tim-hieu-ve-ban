import datetime as dt
import re
import unicodedata
from typing import Dict, List

import streamlit as st


st.set_page_config(page_title="Tìm hiểu về bạn", page_icon="🌟", layout="centered")

# Ảnh nền theo chủ đề thần số học và tử vi
BACKGROUND_IMAGE_URL = (
    "https://images.unsplash.com/photo-1534447677768-be436bb09401"
    "?auto=format&fit=crop&w=1600&q=80"
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(10, 10, 25, 0.78), rgba(10, 10, 25, 0.78)),
            url("{BACKGROUND_IMAGE_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    [data-testid="stForm"], .stAlert, .stMetric, .stDownloadButton, .stTextInput, .stDateInput, .stNumberInput, .stSelectbox {{
        background: rgba(255, 255, 255, 0.92);
        border-radius: 10px;
        padding: 8px;
    }}

    h1, h2, h3, p, label {{
        color: #f5f6ff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def sum_digits_until_one_digit(num: int) -> int:
    while num > 9 and num not in (11, 22, 33):
        num = sum(int(d) for d in str(num))
    return num


def calculate_bmi(height_cm: float, weight_kg: float) -> Dict[str, str]:
    height_m = height_cm / 100
    bmi = weight_kg / (height_m**2)

    if bmi < 18.5:
        category = "Thiếu cân"
        advice = "Bạn nên tăng cường dinh dưỡng và tập luyện nhẹ để cải thiện sức khỏe tổng thể."
    elif bmi < 25:
        category = "Bình thường"
        advice = "Chỉ số BMI lý tưởng. Hãy duy trì chế độ ăn uống và vận động hợp lý."
    elif bmi < 30:
        category = "Thừa cân"
        advice = "Bạn nên cân bằng khẩu phần ăn, giảm đường/chất béo và tăng hoạt động thể chất."
    else:
        category = "Béo phì"
        advice = "Bạn nên tham khảo chuyên gia dinh dưỡng và xây dựng kế hoạch giảm cân phù hợp."

    return {
        "bmi": f"{bmi:.2f}",
        "category": category,
        "advice": advice,
    }


def numerology_from_name_and_birth(name: str, birth_date: dt.date) -> Dict[str, str]:
    clean_name = re.sub(r"[^A-Za-zÀ-ỹà-ỹ\s]", "", name).upper()
    letters_only = re.sub(r"\s+", "", clean_name)

    # Bảng quy đổi Pythagoras
    mapping = {
        "A": 1,
        "J": 1,
        "S": 1,
        "B": 2,
        "K": 2,
        "T": 2,
        "C": 3,
        "L": 3,
        "U": 3,
        "D": 4,
        "M": 4,
        "V": 4,
        "E": 5,
        "N": 5,
        "W": 5,
        "F": 6,
        "O": 6,
        "X": 6,
        "G": 7,
        "P": 7,
        "Y": 7,
        "H": 8,
        "Q": 8,
        "Z": 8,
        "I": 9,
        "R": 9,
    }

    # Chuẩn hóa Unicode để bỏ dấu tiếng Việt an toàn
    ascii_name = unicodedata.normalize("NFD", letters_only)
    ascii_name = "".join(ch for ch in ascii_name if unicodedata.category(ch) != "Mn")
    ascii_name = ascii_name.replace("Đ", "D").replace("đ", "d")

    name_sum = sum(mapping.get(ch, 0) for ch in ascii_name)
    expression_number = sum_digits_until_one_digit(name_sum)

    life_path_raw = int(birth_date.strftime("%d%m%Y"))
    life_path_number = sum_digits_until_one_digit(sum(int(d) for d in str(life_path_raw)))

    expression_meanings = {
        1: "Độc lập, chủ động, có tố chất lãnh đạo.",
        2: "Tinh tế, hợp tác tốt, giàu cảm xúc.",
        3: "Sáng tạo, biểu đạt tốt, năng lượng tích cực.",
        4: "Thực tế, kỷ luật, bền bỉ.",
        5: "Yêu tự do, linh hoạt, thích trải nghiệm.",
        6: "Trách nhiệm, yêu gia đình, biết quan tâm.",
        7: "Chiêm nghiệm, thích học hỏi chiều sâu.",
        8: "Tham vọng, giỏi tổ chức, thiên hướng quản lý.",
        9: "Nhân ái, bao dung, có tầm nhìn cộng đồng.",
        11: "Trực giác mạnh, truyền cảm hứng.",
        22: "Khả năng hiện thực hóa ý tưởng lớn.",
        33: "Năng lực chữa lành, phụng sự và yêu thương sâu sắc.",
    }

    life_path_meanings = {
        1: "Con đường tiên phong, học cách tự tin và dẫn dắt.",
        2: "Con đường hòa hợp, phát triển kỹ năng lắng nghe và cân bằng.",
        3: "Con đường sáng tạo, học cách biểu đạt và lan tỏa niềm vui.",
        4: "Con đường xây nền tảng, ổn định và kiên trì.",
        5: "Con đường thay đổi, khám phá và thích nghi.",
        6: "Con đường trách nhiệm, tình yêu và phụng sự.",
        7: "Con đường tri thức, hướng nội và phát triển nội tâm.",
        8: "Con đường thành tựu, quản trị và tác động thực tế.",
        9: "Con đường nhân văn, vị tha và phụng sự cộng đồng.",
        11: "Con đường trực giác, truyền cảm hứng tinh thần.",
        22: "Con đường kiến tạo lớn, biến tầm nhìn thành hiện thực.",
        33: "Con đường chữa lành và lan tỏa tình thương.",
    }

    return {
        "expression_number": str(expression_number),
        "expression_meaning": expression_meanings.get(
            expression_number, "Đang cập nhật diễn giải cho chỉ số này."
        ),
        "life_path_number": str(life_path_number),
        "life_path_meaning": life_path_meanings.get(
            life_path_number, "Đang cập nhật diễn giải cho chỉ số này."
        ),
    }


def zodiac_info_from_year(year: int, gender: str) -> Dict[str, str]:
    can = [
        "Canh",
        "Tân",
        "Nhâm",
        "Quý",
        "Giáp",
        "Ất",
        "Bính",
        "Đinh",
        "Mậu",
        "Kỷ",
    ]
    chi = [
        "Thân",
        "Dậu",
        "Tuất",
        "Hợi",
        "Tý",
        "Sửu",
        "Dần",
        "Mão",
        "Thìn",
        "Tỵ",
        "Ngọ",
        "Mùi",
    ]

    menh_map = [
        "Kim",
        "Kim",
        "Hỏa",
        "Hỏa",
        "Mộc",
        "Mộc",
        "Thổ",
        "Thổ",
        "Kim",
        "Kim",
        "Hỏa",
        "Hỏa",
        "Thủy",
        "Thủy",
        "Thổ",
        "Thổ",
        "Mộc",
        "Mộc",
        "Thủy",
        "Thủy",
        "Kim",
        "Kim",
        "Hỏa",
        "Hỏa",
        "Mộc",
        "Mộc",
        "Thổ",
        "Thổ",
        "Kim",
        "Kim",
        "Thủy",
        "Thủy",
        "Thổ",
        "Thổ",
        "Mộc",
        "Mộc",
        "Kim",
        "Kim",
        "Hỏa",
        "Hỏa",
        "Thủy",
        "Thủy",
        "Thổ",
        "Thổ",
        "Mộc",
        "Mộc",
        "Kim",
        "Kim",
        "Hỏa",
        "Hỏa",
        "Thủy",
        "Thủy",
        "Thổ",
        "Thổ",
        "Mộc",
        "Mộc",
        "Kim",
        "Kim",
        "Hỏa",
        "Hỏa",
    ]

    can_chi = f"{can[year % 10]} {chi[year % 12]}"
    menh = menh_map[year % 60]

    basic_advice = (
        "Năm nay nên chú trọng cân bằng công việc - nghỉ ngơi, giữ tinh thần tích cực "
        "và ưu tiên các mục tiêu dài hạn."
    )
    if gender == "Nam":
        detail = "Nam mệnh phù hợp phát triển sự nghiệp qua tính chủ động và quyết đoán."
    elif gender == "Nữ":
        detail = "Nữ mệnh thuận lợi khi phát huy sự tinh tế, bền bỉ và khả năng kết nối."
    else:
        detail = "Bạn có thể phát huy điểm mạnh cá nhân bằng việc đặt mục tiêu rõ ràng và kiên định."

    return {
        "can_chi": can_chi,
        "menh": menh,
        "zodiac_message": f"{basic_advice} {detail}",
    }


def build_export_text(
    profile: Dict[str, str],
    bmi_data: Dict[str, str],
    numerology_data: Dict[str, str],
    zodiac_data: Dict[str, str],
) -> str:
    lines: List[str] = [
        "TÌM HIỂU VỀ BẠN",
        "=" * 40,
        "",
        "1) THÔNG TIN CÁ NHÂN",
        f"- Họ và tên: {profile['full_name']}",
        f"- Ngày sinh: {profile['birth_date']}",
        f"- Giới tính: {profile['gender']}",
        f"- Chiều cao: {profile['height_cm']} cm",
        f"- Cân nặng: {profile['weight_kg']} kg",
        "",
        "2) ĐÁNH GIÁ BMI",
        f"- BMI: {bmi_data['bmi']}",
        f"- Phân loại: {bmi_data['category']}",
        f"- Gợi ý: {bmi_data['advice']}",
        "",
        "3) THẦN SỐ HỌC",
        f"- Chỉ số biểu đạt: {numerology_data['expression_number']}",
        f"- Ý nghĩa: {numerology_data['expression_meaning']}",
        f"- Số đường đời: {numerology_data['life_path_number']}",
        f"- Ý nghĩa: {numerology_data['life_path_meaning']}",
        "",
        "4) TỬ VI CƠ BẢN",
        f"- Năm âm lịch (Can Chi): {zodiac_data['can_chi']}",
        f"- Mệnh ngũ hành: {zodiac_data['menh']}",
        f"- Tổng quan: {zodiac_data['zodiac_message']}",
        "",
        "-" * 40,
        "Lưu ý: Nội dung chỉ mang tính tham khảo, không thay thế tư vấn y khoa/chuyên gia.",
    ]
    return "\n".join(lines)


st.title("🌟 Tìm hiểu về bạn")
st.write(
    "Nhập thông tin cá nhân để xem nhanh tình trạng sức khỏe theo BMI, thần số học và tử vi cơ bản."
)

with st.form("profile_form"):
    full_name = st.text_input("Họ và tên (đầy đủ)")
    birth_date = st.date_input(
        "Ngày tháng năm sinh",
        min_value=dt.date(1900, 1, 1),
        max_value=dt.date.today(),
        value=dt.date(2000, 1, 1),
    )
    gender = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])
    height_cm = st.number_input("Chiều cao (cm)", min_value=50.0, max_value=250.0, value=165.0)
    weight_kg = st.number_input("Cân nặng (kg)", min_value=20.0, max_value=300.0, value=60.0)
    submitted = st.form_submit_button("Xem kết quả")

if submitted:
    full_name = normalize_text(full_name)
    if not full_name:
        st.error("Vui lòng nhập đầy đủ họ và tên.")
        st.stop()

    profile_data = {
        "full_name": full_name,
        "birth_date": birth_date.strftime("%d/%m/%Y"),
        "gender": gender,
        "height_cm": f"{height_cm:.1f}",
        "weight_kg": f"{weight_kg:.1f}",
    }

    bmi_result = calculate_bmi(height_cm, weight_kg)
    numerology_result = numerology_from_name_and_birth(full_name, birth_date)
    zodiac_result = zodiac_info_from_year(birth_date.year, gender)

    st.subheader("1) Thông tin cá nhân")
    st.write(profile_data)

    st.subheader("2) Tình trạng sức khỏe theo BMI")
    st.metric("BMI", bmi_result["bmi"], bmi_result["category"])
    st.info(bmi_result["advice"])

    st.subheader("3) Thần số học (tham khảo)")
    st.write(f"**Chỉ số biểu đạt:** {numerology_result['expression_number']}")
    st.write(numerology_result["expression_meaning"])
    st.write(f"**Số đường đời:** {numerology_result['life_path_number']}")
    st.write(numerology_result["life_path_meaning"])

    st.subheader("4) Tử vi cơ bản theo năm sinh")
    st.write(f"**Can Chi:** {zodiac_result['can_chi']}")
    st.write(f"**Mệnh ngũ hành:** {zodiac_result['menh']}")
    st.write(zodiac_result["zodiac_message"])

    export_text = build_export_text(
        profile=profile_data,
        bmi_data=bmi_result,
        numerology_data=numerology_result,
        zodiac_data=zodiac_result,
    )

    st.download_button(
        label="📄 Xuất kết quả ra file TXT",
        data=export_text.encode("utf-8"),
        file_name="tim_hieu_ve_ban.txt",
        mime="text/plain",
    )
