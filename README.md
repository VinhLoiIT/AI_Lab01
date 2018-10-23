# AI_Lab01
Đồ án Thực hành cơ sở trí tuệ nhân tạo - LAB01
Thành viên:
- Lý Vĩnh Lợi: MSSV 1612348
- Nguyễn Hữu Trường: MSSV 1612756

# Giới thiệu
- Giao diện sử dụng module Tkinter

# Cách chạy
- Chạy file __main__.py từ dòng lệnh:
++ Để hiển thị các lệnh được hỗ trợ:
	python __main__.py --help
++ Để chạy demo giao diện cho thuật toán A*
	python __main__.py gui
++ Để chạy demo thuật toán A* và ARA không đồ họa:
	python __main__.py astar -i input_file -o output_file -hf heuristic
	python __main__.py ara -i input_file -o output_file -t time -c coefficient -hf heuristic
	Trong đó:
		input_file là đường dẫn file input (một số file có sẵn được đặt trong thư mục test)
		output_file là đường dẫn file để xuất kết quả, được truyền vào từ dòng lệnh
		heuristic là một trong hai lựa chọn: euclidean và diagonal, mặc định là euclidean
		time là thời gian giới hạn cho thuật toán ARA đơn vị là giây, mặc định là 3.0
		coefficient là hệ số hàm heuristic, mặc định là 3
	
- Chọn button Load map để load một file test
- Chọn button Step để chạy từng bước một
- Chọn button Fast Forward để chạy nhanh
- Chọn button Restart để chạy lại 

# Tạo file input ngẫu nhiên
- Mở file map_generator.py và sửa các giá trị
- Chạy file map_generator.py từ dòng lệnh
	python map_generator.py
- Kiểm tra file map được sinh ra (cùng thư mục với file map_generator.py)
- Lưu ý, đây chỉ là file test được tạo sơ khai