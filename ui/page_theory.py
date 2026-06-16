"""Beginner-friendly RSA theory lessons."""

from __future__ import annotations

import streamlit as st

from core.factor_demo import fast_mod_exp_detailed_steps
from core.mod_math import extended_gcd_table


def _render_learning_map() -> None:
    st.markdown(
        """
        <div class="learning-map">
            <div class="map-item"><span>01</span><strong>RSA là gì?</strong><small>Hai khóa và mục đích sử dụng.</small></div>
            <div class="map-item"><span>02</span><strong>Nền tảng toán</strong><small>Số nguyên tố, modulo, gcd.</small></div>
            <div class="map-item"><span>03</span><strong>Tạo khóa</strong><small>Tìm n, φ(n), e và d.</small></div>
            <div class="map-item"><span>04</span><strong>Mã hóa</strong><small>Biến m thành bản mã c.</small></div>
            <div class="map-item"><span>05</span><strong>Giải mã</strong><small>Khôi phục lại thông điệp m.</small></div>
            <div class="map-item"><span>06</span><strong>An toàn</strong><small>Vì sao số lớn bảo vệ RSA.</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _overview_lesson() -> None:
    st.markdown('<div class="section-label">RSA là gì?</div>', unsafe_allow_html=True)
    st.write(
        "RSA là thuật toán mã hóa **bất đối xứng**: hệ thống sử dụng hai khóa "
        "khác nhau nhưng liên hệ toán học với nhau. Người gửi dùng khóa công khai "
        "để mã hóa; chỉ người giữ khóa bí mật tương ứng mới giải mã được."
    )

    public_col, private_col = st.columns(2)
    with public_col:
        st.info(
            "**Khóa công khai `(e, n)`**\n\n"
            "Có thể công bố cho mọi người. Vai trò chính là mã hóa thông điệp gửi "
            "đến chủ sở hữu khóa."
        )
    with private_col:
        st.warning(
            "**Khóa bí mật `(d, n)`**\n\n"
            "Chỉ người nhận được giữ. Vai trò chính là giải mã bản mã được tạo "
            "bởi khóa công khai tương ứng."
        )

    st.markdown(
        """
        <div class="analogy">
            <strong>Ví dụ đời thường:</strong> Khóa công khai giống một ổ khóa bạn
            phát cho mọi người. Ai cũng có thể dùng ổ khóa đó để khóa hộp thư gửi
            cho bạn, nhưng chỉ bạn có chìa khóa bí mật để mở hộp.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Ý tưởng an toàn</div>', unsafe_allow_html=True)
    st.write(
        "Nhân hai số nguyên tố lớn `p` và `q` để có `n = p × q` là dễ. Nhưng nếu "
        "chỉ biết một `n` rất lớn, việc tìm ngược lại đúng `p` và `q` là rất khó. "
        "Đây là nền tảng trực giác của RSA."
    )


def _math_lesson() -> None:
    st.markdown('<div class="section-label">Các ký hiệu cần biết</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="definition-grid">
            <div class="definition-card"><div class="symbol">p, q</div><strong>Số nguyên tố bí mật</strong><p>Hai số được chọn ban đầu, khác nhau và rất lớn trong thực tế.</p></div>
            <div class="definition-card"><div class="symbol">n</div><strong>Modulo chung</strong><p>n = p × q, xuất hiện trong cả khóa công khai và khóa bí mật.</p></div>
            <div class="definition-card"><div class="symbol">φ(n)</div><strong>Hàm phi Euler</strong><p>Với RSA cơ bản: φ(n) = (p−1)(q−1).</p></div>
            <div class="definition-card"><div class="symbol">e</div><strong>Số mũ mã hóa</strong><p>1 &lt; e &lt; φ(n) và gcd(e, φ(n)) = 1.</p></div>
            <div class="definition-card"><div class="symbol">d</div><strong>Số mũ giải mã</strong><p>Nghịch đảo modulo của e: e·d ≡ 1 mod φ(n).</p></div>
            <div class="definition-card"><div class="symbol">m, c</div><strong>Thông điệp và bản mã</strong><p>m là số ban đầu, c là kết quả sau mã hóa.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Bốn công cụ toán học</div>', unsafe_allow_html=True)
    concepts = [
        (
            "Số nguyên tố",
            "Số lớn hơn 1 chỉ chia hết cho 1 và chính nó. Ví dụ: 3, 5, 7, 11.",
        ),
        (
            "Modulo",
            "`21 mod 20 = 1` vì `21 = 20 × 1 + 1`. Ta chỉ giữ phần dư.",
        ),
        (
            "Ước chung lớn nhất",
            "`gcd(a,b)=1` nghĩa là a và b nguyên tố cùng nhau. e phải thỏa điều này với φ(n).",
        ),
        (
            "Nghịch đảo modulo",
            "d là nghịch đảo của e nếu `e × d mod φ(n) = 1`.",
        ),
    ]
    for title, text in concepts:
        with st.expander(title):
            st.markdown(text)


def _key_lesson() -> None:
    st.markdown('<div class="section-label">Quy trình tạo khóa</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="formula-grid">
            <div class="formula-card"><div class="formula-label">1. Chọn số nguyên tố</div><div class="formula-value">p = 3, q = 11</div></div>
            <div class="formula-card"><div class="formula-label">2. Tính n</div><div class="formula-value">n = 3 × 11 = 33</div></div>
            <div class="formula-card"><div class="formula-label">3. Tính φ(n)</div><div class="formula-value">φ(n) = 2 × 10 = 20</div></div>
            <div class="formula-card"><div class="formula-label">4. Chọn e</div><div class="formula-value">e = 3, gcd(3,20)=1</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "Bước còn lại là tìm `d` sao cho `3 × d ≡ 1 (mod 20)`. Dùng Euclid mở "
        "rộng, ta biểu diễn mỗi số dư theo dạng `r = s·20 + t·3`."
    )
    table = extended_gcd_table(20, 3)
    st.dataframe(table, width="stretch", hide_index=True)
    st.success(
        "Dòng có `r = 1` cho ta `1 = -1×20 + 7×3`. Hệ số của e là 7, "
        "vì vậy `d = 7`. Kiểm tra: `3×7 mod 20 = 1`."
    )

    st.markdown('<div class="section-label">Kết quả tạo khóa</div>', unsafe_allow_html=True)
    public_col, private_col = st.columns(2)
    public_col.metric("Khóa công khai", "(e, n) = (3, 33)")
    private_col.metric("Khóa bí mật", "(d, n) = (7, 33)")


def _cipher_lesson() -> None:
    st.markdown('<div class="section-label">Mã hóa</div>', unsafe_allow_html=True)
    st.write(
        "Thông điệp phải được biểu diễn bằng số `m` và thỏa `0 ≤ m < n`. "
        "Người gửi dùng khóa công khai `(e,n)`:"
    )
    st.latex(r"c = m^e \bmod n")
    st.code("m = 4, e = 3, n = 33\nc = 4³ mod 33 = 31", language="text")

    st.markdown('<div class="section-label">Giải mã</div>', unsafe_allow_html=True)
    st.write("Người nhận dùng khóa bí mật `(d,n)` để khôi phục thông điệp:")
    st.latex(r"m = c^d \bmod n")
    st.code("c = 31, d = 7, n = 33\nm = 31⁷ mod 33 = 4", language="text")
    st.success("Kết quả giải mã `4` trùng với thông điệp ban đầu `4`.")

    st.markdown('<div class="section-label">Khi thông điệp là văn bản</div>', unsafe_allow_html=True)
    st.write(
        "RSA chỉ xử lý số. Website chuyển văn bản thành các byte UTF-8, mã hóa "
        "từng byte rồi ghép lại sau khi giải mã. Khi đó `n` phải lớn hơn mọi byte, "
        "nên ví dụ văn bản cần `n > 255`."
    )


def _fast_power_lesson() -> None:
    st.markdown('<div class="section-label">Vì sao cần Square-and-Multiply?</div>', unsafe_allow_html=True)
    st.write(
        "Tính trực tiếp `a^b` tạo ra số cực lớn. Thuật toán bình phương–nhân đọc "
        "số mũ theo từng bit, chỉ cần khoảng `log₂(b)` vòng lặp."
    )
    st.markdown(
        """
        <div class="formula-grid">
            <div class="formula-card"><div class="formula-label">Khởi tạo</div><div class="formula-value">result = 1</div></div>
            <div class="formula-card"><div class="formula-label">Nếu số mũ lẻ</div><div class="formula-value">result = result × base mod n</div></div>
            <div class="formula-card"><div class="formula-label">Bình phương</div><div class="formula-value">base = base² mod n</div></div>
            <div class="formula-card"><div class="formula-label">Giảm số mũ</div><div class="formula-value">exponent = exponent // 2</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Ví dụ: tính `4³ mod 33`; số mũ `3 = 11₂`.")
    st.dataframe(
        fast_mod_exp_detailed_steps(4, 3, 33),
        width="stretch",
        hide_index=True,
    )
    st.success("Kết quả cuối là `31`, chính là bản mã của thông điệp `m = 4`.")


def _security_lesson() -> None:
    st.subheader("RSA trong chữ ký số")
    st.info(
        "Trong chữ ký số, RSA giúp xác thực người ký và kiểm tra dữ liệu có bị thay đổi "
        "sau khi ký hay không. Muốn an toàn, RSA cần khóa đủ lớn, chuẩn ký phù hợp và "
        "thư viện mật mã đã được kiểm chứng."
    )

    def render_point_cards(items: list[tuple[str, str]]) -> None:
        card_height = 128
        for row_start in range(0, len(items), 2):
            columns = st.columns(2)
            for column, (title, text) in zip(columns, items[row_start : row_start + 2]):
                with column:
                    with st.container(border=True, height=card_height):
                        st.markdown(f"**{title}**")
                        st.write(text)

    st.markdown("### Ưu điểm")
    advantages = [
        (
            "Bảo mật cao",
            "Khóa đủ lớn và chuẩn ký an toàn giúp RSA rất khó bị phá bằng máy tính thông thường.",
        ),
        (
            "Linh hoạt",
            "RSA dùng được trong nhiều hệ thống bảo mật, nhất là khi cần xác thực danh tính.",
        ),
        (
            "Tương thích rộng",
            "Nhiều nền tảng, thư viện và hạ tầng chứng chỉ số hiện đã hỗ trợ RSA.",
        ),
        (
            "Đã được kiểm chứng",
            "RSA đã được dùng lâu năm trong thực tế nên có mức độ tin cậy cao.",
        ),
    ]
    render_point_cards(advantages)

    st.markdown("### Hạn chế")
    limitations = [
        (
            "Xử lý chậm hơn",
            "RSA có thể chậm khi cần ký hoặc kiểm tra chữ ký với số lượng lớn.",
        ),
        (
            "Cần khóa lớn",
            "Khóa 2048 bit hoặc 4096 bit an toàn hơn nhưng tốn thêm tài nguyên.",
        ),
        (
            "Quản lý khóa phức tạp",
            "Hệ thống nhiều người dùng cần quản lý tạo, lưu trữ và thu hồi khóa chặt chẽ.",
        ),
        (
            "Có rủi ro triển khai",
            "Máy tính lượng tử và side-channel có thể gây rủi ro nếu triển khai sai.",
        ),
    ]
    render_point_cards(limitations)

    st.warning(
        "**Ghi nhớ:** các ví dụ số nhỏ trong website chỉ dùng để học. Hệ thống thật nên dùng "
        "khóa đủ dài, thư viện chuẩn và padding chữ ký như RSA-PSS; không nên tự triển khai mật mã."
    )


def render() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Phần 1 · Lý thuyết RSA</div>
            <h1>Hiểu bản chất trước khi bấm nút mô phỏng.</h1>
            <p>
                Bài học đi từ khái niệm hai khóa, nền tảng toán học, tạo khóa,
                mã hóa và giải mã đến lũy thừa modulo nhanh. Mỗi chủ đề đều có
                ví dụ thay số để người mới có thể tự kiểm tra.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _render_learning_map()

    tabs = st.tabs(
        [
            "1. Tổng quan",
            "2. Nền tảng toán",
            "3. Tạo khóa",
            "4. Mã hóa & giải mã",
            "5. Lũy thừa nhanh",
            "6. An toàn",
        ]
    )
    lessons = [
        _overview_lesson,
        _math_lesson,
        _key_lesson,
        _cipher_lesson,
        _fast_power_lesson,
        _security_lesson,
    ]
    for tab, lesson in zip(tabs, lessons):
        with tab:
            lesson()
