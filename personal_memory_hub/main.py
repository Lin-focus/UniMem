# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import boto3
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(title="Personal Memory Hub - File Upload Service")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'md'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def validate_file(file: UploadFile):
    """Validate file format and size"""
    # Check file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")
    
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    return True

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "service": "Personal Memory Hub - File Upload Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload file to S3
    
    Parameters:
        file: Uploaded file
    
    Returns:
        JSON response with file information
    """
    
    # Validate file
    validate_file(file)
    
    try:
        # 1. Generate filename with timestamp + original filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = file.filename
        s3_key = f"uploads/{timestamp}_{original_filename}"
        
        print(f"📤 Starting file upload: {original_filename}")
        
        # 2. Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        print(f"📊 File size: {file_size / 1024:.2f} KB")
        
        # 3. Upload to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=file.content_type or 'application/octet-stream',
            Metadata={
                'original_filename': original_filename,
                'upload_timestamp': timestamp
            }
        )
        
        print(f"✅ Upload successful: {s3_key}")
        
        # 4. Generate file URL
        file_url = f"s3://{BUCKET_NAME}/{s3_key}"
        
        # 5. Return result
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "File uploaded successfully",
                "data": {
                    "original_filename": original_filename,
                    "s3_key": s3_key,
                    "file_url": file_url,
                    "file_size": file_size,
                    "file_extension": original_filename.split(".")[-1].lower(),
                    "upload_time": timestamp
                }
            }
        )
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

@app.get("/health")
def health_check():
    """Check if AWS connection is working"""
    try:
        # Test S3 connection
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        return {
            "status": "healthy",
            "s3_connection": "ok",
            "bucket": BUCKET_NAME
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "s3_connection": "failed",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Personal Memory Hub File Upload Service...")
    print(f"📦 S3 Bucket: {BUCKET_NAME}")
    print(f"🌍 Region: {os.getenv('AWS_REGION')}")
    uvicorn.run(app, host="0.0.0.0", port=8000)



