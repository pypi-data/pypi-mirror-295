import logging
import asyncio
from multimodal_sdk.common.base import BaseMultiModalRag
from multimodal_sdk.tenant.abstract_class import AbstractTenantHandler
from multimodal_sdk.tenant.controller import (
    create_tenant_func,
    delete_tenant_func,
    get_tenant_func,
    create_knowledge_base_func,
    delete_knowledge_base_func,
    get_knowledge_base_func
)
from multimodal_sdk.knowledge_base import KnowledgeBase
from multimodal_sdk.user_handler import UserHandler
from multimodal_sdk.role.main import _Role

import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Tenant(BaseMultiModalRag, AbstractTenantHandler, _Role):
    def __init__(self, oauth_url=None, base_url=None, authz_url=None):
        super().__init__(base_url=base_url)
        self.oauth_url = oauth_url if oauth_url else self.oauth_url
        self.authz_url = authz_url if authz_url else self.authz_url

        _Role.__init__(self, tenant=self)

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
    def get_tenant_id(response):
        tenant_id = response.get("data", {}).get("tenant", {}).get("id", "")
        if tenant_id:
            return tenant_id
        else:
            raise ValueError("Tenant ID not found in the response.")

    @_inject_params
    async def create_tenant(self, tenant_name: str, **kwargs):
        logger.info("Calling create_tenant with tenant_name: %s, kwargs: %s", tenant_name, kwargs)
        result = await create_tenant_func(
            tenant_name=tenant_name,
            **kwargs
        )

        logger.info("Tenant: create_tenant response: %s", result)
        return result

    @_inject_params
    async def delete_tenant(self, tenant_name: str, **kwargs):
        result = await delete_tenant_func(
            tenant_name=tenant_name,
            **kwargs
        )

        logger.info("Tenant: delete_tenant response: %s", result)
        return result

    @_inject_params
    async def get_tenant(self, **kwargs):
        result = await get_tenant_func(
            **kwargs
        )

        logger.info("Tenant: get_tenant response: %s", result)
        return result

    @_inject_params
    async def create_knowledge_base(self, tenant_resource_id: str, kb_name: str, **kwargs):
        result = await create_knowledge_base_func(
            tenant_resource_id=tenant_resource_id,
            kb_name=kb_name,
            **kwargs
        )

        logger.info("Tenant: create_knowledge_base response: %s", result)
        return result

    @_inject_params
    async def delete_knowledge_base(self, tenant_resource_id: str, kb_name: str, **kwargs):
        result = await delete_knowledge_base_func(
            tenant_resource_id=tenant_resource_id,
            kb_name=kb_name,
            **kwargs
        )

        logger.info("Tenant: delete_knowledge_base response: %s", result)
        return result

    @_inject_params
    async def get_knowledge_base(self, tenant_resource_id: str, **kwargs):
        result = await get_knowledge_base_func(
            tenant_resource_id=tenant_resource_id,
            **kwargs
        )

        logger.info("Tenant: get_knowledge_base response: %s", result)
        return result

async def main():
    logger.info("Testing Tenant class")
    logger.info("Creating Tenant object")

    t = Tenant()
    kb = KnowledgeBase()

    # Users : toyo_test_user_123, toyo_test_user_321, toyo_test_user_456

    # User Handler
    user_handler = UserHandler()

    login_user = await user_handler.login(
        username="toyo_test_user_123",
        password="Tokyo@6377300390"
    )
    logger.info("login_user final response (toyo_test_user_123): %s", login_user)

    access_token_123 = UserHandler.get_access_token(login_user)
    refresh_token_123 = UserHandler.get_refresh_token(login_user)

    login_user = await user_handler.login(
        username="toyo_test_user_321",
        password="Tokyo@6377300390"
    )
    logger.info("login_user final response (toyo_test_user_321): %s", login_user)

    access_token_321 = UserHandler.get_access_token(login_user)
    refresh_token_321 = UserHandler.get_refresh_token(login_user)

    login_user = await user_handler.login(
        username="toyo_test_user_456",
        password="Tokyo@6377300390"
    )
    logger.info("login_user final response (toyo_test_user_456): %s", login_user)

    access_token_456 = UserHandler.get_access_token(login_user)
    refresh_token_456 = UserHandler.get_refresh_token(login_user)

    time.sleep(2)

    tenant_name = "toyo_test_tenant_123"
    kb_name = "toyo_test_kb_123"
    collection_name = "toyo_test_collection_123"

    logger.info("Calling create_tenant")
    res1 = await t.create_tenant(
        tenant_name=tenant_name,
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("create_tenant final response: %s", res1)
    time.sleep(2)

    tenant_id = Tenant.get_tenant_id(res1)
    # tenant_id = "0798e14f-8892-4cfe-abe7-15a750a66f08"
    logger.info("Tenant ID: %s", tenant_id)

    # logger.info("Calling get_tenant")
    # res2 = await t.get_tenant(
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("get_tenant final response: %s", res2)

    # time.sleep(2)

    logger.info("Calling create_knowledge_base")
    res3 = await t.create_knowledge_base(
        tenant_resource_id=tenant_id,
        kb_name=kb_name,
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("create_knowledge_base final response: %s", res3)
    time.sleep(2)

    kb_id = KnowledgeBase.get_knowledge_base_id(res3)
    kb_id = "00dd3b4a-7eaf-4a4d-a9d5-d4ae1e6af9be"
    logger.info("Knowledge Base ID: %s", kb_id)

    # logger.info("Calling get_knowledge_base")
    # res4 = await t.get_knowledge_base(
    #     tenant_resource_id=tenant_id,
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("get_knowledge_base final response: %s", res4)

    # time.sleep(2)

    logger.info("Calling create_collection")
    res7 = await kb.create_collection(
        kb_resource_id=kb_id,
        collection_name=collection_name,
        ingestion_strategy=["text"],
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("create_collection final response: %s", res7)
    time.sleep(2)

    # logger.info("Calling get_collection")
    # res9 = await kb.get_collection(
    #     kb_resource_id=kb_id,
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("get_collection final response: %s", res9)

    # time.sleep(2)

    # logger.info("Calling ingest_data")
    # res10 = await kb.ingest_data(
    #     kb_resource_id=kb_id,
    #     ingestion_type=["text"],
    #     texts=["The solar system consists of the Sun and the objects that orbit it, including eight planets, their moons, and smaller objects such as asteroids and comets. The Sun is the largest object in the solar system, containing 99.8 percent of its total mass. The planets, in order of their distance from the Sun, are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. The solar system also contains dwarf planets like Pluto, which orbit the Sun but are not classified as full-fledged planets. Each planet has unique characteristics, such as Earth's ability to support life, Jupiter's massive size, and Saturn's distinctive rings."],
    #     ids=["ruskwis82skxmaiq8woskzmwwqk"],
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("ingest_data final response: %s", res10)

    # time.sleep(5)

    # logger.info("Calling ingest_data")
    # res10 = await kb.ingest_data(
    #     kb_resource_id=kb_id,
    #     ingestion_type=["text"],
    #     texts=["(aurelien.vialon sent message on 20/06/2023 at 5:01 PM) - End of day. \n As tomorrow I am taking an holiday, I will put my progresses since yesterday \n Refinement on the auth API \n Creating of user model (to be used for permission) \n Fixing some bugs \n Searching how to implement the permission system (authz) I will do it from Monday \n Have a nice weekend !"],
    #     ids=["ruskwis82skxmaiqksimsoskzmwwqk"],
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("ingest_data final response: %s", res10)

    # time.sleep(5)

    logger.info("Calling delete_role")
    res11 = await t.delete_role(
        role_id=10,
        resource_id=kb_id,
        user_id="d77f6e4b-36e4-4c15-9f7f-7765861be4a0",
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("delete_role final response: %s", res11)

    logger.info("Calling assign_role")
    res12 = await t.assign_role(
        role_id=10,
        resource_id=kb_id,
        user_id="d77f6e4b-36e4-4c15-9f7f-7765861be4a0",
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("assign_role final response: %s", res12)

    logger.info("Calling assign_role kb")
    res12 = await kb.assign_role(
        role_id=10,
        resource_id=kb_id,
        user_id="e6864053-0eff-429f-af78-c48d95f4c7f9",
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("assign_role final response (kb): %s", res12)

    logger.info("Calling fetch_all_roles")
    res13 = await t.fetch_all_roles(
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("fetch_all_roles final response: %s", res13)

    logger.info("Calling fetch_user_roles")
    res14 = await t.fetch_user_roles(
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("fetch_user_roles final response: %s", res14)

    logger.info("Calling fetch_resource_roles")
    res15 = await t.fetch_resource_roles(
        resource_id=kb_id,
        access_token=access_token_123,
        refresh_token=refresh_token_123
    )
    logger.info("fetch_resource_roles final response: %s", res15)


    # logger.info("Calling retrieve_data")
    # res11 = await kb.retrieve_data(
    #     kb_resource_id=kb_id,
    #     queries=["Which planet in the solar system has distinctive rings?", "What process do plants use to convert sunlight into chemical energy?"],
    #     includes=["metadatas", "documents"], # "embeddings"
    #     options=["multi-languages", "rag", "async", "fusion"],
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("retrieve_data final response: %s", res11)

    # time.sleep(5)

    # logger.info("Calling retrieve_data")
    # res11 = await kb.retrieve_data(
    #     kb_resource_id=kb_id,
    #     queries=["When did Aurelien take leave?"],
    #     includes=["metadatas", "documents"], # "embeddings"
    #     options=["multi-languages", "rag", "sync"],
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("retrieve_data final response: %s", res11)

    # time.sleep(5)

    # logger.info("Calling delete_collection")
    # res8 = await kb.delete_collection(
    #     kb_resource_id=kb_id,
    #     collection_name=collection_name,
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("delete_collection final response: %s", res8)

    # logger.info("Calling delete_knowledge_base")
    # res5 = await t.delete_knowledge_base(
    #     tenant_resource_id=tenant_id,
    #     kb_name=kb_name,
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("delete_knowledge_base final response: %s", res5)

    # logger.info("Calling delete_tenant")
    # res6 = await t.delete_tenant(
    #     tenant_name=tenant_name,
    #     access_token=access_token,
    #     refresh_token=refresh_token
    # )
    # logger.info("delete_tenant final response: %s", res6)



if __name__ == "__main__":
    asyncio.run(main())
