import numpy as np
from datetime import timedelta
from pymongo import MongoClient
from datetime import datetime, timezone
from collections import defaultdict
import pandas as pd
import services.read_config as rc

# MONGO_URI = "mongodb://192.168.100.198:27017"
MONGO_URI= rc.read("database","url")
# DB_NAME = "SNK-MQTT"
DB_NAME = rc.read("database","collection_name")

def fetch_pressure_today(condition: str, limit=100):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # ดึงเฉพาะ collection หลัก (สมมติว่าชื่อ aircom_logs ตามที่คุณบันทึกจาก Node-RED)
    # หรือถ้ายังใช้หลาย collection ที่เริ่มด้วย aircom ก็ยังใช้ loop ได้แต่ไม่ต้อง merge key
    col = db[condition] 
    
    now = datetime.now(timezone.utc)
    start_of_day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=timezone.utc)

    # 1. ดึงข้อมูลตรงๆ ตามเงื่อนไข
    query = col.find({
        "timestamp": {"$gte": start_of_day, "$lte": end_of_day},
    }, {"_id": 0}).sort("timestamp", 1)

    if limit is not None:
        query = query.limit(limit)
        
    data = list(query)

    if not data:
        return [], []

    # 2. สร้าง DataFrame จากข้อมูลก้อนเดียวได้เลย
    df = pd.DataFrame(data)

    # 3. จัดการฟอร์แมตเวลา (แปลงจาก BSON Date เป็น String สำหรับหน้าบ้าน)
    if 'timestamp' in df.columns:
        # เก็บค่า timestamp ดั้งเดิมไว้ sort ก่อน แล้วค่อยเปลี่ยนเป็น string
        df = df.sort_values("timestamp") 
        df['timestamp'] = df['timestamp'] + timedelta(hours=7)
        df['timestamp'] = df['timestamp'].dt.strftime("%H:%M:%S")

    # 4. จัดลำดับคอลัมน์ (Priority Sorting)
    all_columns = df.columns.tolist()
    priority_cols = ['timestamp', 'line', 'type', 'factory']
    
    existing_priority = [c for c in priority_cols if c in all_columns]
    other_cols = sorted([c for c in all_columns if c not in existing_priority])
    
    final_column_order = existing_priority + other_cols

    # 5. Reindex และจัดการค่าว่าง
    df = df.reindex(columns=final_column_order)
    
    # เปลี่ยน NaN เป็น None เพื่อให้ API ส่งค่า null ได้ถูกต้อง
    # clean_data = df.where(pd.notnull(df), None).to_dict(orient='records')
    clean_data = df.replace({np.nan: 0}).to_dict(orient='records')

    return clean_data, final_column_order
    

def fetch_pressure_weekly(condition: str, limit=500):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # ใช้ Collection หลักที่เก็บข้อมูลแบบ Wide Format
    col = db[condition] 
    
    # 1. ตั้งค่าช่วงเวลา: เริ่มต้นจันทร์นี้ 00:00:00 ถึง ปลายวันนี้ 23:59:59
    now = datetime.now(timezone.utc)
    # หาวันจันทร์ที่ผ่านมา
    start_of_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_period = now.replace(hour=23, minute=59, second=59, microsecond=0)

    # 2. ดึงข้อมูลตรงๆ ตามเงื่อนไขช่วงสัปดาห์
    query = col.find({
        "timestamp": {"$gte": start_of_week, "$lte": end_of_period},
    }, {"_id": 0}).sort("timestamp", 1)

    # สำหรับรายสัปดาห์ ข้อมูลอาจจะเยอะ แนะนำให้เพิ่ม limit ตามความเหมาะสม
    if limit is not None:
        query = query.limit(limit)
        
    data = list(query)

    if not data:
        return [], []

    # 3. สร้าง DataFrame จากข้อมูลก้อนเดียว
    df = pd.DataFrame(data)

    # 4. จัดการฟอร์แมตเวลา (รายสัปดาห์ควรมี วันที่ ติดไปด้วยเพื่อให้ไม่งง)
    if 'timestamp' in df.columns:
        df = df.sort_values("timestamp")
        # ใช้ Format: 2026-04-10 13:15:00
        df['timestamp'] = df['timestamp'] + timedelta(hours=7)
        df['timestamp'] = df['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 5. จัดลำดับคอลัมน์ (Priority Sorting)
    all_columns = df.columns.tolist()
    priority_cols = ['timestamp', 'line', 'type', 'factory']
    
    existing_priority = [c for c in priority_cols if c in all_columns]
    other_cols = sorted([c for c in all_columns if c not in existing_priority])
    
    final_column_order = existing_priority + other_cols

    # 6. Reindex และแปลงเป็น List of Dict
    df = df.reindex(columns=final_column_order)
    # clean_data = df.where(pd.notnull(df), None).to_dict(orient='records')
    clean_data = df.replace({np.nan: 0}).to_dict(orient='records')

    return clean_data, final_column_order

def fetch_pressure_monthly(condition: str, limit=1000):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # ใช้ Collection เดียวที่เก็บข้อมูลแบบ Wide Format
    col = db[condition] 
    
    # 1. ตั้งค่าช่วงเวลา: เริ่มต้นวันที่ 1 ของเดือนนี้ 00:00:00 ถึง ปลายวันนี้ 23:59:59
    now = datetime.now(timezone.utc)
    # ใช้ .replace เพื่อตั้งค่าเป็นวันที่ 1 ของเดือนปัจจุบัน
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_period = now.replace(hour=23, minute=59, second=59, microsecond=0)

    # 2. ดึงข้อมูลตรงๆ (ไม่ต้องวนลูปหลาย Collection และไม่ต้อง Merge เองแล้ว)
    query = col.find({
        "timestamp": {"$gte": start_of_month, "$lte": end_of_period},
    }, {"_id": 0}).sort("timestamp", 1)

    # ข้อมูลรายเดือนอาจจะหนาแน่น ควรตั้ง limit ไว้กัน API ค้าง
    if limit is not None:
        query = query.limit(limit)
        
    data = list(query)

    if not data:
        return [], []

    # 3. สร้าง DataFrame
    df = pd.DataFrame(data)

    # 4. จัดการฟอร์แมตเวลาให้แสดงผลในตารางสวยๆ
    if 'timestamp' in df.columns:
        # เรียงลำดับก่อนแปลงเป็น String เพื่อให้ลำดับในกราฟไม่เพี้ยน
        df = df.sort_values("timestamp")
        # Format: 2026-04-10 13:15:00
        df['timestamp'] = df['timestamp'] + timedelta(hours=7)
        df['timestamp'] = df['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 5. จัดลำดับคอลัมน์ (Priority Sorting)
    all_columns = df.columns.tolist()
    priority_cols = ['timestamp', 'line', 'type', 'factory']
    
    existing_priority = [c for c in priority_cols if c in all_columns]
    other_cols = sorted([c for c in all_columns if c not in existing_priority])
    
    final_column_order = existing_priority + other_cols

    # 6. Reindex และจัดการค่าว่าง (NaN -> None)
    df = df.reindex(columns=final_column_order)
    # clean_data = df.where(pd.notnull(df), None).to_dict(orient='records')
    clean_data = df.replace({np.nan:0}).to_dict(orient='records')

    return clean_data, final_column_order