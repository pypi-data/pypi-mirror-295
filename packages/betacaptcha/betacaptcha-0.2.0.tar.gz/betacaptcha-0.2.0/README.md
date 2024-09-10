
# BetaCaptcha Python Client

Repository này chứa một client Python đơn giản để tương tác với API của BetaCaptcha. Client cung cấp các phương thức để chuyển đổi hình ảnh thành văn bản thông qua giải CAPTCHA, truy xuất số dư tài khoản, và giải các loại CAPTCHA khác nhau bao gồm hình ảnh CAPTCHA và reCAPTCHA.

## Cài đặt

Để sử dụng client này, bạn cần cài đặt Python. Bạn có thể cài đặt các thư viện cần thiết bằng cách sử dụng `pip`:

```bash
pip install requests
pip install betacaptcha
```

## Cấu hình

Đầu tiên, bạn cần có khóa API từ [BetaCaptcha](https://betacaptcha.com).

Sau đó, bạn có thể thiết lập client như sau:

```python
import os
from betacaptcha import BetaCaptcha

# Đặt khóa API của bạn trong biến môi trường để tăng cường bảo mật
api_key = os.getenv("BETACAPTCHA_API_KEY")
if api_key:
    client = BetaCaptcha(API_KEY=api_key)
else:
    raise ValueError("API key is not set. Please set the BETACAPTCHA_API_KEY environment variable.")
```

Hoặc bạn có thể khởi tạo trực tiếp client với khóa API của mình:

```python
from betacaptcha import BetaCaptcha
client = BetaCaptcha(API_KEY="your_api_key_here")
```

## Sử dụng

### Kiểm tra số dư tài khoản

Bạn có thể kiểm tra số dư tài khoản của mình với phương thức sau:

```python
balance = client.get_balance()
print("Số dư tài khoản của bạn là:", balance)
```

### Chuyển đổi hình ảnh thành văn bản

Để chuyển đổi một hình ảnh CAPTCHA thành văn bản:

```python
text_result = client.image_to_text(file="path_to_your_image.png")
print("Văn bản CAPTCHA:", text_result)
```

Bạn cũng có thể cung cấp dữ liệu hình ảnh dưới dạng chuỗi base64:

```python
image_data = client.image_to_base64("path_to_your_image.png")
text_result = client.image_to_text(image_as_base64=image_data)
print("Văn bản CAPTCHA:", text_result)
```

### Giải reCAPTCHA

Để giải một reCAPTCHA:

```python
sitekey = "your_sitekey_here"
siteurl = "https://www.example.com"
recaptcha_result = client.recaptcha(sitekey=sitekey, siteurl=siteurl)
print("Kết quả reCAPTCHA:", recaptcha_result)
```

### Giải Funcaptcha Image CAPTCHA

Để giải một Funcaptcha image CAPTCHA:

```python
imginstructions = "Click vào các hình ảnh của mèo"
funcaptcha_result = client.funcaptcha_image(imginstructions=imginstructions, file="path_to_your_image.png")
print("Kết quả Funcaptcha:", funcaptcha_result)
```

## Xử lý lỗi

Nếu khóa API không được đặt hoặc thiếu bất kỳ tham số bắt buộc nào, các phương thức sẽ phát sinh lỗi `RuntimeError` hoặc `ValueError`.

## Giấy phép

Dự án này được cấp phép theo Giấy phép MIT - xem tệp LICENSE để biết thêm chi tiết.

## Liên hệ

Đối với bất kỳ yêu cầu hoặc vấn đề nào, vui lòng liên hệ hỗ trợ tại [BetaCaptcha](https://betacaptcha.com).

