import numpy as np
import pandas as pd

# Cố định seed để dữ liệu sinh ra không đổi mỗi lần chạy
np.random.seed(2026)
num_students = 50

# Sinh dữ liệu phân phối hợp lý cho 50 sinh viên
study_hours = np.round(np.clip(np.random.normal(3.5, 1.0, num_students), 1.5, 6.0), 1)
phone_hours = np.round(np.clip(np.random.normal(3.2, 1.2, num_students), 1.0, 7.0), 1)

# Công thức cân bằng để điểm trung bình quanh mức 7.4 và có khoảng 12-14 sinh viên đạt >= 8 điểm
base_score = 4.3 + (study_hours * 0.95) - (phone_hours * 0.1) + np.random.normal(0, 0.35, num_students)
gpa = np.round(np.clip(base_score, 4.0, 10.0), 2)

# Gom thành DataFrame và lưu vào file dataset.csv
df = pd.DataFrame({
    'SV': range(1, num_students + 1),
    'Điểm TB': gpa,
    'Số giờ học/ngày': study_hours,
    'Số giờ dùng ĐT': phone_hours
})

df.to_csv('dataset.csv', index=False, encoding='utf-8-sig')
print("Đã tạo thành công file 'dataset.csv' với 50 sinh viên!")