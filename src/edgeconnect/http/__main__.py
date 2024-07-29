import uvicorn

from edgeconnect import config

if __name__ == "__main__":  # pragma: nocover
    uvicorn.run(
        app="edgeconnect.http:api",
        host=config.SERVER_HOST,
        port=int(config.SERVER_PORT),
        log_config=config.LOG_CONFIG,
        limit_concurrency=config.SERVER_CONCURRENCY_LIMIT,
    )
