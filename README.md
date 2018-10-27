# AI_Lab01
Đồ án Thực hành cơ sở trí tuệ nhân tạo - LAB01
Thành viên:
- Lý Vĩnh Lợi: 1612348
- Nguyễn Hữu Trường: 1612756

# Giới thiệu
- Giao diện sử dụng module Tkinter
  - `pip install tkinter`

# Cách chạy
- Chạy file `__main__.py` từ dòng lệnh:
- Để hiển thị các lệnh được hỗ trợ:
  - `python __main__.py --help`
- Để chạy demo giao diện cho thuật toán A*
  - `python __main__.py gui`
- Để chạy demo thuật toán A* và ARA không đồ họa:
  - `python __main__.py astar -i input_file -o output_file -hf heuristic`
  - `python __main__.py ara -i input_file -o output_file -t time -hf heuristic`
  - Trong đó:
    - `input_file` là đường dẫn file input (một số file có sẵn được đặt trong thư mục test)
    - `output_file` là đường dẫn file để xuất kết quả, được truyền vào từ dòng lệnh
    - `heuristic` là một trong hai lựa chọn: euclidean và diagonal, mặc định là euclidean
    - `time` là thời gian giới hạn cho thuật toán ARA đơn vị là milliseconds, mặc định là 50

# Tạo file input ngẫu nhiên
- Mở file map_generator.py và sửa các giá trị
- Chạy file map_generator.py từ dòng lệnh
	python map_generator.py
- Kiểm tra file map được sinh ra (cùng thư mục với file map_generator.py)
- Lưu ý, đây chỉ là file test được tạo sơ khai, có thể bị lỗi

# Build executable file (file .exe trên Windows)
Yêu cầu:
- Cài đặt module PyInstaller từ dòng lệnh:
  - `pip install pyinstaller`
- Để build dạng nén (build xong chỉ có 1 file duy nhất):
  - `pyinstaller -y -F -i "E:/TaiLieuDaiHoc/CoSoTriTueNhanTao/AI_Lab01/images/appicon.ico" --add-data "E:/TaiLieuDaiHoc/CoSoTriTueNhanTao/AI_Lab01/images";"images/" -n 1612348_1612756_Lab01 --hidden-import tkinter  "E:/TaiLieuDaiHoc/CoSoTriTueNhanTao/AI_Lab01/__main__.py"`
- Để build dạng không nén (build ra 1 thư mục):
  - `pyinstaller -y -i "E:/TaiLieuDaiHoc/CoSoTriTueNhanTao/AI_Lab01/images/appicon.ico" --add-data "E:/TaiLieuDaiHoc/CoSoTriTueNhanTao/AI_Lab01/images";"images/" -n 1612348_1612756_Lab01 --hidden-import tkinter  "E:/TaiLieuDaiHoc/CoSoTriTueNhanTao/AI_Lab01/__main__.py"`
- *NOTE*: Sau khi chạy lần đầu sẽ sinh ra một file `1612348_1612756_Lab01.spec`. Lần sau khi cần build chỉ cần chạy:
  - `pyinstaller 1612348_1612756_Lab01.spec`
- Sau khi build xong sẽ có 2 thư mục được sinh ra
  - `build`: Chứa thư mục được build xong, thường có file log, file run, chưa bao gồm thư viện nên không chạy được
  - `dist`: Thư mục này đã có đầy đủ thư viện và thường là thư mục để người dùng chạy app. Thư mục này chứa:
    - File thực thi dạng nén **nếu build ở dạng nén**
    - Thư mục sản phẩm **nếu build ở dạng không nén**