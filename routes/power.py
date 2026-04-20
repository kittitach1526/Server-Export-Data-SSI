from fastapi import APIRouter
# from typing import List
from services.power import *
# import ฟังก์ชันดึงข้อมูลของคุณมาที่นี่'
from services.aircom import *
import math

def clean_nan(obj):
    """ฟังก์ชันทำความสะอาดข้อมูล: เปลี่ยน NaN ให้เป็น 0.0 เพื่อไม่ให้ JSON พัง"""
    if isinstance(obj, list):
        return [clean_nan(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0  # บังคับให้เป็น 0.0
    return obj

router = APIRouter(
    prefix="/api/power", # กำหนด Prefix เริ่มต้นของทุก Route ในไฟล์นี้
    tags=["Power System"] # จัดกลุ่มในหน้า /docs
)

@router.get("/power-5-5-today")
async def get_power_5_5_today():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_aircom_today(condition="power_55",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/power-6-5-today")
async def get_power_6_5_today():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_power_today(condition="power_65",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/power-7-today")
async def get_power_7_today():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_power_today(condition="power_7",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }


@router.get("/power-5-5-week")
async def get_power_5_5_week():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_power_weekly(condition="power_55",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/power-6-5-week")
async def get_power_6_5_week():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_power_weekly(condition="power_65",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/power-7-week")
async def get_power_7_week():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_power_weekly(condition="power_7",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/power-5-5-month")
async def get_power_monthly_data_5_5():
    data, cols = fetch_power_monthly(condition="power_55",limit=None)
    return {
        "status": "success",
        "month": datetime.now().strftime("%B %Y"),
        "count": len(data),
        "columns": cols,
        "data": data
    }

@router.get("/power-6-5-month")
async def get_power_monthly_data_6_5():
    data, cols = fetch_power_monthly(condition="power_65",limit=None)
    return {
        "status": "success",
        "month": datetime.now().strftime("%B %Y"),
        "count": len(data),
        "columns": cols,
        "data": data
    }

@router.get("/power-7-month")
async def get_power_monthly_data_7():
    data, cols = fetch_power_monthly(condition="power_7",limit=None)
    return {
        "status": "success",
        "month": datetime.now().strftime("%B %Y"),
        "count": len(data),
        "columns": cols,
        "data": data
    }