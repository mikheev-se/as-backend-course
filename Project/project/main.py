import uvicorn
from project.core.settings import settings
from project.server import app


def main():
    uvicorn.run(
        'server:app',
        host=settings.host,
        port=settings.port,
        reload=True
    )


if __name__ == '__main__':
    main()
