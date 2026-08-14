import sqlite3
from io import BytesIO
import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Quản lý thông tin khách hàng", page_icon="📋", layout="wide"
)


# --- KHỞI TẠO VÀ XỬ LÝ CƠ SỞ DỮ LIỆU (SQLITE) ---
def init_db():
    """Khởi tạo bảng cơ sở dữ liệu nếu chưa tồn tại"""
    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            name TEXT NOT NULL,
            address TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_customer(phone, name, address, notes):
    """Thêm khách hàng mới vào cơ sở dữ liệu"""
    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO customers (phone, name, address, notes) VALUES (?, ?, ?,"
        " ?)",
        (phone, name, address, notes),
    )
    conn.commit()
    conn.close()


def get_all_customers():
    """Lấy toàn bộ danh sách khách hàng"""
    conn = sqlite3.connect("customers.db")
    df = pd.read_sql_query(
        'SELECT phone AS "Số điện thoại", name AS "Tên khách hàng", address AS'
        ' "Địa chỉ", notes AS "Ghi chú", created_at AS "Thời gian tạo" FROM'
        " customers ORDER BY id DESC",
        conn,
    )
    conn.close()
    return df


# Chạy khởi tạo DB
init_db()

# --- GIAO DIỆN ĐIỀU HƯỚNG (SIDEBAR) ---
st.sidebar.title("📌 Menu Quản Lý")
menu = st.sidebar.radio(
    "Chọn chức năng:", ["Nhập thông tin khách hàng", "Trang Admin (Quản lý)"]
)

# --- TRANG 1: NHẬP THÔNG TIN KHÁCH HÀNG ---
if menu == "Nhập thông tin khách hàng":
    st.title("📝 Nhập Thông Tin Khách Hàng")
    st.write("Vui lòng điền thông tin chi tiết bên dưới:")

    with st.form(key="customer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            phone = st.text_input("Số điện thoại (*)")
        with col2:
            name = st.text_input("Tên khách hàng (*)")

        address = st.text_area("Địa chỉ", placeholder="Nhập địa chỉ cụ thể...")
        notes = st.text_area("Ghi chú", placeholder="Ghi chú thêm (nếu có)...")

        submit_button = st.form_submit_button(label="💾 Lưu lại")

        if submit_button:
            if not phone.strip() or not name.strip():
                st.error("⚠️ Vui lòng điền đầy đủ **Số điện thoại** và **Tên khách hàng**!")
            else:
                add_customer(
                    phone.strip(), name.strip(), address.strip(), notes.strip()
                )
                st.success(
                    f"✅ Đã lưu thành công thông tin khách hàng **{name}**!")

# --- TRANG 2: TRANG ADMIN (QUẢN LÝ & XUẤT EXCEL) ---
elif menu == "Trang Admin (Quản lý)":
    st.title("👑 Trang Quản Trị - Danh Sách Khách Hàng")

    df = get_all_customers()

    if not df.empty:
        # Thống kê nhanh
        st.metric(label="Tổng số khách hàng", value=len(df))

        # Hiển thị bảng dữ liệu
        st.subheader("📋 Bảng dữ liệu")
        st.dataframe(df, use_container_width=True)

        # Chức năng xuất file Excel
        st.subheader("📥 Xuất Dữ Liệu")

        # Chuyển đổi DataFrame sang định dạng binary Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Danh_Sach_Khach_Hang")
        excel_data = output.getvalue()

        st.download_button(
            label="📊 Tải xuống file Excel (.xlsx)",
            data=excel_data,
            file_name="danh_sach_khach_hang.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
    else:
        st.info("ℹ️ Hiện chưa có dữ liệu khách hàng nào được lưu.")
