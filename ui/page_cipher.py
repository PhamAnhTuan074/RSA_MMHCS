"""Direct RSA encryption and decryption utility page."""

from __future__ import annotations

import html

import streamlit as st

from core.key_generation import calculate_phi, suggest_e, validate_e
from core.prime_utils import validate_prime_pair
from core.rsa_cipher import decrypt_text, encrypt_text, parse_cipher_numbers
from core.rsa_service import generate_keys
from ui.shared import render_key_cards


def _load_text_key_example() -> None:
    st.session_state.cipher_p = 61
    st.session_state.cipher_q = 53
    st.session_state.cipher_e = 17


def _load_medium_key_example() -> None:
    st.session_state.cipher_p = 109
    st.session_state.cipher_q = 137
    st.session_state.cipher_e = 19


def _use_last_encryption() -> None:
    last = st.session_state.get("cipher_last_encryption")
    if not last:
        return
    keys = last["keys"]
    st.session_state.cipher_action = "Giải mã"
    st.session_state.cipher_p = keys["p"]
    st.session_state.cipher_q = keys["q"]
    st.session_state.cipher_e = keys["e"]
    st.session_state.cipher_numbers_input = ", ".join(
        str(number) for number in last["cipher_numbers"]
    )


def _number_input_kwargs(key: str, value: int) -> dict:
    return {} if key in st.session_state else {"value": value}


def _render_key_setup() -> dict | None:
    st.markdown('<div class="section-label">1. Chọn hoặc tạo khóa RSA</div>', unsafe_allow_html=True)
    preset_col, medium_col, note_col = st.columns([1, 1, 1.35])
    with preset_col:
        st.button(
            "Khóa mẫu văn bản 61×53",
            width="stretch",
            on_click=_load_text_key_example,
        )
    with medium_col:
        st.button(
            "Khóa mẫu 109×137",
            width="stretch",
            on_click=_load_medium_key_example,
        )
    with note_col:
        st.caption(
            "Mã hóa văn bản UTF-8 cần `n > 255`; bộ 61×53 tạo `n = 3233`, đủ cho từng byte."
        )

    p_col, q_col, e_col = st.columns(3)
    with p_col:
        p = int(
            st.number_input(
                "p",
                min_value=3,
                step=1,
                key="cipher_p",
                **_number_input_kwargs("cipher_p", 61),
            )
        )
    with q_col:
        q = int(
            st.number_input(
                "q",
                min_value=3,
                step=1,
                key="cipher_q",
                **_number_input_kwargs("cipher_q", 53),
            )
        )
    with e_col:
        e = int(
            st.number_input(
                "e",
                min_value=2,
                step=1,
                key="cipher_e",
                **_number_input_kwargs("cipher_e", 17),
            )
        )

    prime_result = validate_prime_pair(p, q)
    if not prime_result["valid"]:
        st.error(prime_result["message"])
        return None

    phi_n = calculate_phi(p, q)

    def choose_valid_e() -> None:
        st.session_state.cipher_e = suggest_e(phi_n)

    e_result = validate_e(e, phi_n)
    metric_n, metric_phi, metric_gcd, suggest_col = st.columns([1, 1, 1, 1])
    metric_n.metric("n = p × q", f"{p * q:,}")
    metric_phi.metric("φ(n)", f"{phi_n:,}")
    metric_gcd.metric("gcd(e, φ(n))", "1" if e_result["valid"] else "Không hợp lệ")
    with suggest_col:
        st.button("Gợi ý e", width="stretch", on_click=choose_valid_e)

    if not e_result["valid"]:
        st.error(e_result["message"])
        return None

    keys = generate_keys(p, q, e)
    st.session_state.rsa_keys = keys
    render_key_cards(keys)
    return keys


def _render_encrypt(keys: dict) -> None:
    st.markdown('<div class="section-label">3. Mã hóa văn bản</div>', unsafe_allow_html=True)
    st.write(
        "Nhập văn bản gốc. Website sẽ đổi chuỗi thành byte UTF-8 rồi mã hóa từng byte bằng khóa công khai."
    )
    plain_text = st.text_area(
        "Văn bản cần mã hóa",
        height=130,
        key="cipher_plain_text",
        **(
            {}
            if "cipher_plain_text" in st.session_state
            else {"value": "Xin chào RSA"}
        ),
    )

    if st.button("Mã hóa văn bản", type="primary", width="stretch"):
        try:
            encrypted = encrypt_text(plain_text, keys["public_key"])
            st.session_state.cipher_last_encryption = {
                **encrypted,
                "keys": keys,
            }
        except ValueError as exc:
            st.error(str(exc))

    encrypted = st.session_state.get("cipher_last_encryption")
    if not encrypted:
        st.info("Nhấn nút mã hóa để tạo bản mã.")
        return

    cipher_text = ", ".join(str(number) for number in encrypted["cipher_numbers"])
    st.success("Đã mã hóa văn bản thành công.")

    result_col, detail_col = st.columns([1.1, 1])
    with result_col:
        st.markdown("**Bản mã đầu ra**")
        st.code(cipher_text, language="text")
        st.download_button(
            "Tải bản mã .txt",
            data=cipher_text,
            file_name="rsa_cipher_numbers.txt",
            mime="text/plain",
            width="stretch",
        )
        st.button(
            "Chuyển bản mã này sang phần giải mã",
            width="stretch",
            on_click=_use_last_encryption,
        )
    with detail_col:
        st.markdown("**Dữ liệu trung gian**")
        st.code(
            "Byte UTF-8:\n"
            f"{encrypted['message_numbers']}\n\n"
            f"Public key: {encrypted['public_key']}",
            language="text",
        )

    rows = [
        {
            "#": index,
            "Ký hiệu": f"M{index}",
            "Byte M": message,
            f"C = M^{keys['e']} mod {keys['n']}": cipher,
        }
        for index, (message, cipher) in enumerate(
            zip(encrypted["message_numbers"], encrypted["cipher_numbers"]),
            start=1,
        )
    ]
    with st.expander("Xem từng byte được mã hóa như thế nào", expanded=True):
        st.dataframe(rows, width="stretch", hide_index=True)


def _render_decrypt(keys: dict) -> None:
    st.markdown('<div class="section-label">3. Giải mã bản mã</div>', unsafe_allow_html=True)
    st.write(
        "Dán danh sách số bản mã. Có thể nhập dạng `123, 456`, `[123, 456]` hoặc mỗi số một dòng."
    )

    if st.session_state.get("cipher_last_encryption"):
        st.button(
            "Dùng bản mã vừa mã hóa",
            width="stretch",
            on_click=_use_last_encryption,
        )

    cipher_input = st.text_area(
        "Danh sách bản mã",
        height=150,
        key="cipher_numbers_input",
        placeholder="Ví dụ: 1345, 3179, 2235, 1992",
    )

    if st.button("Giải mã bản mã", type="primary", width="stretch"):
        try:
            cipher_numbers = parse_cipher_numbers(cipher_input)
            decrypted = decrypt_text(cipher_numbers, keys["private_key"])
            st.session_state.cipher_last_decryption = decrypted
        except ValueError as exc:
            st.error(str(exc))

    decrypted = st.session_state.get("cipher_last_decryption")
    if not decrypted:
        st.info("Nhấn nút giải mã để khôi phục văn bản.")
        return

    st.success("Đã giải mã bản mã thành công.")
    st.markdown(
        f"""
        <div class="result-banner">
            <strong>Văn bản sau giải mã</strong>
            <code>{html.escape(decrypted["decrypted_text"])}</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rows = [
        {
            "#": index,
            "Bản mã C": cipher,
            f"M = C^{keys['d']} mod {keys['n']}": message,
        }
        for index, (cipher, message) in enumerate(
            zip(decrypted["cipher_numbers"], decrypted["message_numbers"]),
            start=1,
        )
    ]
    with st.expander("Xem từng số bản mã được giải mã như thế nào", expanded=True):
        st.dataframe(rows, width="stretch", hide_index=True)
        st.code(
            "Byte khôi phục:\n"
            f"{decrypted['message_numbers']}\n\n"
            f"Private key: {decrypted['private_key']}",
            language="text",
        )


def render() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Phần 3 · Mã Hóa, Giải Mã</div>
            <h1>Công cụ thực hành mã hóa và giải mã RSA.</h1>
            <p>
                Phần này tập trung vào thao tác đầu vào và đầu ra: chọn khóa,
                chọn mã hóa hoặc giải mã, nhập văn bản hoặc bản mã rồi nhận kết
                quả ngay. Nếu cần học từng phép tính, quay lại phần mô phỏng.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    keys = _render_key_setup()
    if not keys:
        return

    st.markdown('<div class="section-label">2. Chọn thao tác</div>', unsafe_allow_html=True)
    action = st.radio(
        "Bạn muốn thực hiện thao tác nào?",
        ["Mã hóa", "Giải mã"],
        horizontal=True,
        key="cipher_action",
    )

    if action == "Mã hóa":
        _render_encrypt(keys)
    else:
        _render_decrypt(keys)

    st.warning(
        "Đây là RSA thô dùng để học tập. Không dùng trang này để bảo mật dữ liệu thật."
    )
