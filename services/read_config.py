import configparser
import os

# 1. สร้าง Object สำหรับอ่าน Config
config = configparser.ConfigParser()

# 2. ระบุไฟล์ที่ต้องการอ่าน (ใส่ path ให้ถูกต้อง)
# แนะนำให้ใช้ os.path เพื่อป้องกันปัญหาเรื่อง Directory
file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(file_path, encoding='utf-8')

def read(title:str,key:str):
    result = config.get(title, key)
    return result
