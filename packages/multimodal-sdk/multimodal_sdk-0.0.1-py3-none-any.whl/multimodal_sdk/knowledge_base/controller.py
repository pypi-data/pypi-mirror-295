import aiohttp
import os
import logging
from multimodal_sdk.common.refresh import token_refresh_handler
from multimodal_sdk.common.http_status_handler import HTTPStatusHandler
from multimodal_sdk.common.decorators import log_and_authorize
from multimodal_sdk.knowledge_base.poll_task_status import PollTaskStatusNamespace

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@token_refresh_handler
@log_and_authorize
@HTTPStatusHandler(201)
async def create_collection_func(
    kb_resource_id,
    collection_name,
    ingestion_strategy,
    distance_method=None,
    main_lang=None,
    chunk_strategy=None,
    embedding_strategy=None,
    **kwargs
):
    payload = {
        "name": collection_name,
        "ingestion_strategy": {
            "for_types": ingestion_strategy
        },
        "distance_method": distance_method if distance_method else "cosine",
        "main_lang": main_lang if main_lang else "en",
        "chunk_strategy": chunk_strategy if chunk_strategy else {"active": "true", "max_size": "auto"}
    }

    if embedding_strategy is not None:
        payload["embedding_strategy"] = embedding_strategy
    
    logger.info("KnowledgeBase: create_collection payload: %s", payload)
    
    url = f"{kwargs['base_url']}/knowledge-bases/{kb_resource_id}/collections"

    async with aiohttp.ClientSession() as session:
        return await session.post(url, json=payload, headers=kwargs['headers'])

@token_refresh_handler
@log_and_authorize
@HTTPStatusHandler(204)
async def delete_collection_func(
    kb_resource_id,
    collection_name,
    **kwargs
):
    url = f"{kwargs['base_url']}/knowledge-bases/{kb_resource_id}/collections"
    payload = {
        "name": collection_name
    }

    async with aiohttp.ClientSession() as session:
        return await session.delete(url, json=payload, headers=kwargs['headers'])

@token_refresh_handler
@log_and_authorize
@HTTPStatusHandler(200)
async def get_collection_func(
    kb_resource_id,
    **kwargs
):
    url = f"{kwargs['base_url']}/knowledge-bases/{kb_resource_id}/collections"

    async with aiohttp.ClientSession() as session:
        return await session.get(url, headers=kwargs['headers'])

@token_refresh_handler
@log_and_authorize
@HTTPStatusHandler(201)
async def ingest_data_func(
    kb_resource_id,
    ingestion_type,
    texts=None,
    data=None,
    ids=None,
    **kwargs
):
    if isinstance(ingestion_type, str):
        ingestion_type = [ingestion_type]
    if isinstance(texts, str):
        texts = [texts]
    if isinstance(data, str):
        data = [data]
    if isinstance(ids, str):
        ids = [ids]

    texts, data, ids = texts or [], data or [], ids or []
    combined = texts + data

    if (ids and not (len(ingestion_type) == len(ids) == len(combined))) or (not ids and len(ingestion_type) != len(combined)):
        error_message = f"The length of ingestion_type and {'texts + data and ids' if ids else 'texts + data'} must be equal."
        logger.error(error_message)
        raise ValueError(error_message)

    url = f"{kwargs['base_url']}/knowledge-bases/{kb_resource_id}"
    logger.info(f"Endpoint URL: {url}")

    form_data = aiohttp.FormData()
    files_to_close = []

    try:
        for x, y, z in zip(ingestion_type, combined, ids) if ids else zip(ingestion_type, combined):
            form_data.add_field('ingestion_type[]', x)
            if ids:
                form_data.add_field('ids[]', z)
            if y in texts:
                form_data.add_field('texts[]', y)
            elif y in data and os.path.isfile(y):
                file = open(y, 'rb')
                form_data.add_field('data', file, filename=os.path.basename(y))
                files_to_close.append(file)
            elif y in data:
                error_message = f"File not found or not a valid file: {y}"
                logger.error(error_message)
                raise ValueError(error_message)

        logger.info("Form data created successfully")

        async with aiohttp.ClientSession() as session:
            return await session.post(url, data=form_data, headers=kwargs['headers'])
    finally:
        for file in files_to_close:
            file.close()
            logger.info(f"Closed file: {file.name}")

@token_refresh_handler
@log_and_authorize
@HTTPStatusHandler([200, 202])
async def retrieve_data_func(
    kb_resource_id,
    queries,
    includes=[],
    options=[],
    threshold=0.7,
    limit=5,
    timeout=20,
    **kwargs
):
    if isinstance(queries, str):
        queries = [queries]

    params = {}

    for query in queries:
        if not query.strip():
            raise ValueError("Query cannot be an empty string.")
        params.setdefault("queries[]", []).append(query)

    for include in includes:
        if not include.strip():
            raise ValueError("Include cannot be an empty string.")
        params.setdefault("includes[]", []).append(include)

    for option in options:
        if not option.strip():
            raise ValueError("Option cannot be an empty string.")
        params.setdefault("options[]", []).append(option)

    params["threshold"] = threshold
    params["limit"] = limit
    params["timeout"] = timeout

    url = f"{kwargs['base_url']}/knowledge-bases/{kb_resource_id}"
    logger.info(f"Endpoint URL: {url}")

    logger.info("Query parameters:")
    for key, values in params.items():
        if isinstance(values, list):
            for value in values:
                logger.info(f"{key}: {value}")
        else:
            logger.info(f"{key}: {values}")

    async with aiohttp.ClientSession() as session:
        res = await session.get(url, headers=kwargs['headers'], params=params)

        if res.status != 401:
            result = await PollTaskStatusNamespace.poll_task_status_handler(
                res,
                status_url=f"http://192.168.1.27:5002/tasks/v1/status",
                task_id_key='task_id',
                headers=kwargs['headers']
            )
            return result
        return res