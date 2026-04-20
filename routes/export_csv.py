from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
import pandas as pd
import io
import math
from datetime import datetime
from services.aircom import fetch_aircom_today, fetch_aircom_weekly, fetch_aircom_monthly
from services.power import fetch_power_today, fetch_power_weekly, fetch_power_monthly
from services.flow import fetch_flow_today, fetch_flow_weekly, fetch_flow_monthly
from services.pressure import fetch_pressure_today, fetch_pressure_weekly, fetch_pressure_monthly

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
    prefix="/api/export",
    tags=["CSV Export"]
)

def create_csv_response(data: list, filename: str) -> StreamingResponse:
    """สร้าง CSV response จากข้อมูล"""
    if not data:
        return Response("No data available", media_type="text/plain")
    
    # ทำความสะอาดข้อมูลก่อนสร้าง CSV
    clean_data = clean_nan(data)
    
    df = pd.DataFrame(clean_data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    response = StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),  # utf-8-sig for BOM
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
    return response

# AirCom CSV Export
@router.get("/aircom/{condition}/today/csv")
async def export_aircom_today_csv(condition: str):
    data, _ = fetch_aircom_today(condition, limit=None)  # No limit for export
    filename = f"aircom_{condition}_today_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/aircom/{condition}/week/csv")
async def export_aircom_week_csv(condition: str):
    data, _ = fetch_aircom_weekly(condition, limit=None)  # No limit for export
    filename = f"aircom_{condition}_week_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/aircom/{condition}/month/csv")
async def export_aircom_month_csv(condition: str):
    data, _ = fetch_aircom_monthly(condition, limit=None)  # No limit for export
    filename = f"aircom_{condition}_month_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

# Power CSV Export
@router.get("/power/{condition}/today/csv")
async def export_power_today_csv(condition: str):
    data, _ = fetch_power_today(condition, limit=None)  # No limit for export
    filename = f"power_{condition}_today_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/power/{condition}/week/csv")
async def export_power_week_csv(condition: str):
    data, _ = fetch_power_weekly(condition, limit=None)  # No limit for export
    filename = f"power_{condition}_week_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/power/{condition}/month/csv")
async def export_power_month_csv(condition: str):
    data, _ = fetch_power_monthly(condition, limit=None)  # No limit for export
    filename = f"power_{condition}_month_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

# Flow CSV Export
@router.get("/flow/{condition}/today/csv")
async def export_flow_today_csv(condition: str):
    data, _ = fetch_flow_today(condition, limit=None)  # No limit for export
    filename = f"flow_{condition}_today_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/flow/{condition}/week/csv")
async def export_flow_week_csv(condition: str):
    data, _ = fetch_flow_weekly(condition, limit=None)  # No limit for export
    filename = f"flow_{condition}_week_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/flow/{condition}/month/csv")
async def export_flow_month_csv(condition: str):
    data, _ = fetch_flow_monthly(condition, limit=None)  # No limit for export
    filename = f"flow_{condition}_month_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

# Pressure CSV Export
@router.get("/pressure/{condition}/today/csv")
async def export_pressure_today_csv(condition: str):
    data, _ = fetch_pressure_today(condition, limit=None)  # No limit for export
    filename = f"pressure_{condition}_today_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/pressure/{condition}/week/csv")
async def export_pressure_week_csv(condition: str):
    data, _ = fetch_pressure_weekly(condition, limit=None)  # No limit for export
    filename = f"pressure_{condition}_week_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)

@router.get("/pressure/{condition}/month/csv")
async def export_pressure_month_csv(condition: str):
    data, _ = fetch_pressure_monthly(condition, limit=None)  # No limit for export
    filename = f"pressure_{condition}_month_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return create_csv_response(data, filename)
