import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Hàm tính tổ hợp
def combination(k, n):
    if k > n or k < 0:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

# ==========================================
# CỬA SỔ CHÍNH (HOME DASHBOARD)
# ==========================================
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần Mềm Phân Tích Xác Suất Thống Kê - Đồ Án Sinh Viên")
        self.root.geometry("850x600")
        self.root.configure(bg="#f0f2f5")

        # Đọc dữ liệu
        try:
            self.df = pd.read_csv('dataset.csv')
            self.gpas = self.df['Điểm TB']
            self.study_hours = self.df['Số giờ học/ngày']
            self.phone_hours = self.df['Số giờ dùng ĐT']  # Đã gán đầy đủ biến này
            self.num_students = len(self.df)
        except Exception as e:
            messagebox.showerror("Lỗi", "Không tìm thấy file 'dataset.csv'! Hãy chạy file 'generate_data.py' trước.")
            self.root.destroy()
            return

        # Header
        header = tk.Frame(self.root, bg="#2c3e50", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="ỨNG DỤNG XÁC SUẤT THỐNG KÊ KẾT QUẢ HỌC TẬP", 
                 fg="white", bg="#2c3e50", font=("Arial", 16, "bold")).pack()
        tk.Label(header, text=f"Bộ dữ liệu khảo sát mẫu gồm {self.num_students} sinh viên", 
                 fg="#bdc3c7", bg="#2c3e50", font=("Arial", 10)).pack()

        # Phần giữa: Hiển thị bảng danh sách 50 sinh viên dạng rút gọn
        body_frame = tk.Frame(self.root, bg="#f0f2f5", padx=20, pady=15)
        body_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(body_frame, text="📋 Danh sách dữ liệu 50 sinh viên (Xem trước):", 
                 font=("Arial", 11, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(anchor="w", pady=(0, 5))

        # Tạo Treeview (Bảng hiển thị)
        columns = ("SV", "Điểm TB", "Số giờ học/ngày", "Số giờ dùng ĐT")
        self.tree = ttk.Treeview(body_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Đưa dữ liệu vào bảng
        for index, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=(int(row['SV']), row['Điểm TB'], row['Số giờ học/ngày'], row['Số giờ dùng ĐT']))

        scrollbar = ttk.Scrollbar(body_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Phần dưới: 2 nút bấm điều hướng
        nav_frame = tk.Frame(self.root, bg="#f0f2f5", pady=15)
        nav_frame.pack(fill=tk.X)

        btn_math = tk.Button(nav_frame, text="📐 1. Xem 12 Bài Toán Xác Suất & Thống Kê", 
                             font=("Arial", 11, "bold"), bg="#2980b9", fg="white", 
                             padx=15, pady=10, relief=tk.RAISED, command=self.open_math_window)
        btn_math.pack(side=tk.LEFT, padx=30, expand=True)

        btn_chart = tk.Button(nav_frame, text="📊 2. Xem Biểu Đồ & Mối Quan Hệ", 
                              font=("Arial", 11, "bold"), bg="#27ae60", fg="white", 
                              padx=15, pady=10, relief=tk.RAISED, command=self.open_chart_window)
        btn_chart.pack(side=tk.RIGHT, padx=30, expand=True)

    def open_math_window(self):
        MathWindow(self.root, self.df, self.gpas, self.study_hours, self.phone_hours, self.num_students)

    def open_chart_window(self):
        show_charts_window(self.df, self.gpas, self.study_hours, self.num_students)


# ==========================================
# CỬA SỔ 1: HỆ THỐNG 12 BÀI TOÁN XÁC SUẤT (CÓ XÁC SUẤT ĐẦY ĐỦ & BAYES)
# ==========================================
class MathWindow:
    def __init__(self, parent, df, gpas, study_hours, phone_hours, num_students):
        self.win = tk.Toplevel(parent)
        self.win.title("Chi Tiết Công Thức Toán Học & 12 Bài Toán Xác Suất Thống Kê")
        self.win.geometry("950x820")
        self.win.configure(bg="#f0f2f5")

        tk.Label(self.win, text="HỆ THỐNG 12 BÀI TOÁN XÁC SUẤT THỐNG KÊ (ĐẦY ĐỦ & BAYES)", 
                 font=("Arial", 14, "bold"), bg="#2c3e50", fg="white", pady=10).pack(fill=tk.X)

        text_frame = tk.Frame(self.win, padx=15, pady=15, bg="#f0f2f5")
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_area = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 11), bg="white", fg="#2c3e50", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tính toán thống kê cơ bản
        mean_score = gpas.mean()
        median_score = gpas.median()
        variance_score = gpas.var(ddof=1)
        stdev_score = gpas.std(ddof=1)
        min_score = gpas.min()
        max_score = gpas.max()

        # 10 bài toán đầu
        c1 = (gpas >= 8.0).sum()
        p1 = c1 / num_students

        c2 = ((gpas >= 7.0) & (gpas < 8.0)).sum()
        p2 = c2 / num_students

        c3 = (gpas > 5.0).sum()
        p3 = c3 / num_students

        c4_b = (study_hours >= 3.0).sum()
        c4_inter = ((study_hours >= 3.0) & (gpas >= 8.0)).sum()
        p4 = c4_inter / c4_b if c4_b > 0 else 0

        c5 = ((phone_hours < 4.0) & (gpas >= 7.0)).sum()
        p5 = c5 / num_students

        omega_2 = combination(2, num_students)
        c6_fav = combination(2, c1)
        p6 = c6_fav / omega_2 if omega_2 > 0 else 0

        c7_pool = (gpas >= 5.0).sum()
        c7_fav = combination(2, c7_pool)
        p7 = c7_fav / omega_2 if omega_2 > 0 else 0

        omega_3 = combination(3, num_students)
        c8_not = num_students - c1
        c8_none = combination(3, c8_not)
        p8 = 1 - (c8_none / omega_3) if omega_3 > 0 else 0

        c9_pool = (study_hours >= 4.0).sum()
        c9_fav = combination(2, c9_pool)
        p9 = c9_fav / omega_2 if omega_2 > 0 else 0

        c10_A = (gpas >= 7.0).sum()
        c10_B = (phone_hours < 3.0).sum()
        c10_inter = ((gpas >= 7.0) & (phone_hours < 3.0)).sum()
        p10 = (c10_A + c10_B - c10_inter) / num_students

        # Bài toán 11 & 12: Đổi nguyên nhân thành thời gian dùng điện thoại (< 3.5h và >= 3.5h) để Bayes ra số đẹp mắt hơn
        h1_count = (phone_hours < 3.5).sum()
        h2_count = (phone_hours >= 3.5).sum()
        p_h1 = h1_count / num_students
        p_h2 = h2_count / num_students

        h1_good = ((phone_hours < 3.5) & (gpas >= 8.0)).sum()
        h2_good = ((phone_hours >= 3.5) & (gpas >= 8.0)).sum()
        p_a_given_h1 = h1_good / h1_count if h1_count > 0 else 0
        p_a_given_h2 = h2_good / h2_count if h2_count > 0 else 0

        total_prob = (p_h1 * p_a_given_h1) + (p_h2 * p_a_given_h2)
        bayes_prob = (p_h1 * p_a_given_h1) / total_prob if total_prob > 0 else 0
        content_text = f"""
======================================================================
 [ PHẦN 1 ] — THỐNG KÊ MÔ TẢ (CÔNG THỨC TOÁN HỌC & ÁP DỤNG)
======================================================================
1. Điểm Trung Bình (Mean): x̄ = (∑ xi) / n = {mean_score:.2f}
2. Trung Vị (Median): Giá trị chính giữa dãy số = {median_score:.2f}
3. Phương Sai Mẫu (Variance): s² = [ ∑ (xi - x̄)² ] / (n - 1) = {variance_score:.2f}
4. Độ Lệch Chuẩn Mẫu (Standard Deviation): s = √s² = {stdev_score:.2f}
5. Giá trị Min = {min_score}  |  Max = {max_score}


======================================================================
 [ PHẦN 2 ] — HỆ THỐNG 12 BÀI TOÁN XÁC SUẤT CHI TIẾT
======================================================================

Bài toán 1: Xác suất chọn 1 sinh viên đạt loại Giỏi (Điểm ≥ 8.0)
   • Công thức : P(A) = n(A) / n(Ω) = {c1} / {num_students} = {p1:.4f} (~ {p1*100:.1f}%)

Bài toán 2: Xác suất chọn 1 sinh viên có điểm từ 7 đến dưới 8 (7.0 ≤ Điểm < 8.0)
   • Công thức : P(B) = n(7 ≤ Điểm < 8) / n(Ω) = {c2} / {num_students} = {p2:.4f} (~ {p2*100:.1f}%)

Bài toán 3: Xác suất chọn 1 sinh viên không bị điểm kém (Điểm > 5.0)
   • Công thức : P(C) = n(Điểm > 5) / n(Ω) = {c3} / {num_students} = {p3:.4f} (~ {p3*100:.1f}%)

Bài toán 4: Xác suất có điều kiện P(Điểm ≥ 8.0 | Học ≥ 3 giờ/ngày)
   • Công thức : P(A | D) = n(A ∩ D) / n(D) = {c4_inter} / {c4_b} = {p4:.4f} (~ {p4*100:.1f}%)

Bài toán 5: Xác suất đồng thời (Dùng ĐT < 4 giờ/ngày VÀ Điểm ≥ 7.0)
   • Công thức : P(E) = n(ĐT < 4h ∩ Điểm ≥ 7) / n(Ω) = {c5} / {num_students} = {p5:.4f} (~ {p5*100:.1f}%)

Bài toán 6: Xác suất chọn 2 sinh viên mà CẢ HAI đều đạt loại Giỏi (≥ 8.0)
   • Công thức : P = C(2, k) / C(2, n) = C(2, {c1}) / C(2, {num_students}) = {c6_fav} / {omega_2} = {p6:.4f} (~ {p6*100:.2f}%)

Bài toán 7: Xác suất chọn 2 sinh viên mà cả hai đều đạt từ trung bình trở lên (≥ 5.0)
   • Công thức : P = C(2, c7) / C(2, n) = C(2, {c7_pool}) / C(2, {num_students}) = {c7_fav} / {omega_2} = {p7:.4f} (~ {p7*100:.2f}%)

Bài toán 8: Xác suất chọn 3 sinh viên có ÍT NHẤT 1 sinh viên đạt loại Giỏi
   • Công thức : P = 1 - [ C(3, không_giỏi) / C(3, n) ] = 1 - ({c8_none} / {omega_3}) = {p8:.4f} (~ {p8*100:.2f}%)

Bài toán 9: Xác suất chọn 2 sinh viên mà cả hai đều có giờ tự học ≥ 4 giờ/ngày
   • Công thức : P = C(2, c9) / C(2, n) = C(2, {c9_pool}) / C(2, {num_students}) = {c9_fav} / {omega_2} = {p9:.4f} (~ {p9*100:.2f}%)

Bài toán 10: Xác suất theo quy tắc cộng (Điểm ≥ 7.0 HOẶC Dùng ĐT < 3 giờ/ngày)
   • Công thức : P(A ∪ F) = P(A) + P(F) - P(A ∩ F) = ({c10_A} + {c10_B} - {c10_inter}) / {num_students} = {p10:.4f} (~ {p10*100:.1f}%)

Bài toán 11: Công thức xác suất đầy đủ (Tính xác suất tổng thể một SV đạt loại Giỏi)
   • Giả thiết  : Chia lớp thành 2 nhóm theo thời gian dùng ĐT: H1 (< 3.5h/ngày) và H2 (≥ 3.5h/ngày)
   • Công thức : P(A) = P(H1)*P(A | H1) + P(H2)*P(A | H2)
   • Thay số   : P(A) = ({h1_count}/{num_students} * {h1_good}/{h1_count}) + ({h2_count}/{num_students} * {h2_good}/{h2_count})
   • Kết quả   : {total_prob:.4f} (~ {total_prob*100:.1f}%)

Bài toán 12: Công thức Bayes (Biết SV đạt loại Giỏi, tính xác suất thuộc nhóm dùng ĐT < 3.5h)
   • Công thức : P(H1 | A) = [ P(H1) * P(A | H1) ] / P(A)
   • Thay số   : P(H1 | A) = [ ({h1_count}/{num_students} * {h1_good}/{h1_count}) ] / {total_prob:.4f}
   • Kết quả   : {bayes_prob:.4f} (~ {bayes_prob*100:.2f}%)
"""
        text_area.insert(tk.END, content_text)
        text_area.config(state=tk.DISABLED)


# ==========================================
# CỬA SỔ 2: HÀM HIỂN THỊ BIỂU ĐỒ TRỰC QUAN
# ==========================================
def show_charts_window(df, gpas, study_hours, num_students):
    mean_score = gpas.mean()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Biểu đồ 1: Phân bố điểm
    ax1.hist(gpas, bins=8, color='#3498db', edgecolor='black', alpha=0.85)
    ax1.axvline(mean_score, color='red', linestyle='dashed', linewidth=2, label=f'Điểm TB (x̄): {mean_score:.2f}')
    ax1.set_title('Biểu đồ phân bố điểm trung bình', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Điểm trung bình', fontsize=10)
    ax1.set_ylabel('Số lượng sinh viên', fontsize=10)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Biểu đồ 2: Mối quan hệ giờ học vs điểm
    categories = ['< 2 giờ', '2 - 4 giờ', '> 4 giờ']
    avg_scores = [
        df[study_hours < 2.0]['Điểm TB'].mean() if not df[study_hours < 2.0].empty else 0,
        df[(study_hours >= 2.0) & (study_hours <= 4.0)]['Điểm TB'].mean() if not df[(study_hours >= 2.0) & (study_hours <= 4.0)].empty else 0,
        df[study_hours > 4.0]['Điểm TB'].mean() if not df[study_hours > 4.0].empty else 0
    ]
    ax2.bar(categories, avg_scores, color=['#e74c3c', '#f39c12', '#2ecc71'], edgecolor='black', alpha=0.85)
    ax2.set_title('Mối quan hệ: Số giờ học vs Điểm trung bình', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Số giờ học mỗi ngày', fontsize=10)
    ax2.set_ylabel('Điểm trung bình (GPA)', fontsize=10)
    ax2.set_ylim(0, 10)
    for i, v in enumerate(avg_scores):
        ax2.text(i, v + 0.2, f'{v:.2f}', ha='center', fontweight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# ==========================================
# CHẠY ỨNG DỤNG CHÍNH
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()