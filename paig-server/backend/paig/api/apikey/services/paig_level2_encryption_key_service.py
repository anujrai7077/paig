import logging
from core.controllers.base_controller import BaseController
from api.apikey.database.db_models.paig_level2_encryption_key_model import PaigLevel2EncryptionKeyModel
from api.apikey.services.paig_encryption_views import PaigLevel2EncryptionKeyView
from core.utils import SingletonDepends
from api.apikey.database.db_operations.paig_level2_encryption_key_repository import PaigLevel2EncryptionKeyRepository
from api.encryption.utils.secure_encryptor import SecureEncryptor
from api.encryption.factory.secure_encryptor_factory import SecureEncryptorFactory
from core.exceptions import NotFoundException
from api.apikey.utils import generate_hex_key, short_uuid, EncryptionKeyStatus
from core.db_session.transactional import Transactional, Propagation


logger = logging.getLogger(__name__)


class PaigLevel2EncryptionKeyService(BaseController[PaigLevel2EncryptionKeyModel, PaigLevel2EncryptionKeyView]):
    def __init__(
            self,
            paig_level2_encryption_key_repository: PaigLevel2EncryptionKeyRepository = SingletonDepends(PaigLevel2EncryptionKeyRepository),
            secure_encryptor_factory: SecureEncryptorFactory = SingletonDepends(SecureEncryptorFactory)
    ):
        super().__init__(
            paig_level2_encryption_key_repository,
            PaigLevel2EncryptionKeyModel,
            PaigLevel2EncryptionKeyView
        )
        self.secure_encryptor_factory = secure_encryptor_factory

    def get_repository(self) -> PaigLevel2EncryptionKeyRepository:
        """
        Retrieve the paig level2 encryption key repository.

        Returns:
            PaigLevel2EncryptionKeyRepository: The paig level2 encryption key repository.
        """
        return self.repository

    async def get_paig_level2_encryption_key_by_id(self, key_id: str):
        return await self.repository.get_paig_level2_encryption_key_by_id(key_id)

    async def get_paig_level2_encryption_key_by_uuid(self, key_uuid: str):
        return await self.repository.get_paig_level2_encryption_key_by_uuid(key_uuid)


    @Transactional(propagation=Propagation.REQUIRED)
    async def create_paig_level2_encryption_key(self):
        repository = self.get_repository()
        try:
            # Set existing active key to passive
            existing_paig_level2_encryption_key: PaigLevel2EncryptionKeyModel = await repository.get_active_paig_level2_encryption_key()

            existing_paig_level2_encryption_key_updated_request = PaigLevel2EncryptionKeyView.model_validate(
                existing_paig_level2_encryption_key)
            existing_paig_level2_encryption_key_updated_request.key_status = EncryptionKeyStatus.PASSIVE.value

            await self.update_record(existing_paig_level2_encryption_key.id,
                                     existing_paig_level2_encryption_key_updated_request)
        except NotFoundException:
            logger.debug(f"No active paig level2 key found")
        level2_key_value = generate_hex_key(22)
        level2_key_uuid = short_uuid()

        secure_encryptor: SecureEncryptor = await self.secure_encryptor_factory.get_or_create_secure_encryptor()
        encrypted_key = secure_encryptor.encrypt(level2_key_value)

        paig_level2_encryption_key_view: PaigLevel2EncryptionKeyView = PaigLevel2EncryptionKeyView()
        paig_level2_encryption_key_view.paig_key_value = encrypted_key
        paig_level2_encryption_key_view.key_status = EncryptionKeyStatus.ACTIVE.value
        paig_level2_encryption_key_view.key_id = level2_key_uuid

        result: PaigLevel2EncryptionKeyView = await self.create_record(paig_level2_encryption_key_view)

        response: PaigLevel2EncryptionKeyView = PaigLevel2EncryptionKeyView()
        response.id = result.id
        response.key_id = result.key_id
        response.status = result.status
        response.create_time = result.create_time
        response.update_time = result.update_time
        response.paig_key_value = result.paig_key_value
        response.key_status = result.key_status
        return response

    async def delete_paig_level2_encryption_key(self, key_id: str):
        return await self.repository.delete_by(filters={"id": key_id})

    async def get_active_paig_level2_encryption_key(self):
        try:
            return await self.repository.get_active_paig_level2_encryption_key()
        except NotFoundException:
            return None

    async def get_paig_level2_encryption_key_by_uuid(self, key_id: int):
        try:
            return await self.repository.get_paig_level2_encryption_key_by_uuid(key_id)
        except NotFoundException:
            return None

