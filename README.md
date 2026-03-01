# Password Strength Checker

Script đơn giản kiểm tra độ mạnh của các mật khẩu có trong một file (mỗi dòng 1 mật khẩu).

Yêu cầu kiểm tra (theo yêu cầu):
- Mật khẩu phải dài tối thiểu 6 ký tự (mặc định 6)
- Có chữ thường, chữ in hoa, chữ số và ký tự đặc biệt
- Không nằm trong danh sách mật khẩu phổ biến (`common_passwords.txt`)

Files:
- [password_checker.py](password_checker.py)
- [common_passwords.txt](common_passwords.txt)
- [sample_passwords.txt](sample_passwords.txt)

Ví dụ chạy (Windows):
```powershell
python password_checker.py sample_passwords.txt
```

Options:
- `--common` hoặc `-c`: chỉ định file danh sách mật khẩu phổ biến khác
- `--both-common` hoặc `-b`: khi set, script sẽ kết hợp file do bạn chỉ định (via `-c`) với file `common_passwords.txt` có sẵn và so sánh với tập hợp hợp nhất
- `--min-length` hoặc `-m`: thay đổi chiều dài tối thiểu (mặc định 6)

Exit code:
- `0` nếu tất cả mật khẩu đều đạt
- `1` nếu có mật khẩu yếu
- `2` nếu file đầu vào không tìm thấy

Gợi ý: mở rộng `common_passwords.txt` bằng danh sách phổ biến hơn nếu cần.
