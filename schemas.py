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

# 搜索相关
class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    threshold: float = 0.7

class MemoryUnit(BaseModel):
    id: str
    content: str
    memory_type: str  # text, image, audio, document
    embedding: Optional[List[float]] = None  # 可选字段，搜索时不返回
    metadata: dict
    created_at: str
    updated_at: str
    source: Optional[str] = None
    summary: Optional[str] = None
    tags: List[str] = []

class SearchResult(BaseModel):
    memory: MemoryUnit
    similarity_score: float
    search_time: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int
    search_time: float

# AI Agent相关
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    use_memory: bool = True

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    relevant_memories: List[dict]
    context_used: int
    timestamp: str

# 健康检查
class HealthCheckResponse(BaseModel):
    status: str
    services: dict