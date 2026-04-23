from fastapi import APIRouter
# from typing import List
from services.aircom import *
# import ฟังก์ชันดึงข้อมูลของคุณมาที่นี่
# from services.data_service import fetch_aircom_today, fetch_aircom_weekly, fetch_aircom_monthly
import math
from typing import Optional

import numpy as np # อย่าลืม import numpy ไว้ด้านบนสุด
from datetime import timedelta
from pymongo import MongoClient
from datetime import datetime, timezone
from collections import defaultdict
import pandas as pd
import services.read_config as rc


def fetch_range(condition: str, start_str: str = None, end_str: str = None):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[condition] 

    # การตั้งค่าช่วงเวลา (Default เป็นวันนี้ถ้าไม่ส่งค่ามา)
    if start_str and end_str:
        # รับค่า format "YYYY-MM-DD" จากหน้าบ้าน
        start_dt = datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        # สิ้นสุดวันที่เลือก เวลา 23:59:59
        end_dt = datetime.strptime(end_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    else:
        # Default: Today
        now = datetime.now(timezone.utc)
        start_dt = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        end_dt = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=timezone.utc)

    # 1. Query ข้อมูลตามช่วงเวลา
    query = col.find({
        "timestamp": {"$gte": start_dt, "$lte": end_dt},
    }, {"_id": 0}).sort("timestamp", 1)
        
    data = list(query)
    if not data:
        return [], []

    # 2. สร้าง DataFrame
    df = pd.DataFrame(data)

    # 3. จัดการฟอร์แมตเวลา (UTC -> GMT+7)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values("timestamp") 
        df['timestamp'] = df['timestamp']
        # ถ้าเลือกช่วงหลายวัน ควรมี วันที่ติดไปด้วยใน CSV
        df['timestamp'] = df['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 4. จัดลำดับคอลัมน์ (เหมือนเดิมครบถ้วน)
    all_columns = df.columns.tolist()
    priority_cols = ['timestamp', 'line', 'type', 'factory']
    existing_priority = [c for c in priority_cols if c in all_columns]
    other_cols = sorted([c for c in all_columns if c not in existing_priority])
    final_column_order = existing_priority + other_cols

    # 5. Reindex และจัดการค่าว่าง
    df = df.reindex(columns=final_column_order)
    clean_data = df.replace({np.nan: 0}).to_dict(orient='records')

    return clean_data, final_column_order