import streamlit as st
import pandas as pd
from io import BytesIO

from database import (
    create_table,
    add_customer,
    get_customers,
    delete_customer
)


# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="Quản lý khách hàng",
    page_icon="👤",
    layout="wide"
)

# Tạo database/table
create_table()


# =========================
# HÀM XUẤT EXCEL
# =========================

def export_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Khách hàng"
        )

    return output.getvalue()


# =========================
# MENU
# =========================

st.sidebar.title("📋 MENU")

page = st.sidebar.radio(
    "Chọn trang",
    [
        "👤 Nhập khách hàng",
        "🔐 Admin"
    ]
)


# =====================================================
# TRANG NHẬP KHÁCH HÀNG
# =====================================================

if page == "👤 Nhập khách hàng":

    st.title("👤 THÔNG TIN KHÁCH HÀNG")

    st.write(
        "Vui lòng nhập thông tin khách hàng bên dưới."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        phone = st.text_input(
            "📱 Số điện thoại",
            placeholder="Nhập số điện thoại"
        )

    with col2:

        name = st.text_input(
            "👤 Tên khách hàng",
            placeholder="Nhập tên khách hàng"
        )

    address = st.text_input(
        "📍 Địa chỉ",
        placeholder="Nhập địa chỉ khách hàng"
    )

    note = st.text_area(
        "📝 Ghi chú",
        placeholder="Nhập ghi chú nếu có"
    )

    st.divider()

    if st.button(
        "💾 LƯU THÔNG TIN",
        type="primary",
        use_container_width=True
    ):

        # Kiểm tra dữ liệu bắt buộc
        if phone.strip() == "":
            st.error("❌ Vui lòng nhập số điện thoại.")

        elif name.strip() == "":
            st.error("❌ Vui lòng nhập tên khách hàng.")

        else:

            add_customer(
                phone=phone.strip(),
                name=name.strip(),
                address=address.strip(),
                note=note.strip()
            )

            st.success(
                "✅ Đã lưu thông tin khách hàng thành công!"
            )

            st.balloons()


# =====================================================
# TRANG ADMIN
# =====================================================

elif page == "🔐 Admin":

    st.title("🔐 ADMIN - QUẢN LÝ KHÁCH HÀNG")

    st.divider()

    # =========================
    # ĐĂNG NHẬP ADMIN
    # =========================

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:st.subheader("🔑 Đăng nhập Admin")

        password = st.text_input(
            "Mật khẩu",
            type="password"
        )

        if st.button(
            "Đăng nhập",
            type="primary"
        ):

            if password == "123456":

                st.session_state.admin_logged_in = True

                st.success("✅ Đăng nhập thành công!")

                st.rerun()

            else:

                st.error("❌ Sai mật khẩu.")

    else:

        # =========================
        # HEADER ADMIN
        # =========================

        col1, col2 = st.columns([5, 1])

        with col1:

            st.subheader("📊 Danh sách khách hàng")

        with col2:

            if st.button("🚪 Đăng xuất"):

                st.session_state.admin_logged_in = False

                st.rerun()

        # =========================
        # LẤY DỮ LIỆU
        # =========================

        df = get_customers()

        if df.empty:

            st.info(
                "📭 Chưa có thông tin khách hàng."
            )

        else:

            # =========================
            # THỐNG KÊ
            # =========================

            st.metric(
                "👥 Tổng số khách hàng",
                len(df)
            )

            st.divider()

            # =========================
            # HIỂN THỊ BẢNG
            # =========================

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # =========================
            # XUẤT EXCEL
            # =========================

            excel_file = export_excel(df)

            st.download_button(
                label="📥 XUẤT FILE EXCEL",
                data=excel_file,
                file_name="danh_sach_khach_hang.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True
            )

            st.divider()

            # =========================
            # XÓA KHÁCH HÀNG
            # =========================

            st.subheader("🗑️ Xóa khách hàng")

            customer_id = st.number_input(
                "Nhập STT khách hàng cần xóa",
                min_value=1,
                step=1
            )

            if st.button(
                "🗑️ XÓA KHÁCH HÀNG",
                type="secondary"
            ):

                delete_customer(customer_id)

                st.success(
                    "✅ Đã xóa khách hàng."
                )

                st.rerun()
