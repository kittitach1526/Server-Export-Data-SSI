from fastapi import APIRouter
# from typing import List
# from services.aircom import *
# import ฟังก์ชันดึงข้อมูลของคุณมาที่นี่
# from services.data_service import fetch_aircom_today, fetch_aircom_weekly, fetch_aircom_monthly
# import math
from typing import Optional
from services.export_data import *

router = APIRouter(
    prefix="/api/export", # กำหนด Prefix เริ่มต้นของทุก Route ในไฟล์นี้
    tags=["Export System"] # จัดกลุ่มในหน้า /docs
)


@router.get("")
async def export_aircom_data(
    condition: str, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
):
    try:
        # เรียกใช้ฟังก์ชันที่ปรับปรุงไว้ด้านบน
        # condition = "aircom_55"
        data, columns = fetch_range(condition, start_date, end_date)
        
        return {
            "status": "success",
            "data": data,
            "columns": columns,
            "count": len(data)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }