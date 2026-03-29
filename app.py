import os
import sys
import logging
from contextlib import asynccontextmanager  # 异步上下文管理器

from fastapi import FastAPI, Request

# HTMLResponse 用于返回 HTML 页面，StreamingResponse 用于流式响应
from fastapi.responses import HTMLResponse, StreamingResponse

# 通常用于托管静态文件（如 CSS、JS），一般在要分离静态文件时使用
from fastapi.staticfiles import StaticFiles

# Pydantic 用于数据验证和序列化
from pydantic import BaseModel

# 把当前文件所在的目录，添加到系统路径中，确保可以导入 main 模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AdvancedGraphRAGSystem

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

rag_system = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 开始
    """Initialize the RAG system on startup."""
    global rag_system
    logger.info("Initializing RAG System...")
    try:
        rag_system = AdvancedGraphRAGSystem()
        rag_system.initialize_system()
        
        logger.info("Building/Loading Knowledge Base...")
        rag_system.build_knowledge_base()
        
        logger.info("RAG System Ready!")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        pass
    
    yield  # 只要服务器不关，就会一直停留在这
    
    # 结束
    if rag_system:
        rag_system._cleanup()

# lifespan 管理应用的启动和关闭过程
app = FastAPI(title="Cook RAG Assistant", lifespan=lifespan)

# Model for incoming chat requests
class ChatRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def get_root():
    """Serve the static HTML entry point."""
    try:
        # Construct absolute path to main.html
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(base_dir, "main.html")
        
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"<h1>Error: main.html not found at {html_path}</h1>"

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    if not rag_system or not rag_system.system_ready:
        return StreamingResponse(
            iter(["系统正在初始化，请稍后再试..."]), 
            media_type="text/plain"
        )
            
    question = request.question
    
    def response_generator():
        try:
            # 首先，路由查询以获取相关文档和分析
            relevant_docs, analysis = rag_system.query_router.route_query(question, rag_system.config.top_k)
            
            strategy_name = analysis.recommended_strategy.value
            complexity = analysis.query_complexity
            rel_intensity = analysis.relationship_intensity
            
            # 然后，生成响应头，yield的作用是生成一点内容就返回一点内容，实现流式响应，和return不同
            header = f"> **策略**: `{strategy_name}` | **复杂度**: {complexity:.2f} | **关联度**: {rel_intensity:.2f}\n\n---\n\n"
            yield header
            
            # 最后，基于选定的策略生成答案
            for chunk in rag_system.generation_module.generate_adaptive_answer_stream(question, relevant_docs):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            yield f"\n\n**系统错误**: {str(e)}"

    return StreamingResponse(response_generator(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
