from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path

from ..core.config import settings
from ..core.llm import LLMClient
from ..core.search import SimpleSearchEngine
from ..services.wiki_compiler import WikiCompiler
from ..services.qa_system import QASystem
from ..services.output_renderer import OutputRenderer
from ..services.embeddings import EmbeddingsService
from ..services.export import ExportService


# Initialize services
llm_client = LLMClient(
    api_key=settings.anthropic_api_key,
    model=settings.model,
)

# Initialize embeddings and search services early
embeddings_service = EmbeddingsService()
search_engine = SimpleSearchEngine(settings.wiki_path, embeddings_service=embeddings_service)
wiki_compiler = WikiCompiler(settings.raw_data_path, settings.wiki_path, llm_client)
qa_system = QASystem(settings.wiki_path, llm_client, search_engine)
output_renderer = OutputRenderer(settings.output_path)

# Initialize export service
export_service = ExportService(settings.wiki_path, settings.output_path, embeddings_service)


# Request/Response models
class CompileRequest(BaseModel):
    source_path: str
    title: Optional[str] = None


class QueryRequest(BaseModel):
    question: str
    max_sources: int = 5
    output_format: str = "markdown"
    follow_links: bool = True
    max_total_docs: int = 10


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class HealthResponse(BaseModel):
    status: str
    wiki_articles: int
    raw_documents: int


# Create FastAPI app
app = FastAPI(title="LLM Knowledge Base API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    wiki_count = len(list(settings.wiki_path.rglob("*.md")))
    raw_count = len(list(settings.raw_data_path.rglob("*"))) if settings.raw_data_path.exists() else 0
    
    return HealthResponse(
        status="healthy",
        wiki_articles=wiki_count,
        raw_documents=raw_count,
    )


@app.post("/wiki/compile")
async def compile_document(request: CompileRequest):
    """Compile a raw document into wiki format"""
    try:
        wiki_path = wiki_compiler.compile_document(request.source_path, request.title)
        search_engine.refresh()
        # Update backlinks for connection strength
        backlinks = wiki_compiler.generate_backlinks_index()
        search_engine.set_backlinks(backlinks)
        return {
            "status": "success",
            "message": f"Document compiled successfully",
            "wiki_path": wiki_path,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/wiki/compile-all")
async def compile_all():
    """Compile all raw documents"""
    try:
        count = wiki_compiler.compile_all()
        search_engine.refresh()
        # Update backlinks for connection strength
        backlinks = wiki_compiler.generate_backlinks_index()
        search_engine.set_backlinks(backlinks)
        return {
            "status": "success",
            "message": f"Compiled {count} documents",
            "compiled_count": count,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/wiki/index")
async def get_wiki_index():
    """Get wiki index/table of contents"""
    try:
        index = wiki_compiler.generate_index()
        return {
            "status": "success",
            "index": index,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/wiki/refresh")
async def refresh_wiki():
    """Refresh the search index after adding new documents"""
    try:
        search_engine.refresh()
        # Update backlinks for connection strength
        backlinks = wiki_compiler.generate_backlinks_index()
        search_engine.set_backlinks(backlinks)
        return {
            "status": "success",
            "message": "Search index refreshed",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/wiki/backlinks")
async def get_backlinks():
    """Get wiki backlinks"""
    try:
        backlinks = wiki_compiler.generate_backlinks_index()
        return {
            "status": "success",
            "backlinks": backlinks,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/search")
async def search(request: SearchRequest):
    """Search the wiki"""
    try:
        results = search_engine.search(request.query, limit=request.limit)
        return {
            "status": "success",
            "query": request.query,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/qa/query")
async def query(request: QueryRequest):
    """Query the knowledge base"""
    try:
        answer = qa_system.query(
            question=request.question,
            max_sources=request.max_sources,
            output_format=request.output_format,
            follow_links=request.follow_links,
            max_total_docs=request.max_total_docs,
        )
        
        # Optionally save output
        output_path = output_renderer.save_markdown(
            answer,
            f"query-{len(list(settings.output_path.glob('*.md')))}",
        )
        
        return {
            "status": "success",
            "question": request.question,
            "answer": answer,
            "output_path": output_path,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/qa/summarize")
async def summarize(request: SearchRequest):
    """Search and summarize a topic"""
    try:
        summary = qa_system.search_and_summarize(request.query)
        
        output_path = output_renderer.save_markdown(
            summary,
            f"summary-{request.query.replace(' ', '-')[:30]}",
        )
        
        return {
            "status": "success",
            "topic": request.query,
            "summary": summary,
            "output_path": output_path,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Export endpoints for sharing
@app.post("/export/jsonl")
async def export_jsonl():
    """Export knowledge base as JSONL (machine-readable format)"""
    try:
        output_file = export_service.export_jsonl()
        return {
            "status": "success",
            "format": "jsonl",
            "file": str(output_file),
            "message": "Knowledge base exported as JSONL for sharing and reuse",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/export/sqlite")
async def export_sqlite():
    """Export knowledge base as searchable SQLite database"""
    try:
        output_file = export_service.export_sqlite()
        return {
            "status": "success",
            "format": "sqlite",
            "file": str(output_file),
            "message": "Knowledge base exported as SQLite for local search",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/export/html")
async def export_html():
    """Export knowledge base as single shareable HTML page"""
    try:
        output_file = export_service.export_html()
        return {
            "status": "success",
            "format": "html",
            "file": str(output_file),
            "message": "Knowledge base exported as HTML for web sharing",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/export/metadata")
async def export_metadata():
    """Export dataset metadata (JSON-LD + manifest)"""
    try:
        output_file = export_service.export_metadata()
        return {
            "status": "success",
            "format": "json",
            "file": str(output_file),
            "message": "Dataset metadata exported for discoverability",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/export/all")
async def export_all():
    """Export knowledge base in all formats (JSONL, SQLite, HTML, metadata)"""
    try:
        results = export_service.export_all()
        return {
            "status": "success",
            "formats": list(results.keys()),
            "files": {k: str(v) for k, v in results.items()},
            "message": "Knowledge base exported in all formats for maximum compatibility",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
