# schemas.py
from pydantic import BaseModel
from typing import List, Optional

# 文件上传相关
class FileUploadResponse(BaseModel):
    success: bool
    message: str
    data: dict

# Embedding相关
class EmbeddingRequest(BaseModel):
    text: str
    input_type: str = "passage"  # "passage" or "query"

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dimension: int
    model: str

class BatchEmbeddingRequest(BaseModel):
    texts: List[str]
    input_type: str = "passage"

class BatchEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    count: int
    dimension: int

# 健康检查
class HealthCheckResponse(BaseModel):
    status: str
    services: dict