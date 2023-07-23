import logging
from fastapi import Request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.basicConfig(filename='app.log', level=logging.DEBUG)

class CustomLoggerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)

        # Logları dosyaya yaz
        logger.info(
            f"Request received: {request.method} {request.url.path} - Headers: {request.headers}"
        )

        try:
            response = await self.app(scope, receive, send)
            if response is not None:
                logger.info(
                    f"Response sent: {response.status_code} - Headers: {response.headers}"
                )
            return response
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            raise e

