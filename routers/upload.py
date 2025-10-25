# 上传路由
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.s3_service import s3_service
from schemas import FileUploadResponse

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件到S3
    
    Parameters:
        file: 上传的文件
    
    Returns:
        JSON响应包含文件信息
    """
    file_data = await s3_service.upload_file(file)
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "File uploaded successfully",
            "data": file_data
        }
    )