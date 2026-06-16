"""End-to-end, step-by-step RSA simulation."""

from __future__ import annotations

import html
import math

import streamlit as st

from core.factor_demo import (
    factor_n_demo,
    fast_mod_exp,
    fast_mod_exp_detailed_steps,
)
from core.key_generation import calculate_n, calculate_phi, suggest_e, validate_e
from core.mod_math import extended_gcd_table
from core.prime_utils import is_prime, validate_prime_pair
from core.rsa_cipher import decrypt_text, encrypt_text, text_to_numbers
from core.rsa_service import generate_keys
from ui.shared import render_key_cards, render_step, render_substeps


def _smallest_divisor(number: int) -> int | None:
    if number < 2:
        return None
    if number % 2 == 0:
        return 2 if number != 2 else None
    for divisor in range(3, math.isqrt(number) + 1, 2):
        if number % divisor == 0:
            return divisor
    return None


def _prime_explanation(label: str, number: int) -> str:
    if is_prime(number):
        return (
            f"{label} = {number} là số nguyên tố: không có ước nào từ 2 đến "
            f"√{number} ≈ {math.isqrt(number)}."
        )
    divisor = _smallest_divisor(number)
    if divisor:
        return (
            f"{label} = {number} không phải số nguyên tố vì chia hết cho "
            f"{divisor} ({number} = {divisor} × {number // divisor})."
        )
    return f"{label} = {number} không phải số nguyên tố."


def _gcd_steps(a: int, b: int) -> list[dict]:
    rows = []
    step = 1
    while b:
        quotient, remainder = divmod(a, b)
        rows.append(
            {
                "Bước": step,
                "Phép chia": f"{a} = {quotient}×{b} + {remainder}",
                "Số dư": remainder,
            }
        )
        a, b = b, remainder
        step += 1
    return rows


def _load_easy_example() -> None:
    st.session_state.simulation_mode = "Nhập số"
    st.session_state.sim_p = 3
    st.session_state.sim_q = 11
    st.session_state.sim_e = 3
    st.session_state.sim_m = 4


def _load_medium_example() -> None:
    st.session_state.simulation_mode = "Nhập số"
    st.session_state.sim_p = 109
    st.session_state.sim_q = 137
    st.session_state.sim_e = 19
    st.session_state.sim_m = 123


def _load_text_example() -> None:
    st.session_state.simulation_mode = "Nhập văn bản"
    st.session_state.sim_p = 61
    st.session_state.sim_q = 53
    st.session_state.sim_e = 17
    st.session_state.sim_text = "HELLO RSA"


def _render_presets() -> None:
    st.markdown('<div class="section-label">Chọn điểm bắt đầu</div>', unsafe_allow_html=True)
    easy_col, medium_col, text_col = st.columns(3)
    with easy_col:
        st.button(
            "Ví dụ dễ: 3, 11, 3, m=4",
            width="stretch",
            on_click=_load_easy_example,
        )
    with medium_col:
        st.button(
            "Ví dụ vừa: 109, 137, 19",
            width="stretch",
            on_click=_load_medium_example,
        )
    with text_col:
        st.button(
            "Ví dụ văn bản: 61, 53, 17",
            width="stretch",
            on_click=_load_text_example,
        )


def _render_number_cipher(keys: dict) -> None:
    n, e, d = keys["n"], keys["e"], keys["d"]
    render_step(
        7,
        "Nhập thông điệp số m",
        "RSA làm việc với số. Điều kiện bắt buộc là 0 ≤ m < n.",
    )
    render_substeps(
        [
            ("7.1", "Nhập một số nguyên không âm."),
            ("7.2", f"So sánh m với n = {n}."),
            ("7.3", "Chỉ tiếp tục khi m nhỏ hơn n."),
        ]
    )
    m = int(
        st.number_input(
            "Thông điệp số m",
            min_value=0,
            step=1,
            key="sim_m",
            **({} if "sim_m" in st.session_state else {"value": 4}),
        )
    )
    if m >= n:
        st.error(
            f"m = {m} không hợp lệ vì m phải nhỏ hơn n = {n}. "
            "Hãy chọn số nhỏ hơn n."
        )
        return
    st.success(f"Thông điệp hợp lệ: 0 ≤ {m} < {n}.")

    render_step(
        8,
        "Mã hóa bằng khóa công khai",
        "Áp dụng c = mᵉ mod n và theo dõi thuật toán Square-and-Multiply.",
        "success",
    )
    render_substeps(
        [
            ("8.1", f"Lấy khóa công khai (e,n) = ({e},{n})."),
            ("8.2", f"Thay số: c = {m}^{e} mod {n}."),
            ("8.3", "Xử lý từng bit của e bằng bình phương–nhân."),
        ]
    )
    cipher = fast_mod_exp(m, e, n)
    st.latex(rf"c = {m}^{{{e}}} \bmod {n} = {cipher}")
    st.dataframe(
        fast_mod_exp_detailed_steps(m, e, n),
        width="stretch",
        hide_index=True,
    )
    st.success(f"Bản mã thu được: c = {cipher}.")

    render_step(
        9,
        "Giải mã bằng khóa bí mật",
        "Dùng m = cᵈ mod n để khôi phục thông điệp.",
        "success",
    )
    render_substeps(
        [
            ("9.1", f"Lấy khóa bí mật (d,n) = ({d},{n})."),
            ("9.2", f"Thay số: m = {cipher}^{d} mod {n}."),
            ("9.3", "Tiếp tục bình phương–nhân cho đến khi số mũ bằng 0."),
        ]
    )
    recovered = fast_mod_exp(cipher, d, n)
    st.latex(rf"m = {cipher}^{{{d}}} \bmod {n} = {recovered}")
    st.dataframe(
        fast_mod_exp_detailed_steps(cipher, d, n),
        width="stretch",
        hide_index=True,
    )

    render_step(
        10,
        "Đối chiếu kết quả",
        "So sánh thông điệp ban đầu với kết quả sau giải mã.",
        "success",
    )
    if recovered == m:
        st.markdown(
            f"""
            <div class="result-banner">
                <strong>Chu trình RSA hoàn tất chính xác</strong>
                Thông điệp ban đầu <code>{m}</code> → bản mã
                <code>{cipher}</code> → thông điệp khôi phục
                <code>{recovered}</code>.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Kết quả sau giải mã không trùng với thông điệp ban đầu.")


def _render_text_cipher(keys: dict) -> None:
    n, e, d = keys["n"], keys["e"], keys["d"]
    render_step(
        7,
        "Chuyển văn bản thành số",
        "Mỗi ký tự được mã hóa UTF-8 thành một hoặc nhiều byte, rồi từng byte đi qua RSA.",
    )
    render_substeps(
        [
            ("7.1", "Nhập chuỗi văn bản cần bảo vệ."),
            ("7.2", "Mã hóa chuỗi thành danh sách byte UTF-8."),
            ("7.3", f"Kiểm tra mọi byte đều nhỏ hơn n = {n}."),
        ]
    )
    plain_text = st.text_area(
        "Văn bản ban đầu",
        key="sim_text",
        height=100,
        **(
            {}
            if "sim_text" in st.session_state
            else {"value": "HELLO RSA"}
        ),
    )
    if not plain_text:
        st.error("Vui lòng nhập văn bản cần mô phỏng.")
        return

    message_numbers = text_to_numbers(plain_text)
    st.code(str(message_numbers), language="text")
    if n <= max(message_numbers):
        st.error(
            f"n = {n} chưa đủ lớn. Byte lớn nhất của thông điệp là "
            f"{max(message_numbers)}; hãy dùng ví dụ p=61, q=53 để có n=3233."
        )
        return
    st.success(
        f"Có {len(message_numbers)} byte và tất cả đều nhỏ hơn n = {n}."
    )

    encrypted = encrypt_text(plain_text, keys["public_key"])
    decrypted = decrypt_text(encrypted["cipher_numbers"], keys["private_key"])
    summary_rows = [
        {
            "#": index,
            "Byte M": message,
            "Bản mã C": cipher,
            "Byte khôi phục": recovered,
            "Khớp": "Đúng" if message == recovered else "Sai",
        }
        for index, (message, cipher, recovered) in enumerate(
            zip(
                encrypted["message_numbers"],
                encrypted["cipher_numbers"],
                decrypted["message_numbers"],
            ),
            start=1,
        )
    ]

    render_step(
        8,
        "Mã hóa từng byte",
        "Mỗi byte M được tính độc lập theo C = Mᵉ mod n.",
        "success",
    )
    render_substeps(
        [
            ("8.1", f"Dùng khóa công khai ({e},{n})."),
            ("8.2", "Lặp qua từng byte của văn bản."),
            ("8.3", "Lưu các C thành danh sách bản mã."),
        ]
    )
    st.dataframe(summary_rows, width="stretch", hide_index=True)

    selected_index = st.selectbox(
        "Chọn một byte để xem chi tiết phép mã hóa",
        options=list(range(len(message_numbers))),
        format_func=lambda index: (
            f"Byte #{index + 1}: M={message_numbers[index]}, "
            f"C={encrypted['cipher_numbers'][index]}"
        ),
    )
    selected_message = message_numbers[selected_index]
    selected_cipher = encrypted["cipher_numbers"][selected_index]
    st.latex(
        rf"C = {selected_message}^{{{e}}} \bmod {n} = {selected_cipher}"
    )
    st.dataframe(
        fast_mod_exp_detailed_steps(selected_message, e, n),
        width="stretch",
        hide_index=True,
    )

    render_step(
        9,
        "Giải mã từng bản mã",
        "Mỗi C được đưa qua m = Cᵈ mod n, sau đó các byte được ghép lại thành UTF-8.",
        "success",
    )
    render_substeps(
        [
            ("9.1", f"Dùng khóa bí mật ({d},{n})."),
            ("9.2", "Khôi phục từng byte từ từng bản mã."),
            ("9.3", "Giải mã danh sách byte thành văn bản UTF-8."),
        ]
    )
    st.latex(
        rf"M = {selected_cipher}^{{{d}}} \bmod {n} = {selected_message}"
    )
    st.dataframe(
        fast_mod_exp_detailed_steps(selected_cipher, d, n),
        width="stretch",
        hide_index=True,
    )

    render_step(
        10,
        "Đối chiếu văn bản",
        "So sánh toàn bộ chuỗi trước mã hóa và sau giải mã.",
        "success",
    )
    recovered_text = decrypted["decrypted_text"]
    if recovered_text == plain_text:
        st.markdown(
            f"""
            <div class="result-banner">
                <strong>Khôi phục văn bản thành công</strong>
                Văn bản ban đầu <code>{html.escape(plain_text)}</code> đã được
                mã hóa thành {len(encrypted["cipher_numbers"])} số và giải mã
                trở lại chính xác thành <code>{html.escape(recovered_text)}</code>.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Văn bản sau giải mã không trùng với văn bản ban đầu.")


def _render_factor_and_practice(keys: dict) -> None:
    with st.expander("Mở rộng: thử phân tích n để hiểu độ an toàn"):
        result = factor_n_demo(keys["n"])
        st.write(
            f"Với số nhỏ, thử chia tìm được `{keys['n']} = {result['p']} × "
            f"{result['q']}` sau `{result['attempts']}` lần thử."
        )
        st.warning(
            "Trong RSA thực tế, n có hàng trăm chữ số và phép thử chia như vậy "
            "không khả thi trong thời gian hợp lý."
        )

    with st.expander("Bài tập tự luyện"):
        st.markdown(
            """
            1. `p=5, q=11, e=3, m=9`: tìm `n`, `φ(n)`, `d`, `c`.
            2. `p=7, q=17, e=5, m=8`: kiểm tra điều kiện của `e`.
            3. `p=109, q=137, e=19, m=123`: đối chiếu với ví dụ trung bình.

            Dùng các nút ví dụ ở đầu trang để xem lời giải tự động từng bước.
            """
        )


def render() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Phần 2 · Mô phỏng từng bước</div>
            <h1>Tự tay đi qua toàn bộ chu trình RSA.</h1>
            <p>
                Mỗi bước lớn được chia thành các việc nhỏ: kiểm tra đầu vào,
                thay số vào công thức, xem bảng thuật toán và giải thích kết quả.
                Bạn có thể học bằng số nhỏ hoặc thử mã hóa văn bản UTF-8.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _render_presets()

    st.radio(
        "Chế độ thông điệp",
        ["Nhập số", "Nhập văn bản"],
        horizontal=True,
        key="simulation_mode",
    )

    render_step(
        1,
        "Nhập và kiểm tra p, q",
        "Hai giá trị phải là số nguyên tố khác nhau. Website giải thích cả trường hợp đúng và sai.",
    )
    render_substeps(
        [
            ("1.1", "Nhập hai số p và q."),
            ("1.2", "Thử các ước từ 2 đến căn bậc hai."),
            ("1.3", "Kiểm tra p và q không trùng nhau."),
        ]
    )
    p_col, q_col = st.columns(2)
    with p_col:
        p = int(
            st.number_input(
                "Số nguyên tố p",
                min_value=3,
                step=1,
                key="sim_p",
                **({} if "sim_p" in st.session_state else {"value": 3}),
            )
        )
    with q_col:
        q = int(
            st.number_input(
                "Số nguyên tố q",
                min_value=3,
                step=1,
                key="sim_q",
                **({} if "sim_q" in st.session_state else {"value": 11}),
            )
        )

    st.write(_prime_explanation("p", p))
    st.write(_prime_explanation("q", q))
    prime_result = validate_prime_pair(p, q)
    if not prime_result["valid"]:
        st.error(prime_result["message"])
        return
    st.success("p và q là hai số nguyên tố khác nhau.")

    render_step(
        2,
        "Tính n = p × q",
        "n là modulo chung xuất hiện trong cả khóa công khai và khóa bí mật.",
        "success",
    )
    render_substeps(
        [
            ("2.1", f"Lấy p = {p}."),
            ("2.2", f"Lấy q = {q}."),
            ("2.3", "Nhân hai số để tạo n."),
        ]
    )
    n = calculate_n(p, q)
    st.latex(rf"n = p \times q = {p} \times {q} = {n}")

    render_step(
        3,
        "Tính φ(n)",
        "Với n là tích của hai số nguyên tố, φ(n) = (p−1)(q−1).",
        "success",
    )
    render_substeps(
        [
            ("3.1", f"Tính p−1 = {p - 1}."),
            ("3.2", f"Tính q−1 = {q - 1}."),
            ("3.3", "Nhân hai kết quả để có φ(n)."),
        ]
    )
    phi_n = calculate_phi(p, q)
    st.latex(
        rf"\varphi(n) = ({p}-1)({q}-1) = {p - 1}\times{q - 1} = {phi_n}"
    )

    render_step(
        4,
        "Chọn và kiểm tra e",
        "e phải nằm giữa 1 và φ(n), đồng thời nguyên tố cùng nhau với φ(n).",
    )
    render_substeps(
        [
            ("4.1", f"Kiểm tra 1 < e < {phi_n}."),
            ("4.2", f"Tính gcd(e,{phi_n})."),
            ("4.3", "Chỉ chấp nhận khi gcd bằng 1."),
        ]
    )

    def choose_e() -> None:
        st.session_state.sim_e = suggest_e(phi_n)

    e_col, suggest_col = st.columns([2, 1])
    with e_col:
        e = int(
            st.number_input(
                "Số mũ công khai e",
                min_value=2,
                step=1,
                key="sim_e",
                **({} if "sim_e" in st.session_state else {"value": 3}),
            )
        )
    with suggest_col:
        st.button("Gợi ý e hợp lệ", width="stretch", on_click=choose_e)

    e_result = validate_e(e, phi_n)
    st.dataframe(_gcd_steps(e, phi_n), width="stretch", hide_index=True)
    common_divisor = math.gcd(e, phi_n)
    if not e_result["valid"]:
        st.error(e_result["message"])
        return
    st.success(f"gcd({e}, {phi_n}) = {common_divisor}; e hợp lệ.")

    render_step(
        5,
        "Tìm khóa bí mật d bằng Euclid mở rộng",
        "Theo dõi bảng hệ số r = s·φ(n) + t·e; hệ số t tại dòng r=1 cho ta d.",
        "success",
    )
    render_substeps(
        [
            ("5.1", f"Đặt a = φ(n) = {phi_n}, b = e = {e}."),
            ("5.2", "Chia Euclid và cập nhật đồng thời r, s, t."),
            ("5.3", "Lấy t tại r=1 rồi đưa về modulo φ(n)."),
        ]
    )
    keys = generate_keys(p, q, e)
    st.session_state.rsa_keys = keys
    euclid_rows = extended_gcd_table(phi_n, e)
    st.dataframe(euclid_rows, width="stretch", hide_index=True)
    inverse_row = next(row for row in euclid_rows if row["r"] == 1)
    coefficient = inverse_row["t"]
    st.info(
        f"Dòng r=1 cho hệ số của e là t={coefficient}. "
        f"Do đó d = {coefficient} mod {phi_n} = {keys['d']}."
    )
    st.code(
        f"Kiểm tra: {e} × {keys['d']} mod {phi_n} = "
        f"{(e * keys['d']) % phi_n}",
        language="text",
    )

    render_step(
        6,
        "Xuất khóa RSA",
        "Khóa công khai dùng để mã hóa; khóa bí mật dùng để giải mã.",
        "success",
    )
    render_substeps(
        [
            ("6.1", f"Ghép public key = ({e},{n})."),
            ("6.2", f"Ghép private key = ({keys['d']},{n})."),
            ("6.3", "Giữ d, p và q bí mật trong hệ thống thật."),
        ]
    )
    render_key_cards(keys)

    if st.session_state.simulation_mode == "Nhập số":
        _render_number_cipher(keys)
    else:
        _render_text_cipher(keys)

    _render_factor_and_practice(keys)
