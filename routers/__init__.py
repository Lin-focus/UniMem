# 导出路由
from .upload import router as upload_router
from .embedding import router as embedding_router

__all__ = ['upload_router', 'embedding_router']