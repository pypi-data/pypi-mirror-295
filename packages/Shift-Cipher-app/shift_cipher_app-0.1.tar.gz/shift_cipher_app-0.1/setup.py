from setuptools import setup, find_packages

setup(
    name="Shift_Cipher_app",  # Tên của gói
    version="0.1",  # Phiên bản
    packages=find_packages(),  # Tìm và đóng gói các modules
    include_package_data=True,  # Bao gồm cả các tệp tĩnh và templates
    install_requires=[
        "Flask",  # Nếu bạn đang sử dụng Flask cho web app
        # Các thư viện khác mà app cần, ví dụ: numpy, pandas
    ],
    author="Tên của bạn",
    author_email="email@example.com",
    description="Ứng dụng Shift Cipher với giao diện web",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/TheHuwn/ATBMTT.git",  # URL repo GitHub của bạn
)
