import logging
from multimodal_sdk.common.base import BaseMultiModalRag
from multimodal_sdk.knowledge_base.abstract_class import AbstractKnowledgeBaseHandler
from multimodal_sdk.knowledge_base.controller import (
    create_collection_func,
    delete_collection_func,
    get_collection_func,
    ingest_data_func,
    retrieve_data_func
)
from multimodal_sdk.role.main import _Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBase(BaseMultiModalRag, AbstractKnowledgeBaseHandler, _Role):
    def __init__(self, oauth_url=None, base_url=None, authz_url=None):
        super().__init__(base_url=base_url)
        self.oauth_url = oauth_url if oauth_url else self.oauth_url
        self.authz_url = authz_url if authz_url else self.authz_url

        _Role.__init__(self, knowledge_base=self)

    def _inject_params(func):
        async def wrapper(self, *args, **kwargs):
            access_token = kwargs.get('access_token')
            refresh_token = kwargs.get('refresh_token')
            if not access_token or not refresh_token:
                raise ValueError("access_token and refresh_token are required.")

            kwargs['oauth_url'] = self.oauth_url
            kwargs['base_url'] = self.base_url
            kwargs['authz_url'] = self.authz_url

            return await func(self, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def get_knowledge_base_id(response):
        knowledge_base_id = response.get("data", {}).get("knowledge_base", {}).get("id", "")
        if knowledge_base_id:
            return knowledge_base_id
        else:
            raise ValueError("Knowledge Base ID not found in the response.")

    @_inject_params
    async def create_collection(
        self,
        kb_resource_id,
        collection_name,
        ingestion_strategy,
        distance_method=None,
        main_lang=None,
        chunk_strategy=None,
        embedding_strategy=None,
        **kwargs
    ):
        result = await create_collection_func(
            kb_resource_id=kb_resource_id,
            collection_name=collection_name,
            ingestion_strategy=ingestion_strategy,
            distance_method=distance_method,
            main_lang=main_lang,
            chunk_strategy=chunk_strategy,
            embedding_strategy=embedding_strategy,
            **kwargs
        )

        logger.info("KnowledgeBase: create_collection response: %s", result)
        return result
    
    @_inject_params
    async def delete_collection(
        self,
        kb_resource_id,
        collection_name,
        **kwargs
    ):
        result = await delete_collection_func(
            kb_resource_id=kb_resource_id,
            collection_name=collection_name,
            **kwargs
        )

        logger.info("KnowledgeBase: delete_collection response: %s", result)
        return result
    
    @_inject_params
    async def get_collection(
        self,
        kb_resource_id,
        **kwargs
    ):
        result = await get_collection_func(
            kb_resource_id=kb_resource_id,
            **kwargs
        )

        logger.info("KnowledgeBase: get_collection response: %s", result)
        return result
    
    @_inject_params
    async def ingest_data(
        self,
        kb_resource_id,
        ingestion_type,
        texts=None,
        data=None,
        ids=None,
        **kwargs
    ):
        result = await ingest_data_func(
            kb_resource_id=kb_resource_id,
            ingestion_type=ingestion_type,
            texts=texts,
            data=data,
            ids=ids,
            **kwargs
        )

        logger.info("KnowledgeBase: ingest_data response: %s", result)
        return result

    @_inject_params
    async def retrieve_data(
        self,
        kb_resource_id,
        queries,
        includes=[],
        options=[],
        threshold=0.7,
        limit=5,
        timeout=20,
        **kwargs
    ):
        result = await retrieve_data_func(
            kb_resource_id=kb_resource_id,
            queries=queries,
            includes=includes,
            options=options,
            threshold=threshold,
            limit=limit,
            timeout=timeout,
            **kwargs
        )

        logger.info("KnowledgeBase: retrieve_data response: %s", result)
        return result