import uvicorn
from app.api.routes import app


if __name__ == "__main__":
    from app.core.config import settings
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
