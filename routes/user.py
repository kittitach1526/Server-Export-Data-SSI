from fastapi import APIRouter

router = APIRouter(
    prefix="/api/user", # กำหนด Prefix เริ่มต้นของทุก Route ในไฟล์นี้
    tags=["User System"] # จัดกลุ่มในหน้า /docs
)

@router.get("/login")
async def login():
    pass
    
    
    