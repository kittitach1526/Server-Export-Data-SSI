from fastapi import APIRouter
# from typing import List
from services.aircom import *
# import ฟังก์ชันดึงข้อมูลของคุณมาที่นี่
# from services.data_service import fetch_aircom_today, fetch_aircom_weekly, fetch_aircom_monthly
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
    prefix="/api/aircom", # กำหนด Prefix เริ่มต้นของทุก Route ในไฟล์นี้
    tags=["Air Compressor System"] # จัดกลุ่มในหน้า /docs
)


@router.get("/aircom-5-5-today")
async def get_aircom_5_5_today():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_aircom_today(condition="aircom_55",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/aircom-6-5-today")
async def get_aircom_6_5_today():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_aircom_today(condition="aircom_65",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/aircom-7-today")
async def get_aircom_7_today():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_aircom_today(condition="aircom_7",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/aircom-5-5-week")
async def get_aircom_5_5_week():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_aircom_weekly(condition="aircom_55",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/aircom-6-5-week")
async def get_aircom_6_5_week():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_aircom_weekly(condition="aircom_65",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/aircom-7-week")
async def get_aircom_7_week():
    # รับค่า 2 อย่างคือ ข้อมูลที่เรียงแล้ว และ รายชื่อหัวตารางที่เรียงแล้ว
    data, sorted_columns = fetch_aircom_weekly(condition="aircom_7",limit=None)
    
    return {
        "status": "success",
        "count": len(data),
        "columns": sorted_columns, 
        "data": data
    }

@router.get("/aircom-5-5-month")
async def get_monthly_data_5_5():
    data, cols = fetch_aircom_monthly(condition="aircom_55",limit=None)
    return {
        "status": "success",
        "month": datetime.now().strftime("%B %Y"),
        "count": len(data),
        "columns": cols,
        "data": data
    }

@router.get("/aircom-6-5-month")
async def get_monthly_data_6_5():
    data, cols = fetch_aircom_monthly(condition="aircom_65",limit=None)
    return {
        "status": "success",
        "month": datetime.now().strftime("%B %Y"),
        "count": len(data),
        "columns": cols,
        "data": data
    }

@router.get("/aircom-7-month")
async def get_monthly_data_7():
    data, cols = fetch_aircom_monthly(condition="aircom_7",limit=None)
    return {
        "status": "success",
        "month": datetime.now().strftime("%B %Y"),
        "count": len(data),
        "columns": cols,
        "data": data
    }

