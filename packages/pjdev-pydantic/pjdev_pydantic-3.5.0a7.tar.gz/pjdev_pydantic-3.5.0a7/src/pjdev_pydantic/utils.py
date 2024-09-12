from pathlib import Path
from typing import (
    Type,
    TypeVar,
    Tuple,
    Any,
    Dict
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource
)
from pydantic.fields import FieldInfo
from keeper_secrets_manager_core import SecretsManager
from keeper_secrets_manager_core.storage import FileKeyValueStorage
from loguru import logger

from pjdev_pydantic.models import KeeperSettings

T = TypeVar('T', bound=BaseSettings)


def get_keeper_settings(root: Path) -> KeeperSettings:
    return KeeperSettings(_env_file=root / ".env", root_dir=root)


def get_secrets_manager(settings: KeeperSettings) -> SecretsManager:
    secrets_manager = SecretsManager(
            token=settings.token, config=FileKeyValueStorage(settings.root_dir / ".ksm-config.json")
    )

    return secrets_manager

def keeper_settings_source_class_factory(secrets_manager: SecretsManager, keeper_secret_title: str) -> Type[
    PydanticBaseSettingsSource]:

    secret = secrets_manager.get_secret_by_title(keeper_secret_title)

    class KeeperConfigSettingsSource(PydanticBaseSettingsSource):

        def get_field_value(
                self, field: FieldInfo, field_name: str
        ) -> Tuple[Any, str, bool]:
            if not secret:
                return None, field_name, False
            key = field.alias if field.alias else field_name
            try:
                secret_value = secret.field(key, single=True)
            except ValueError as e:
                logger.warning(e)
                secret_value = secret.custom_field(key, single=True)
            return secret_value, field_name, False

        def prepare_field_value(
                self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
        ) -> Any:
            return value

        def __call__(self) -> Dict[str, Any]:
            d: Dict[str, Any] = {}

            for field_name, field in self.settings_cls.model_fields.items():
                field_value, field_key, value_is_complex = self.get_field_value(
                        field, field_name
                )
                field_value = self.prepare_field_value(
                        field_name, field, field_value, value_is_complex
                )
                if field_value is not None:
                    d[field_key] = field_value

            return d

    return KeeperConfigSettingsSource


def keeper_settings_class_factory(class_type: Type[T], secrets_manager: SecretsManager, keeper_secret_title: str) -> Type[T]:
    class KeeperSecretsClass(class_type):
        model_config = SettingsConfigDict(
                populate_by_name=True
        )

        @classmethod
        def settings_customise_sources(
                cls,
                settings_cls: Type[class_type],
                init_settings: PydanticBaseSettingsSource,
                env_settings: PydanticBaseSettingsSource,
                dotenv_settings: PydanticBaseSettingsSource,
                file_secret_settings: PydanticBaseSettingsSource,
        ) -> Tuple[PydanticBaseSettingsSource, ...]:
            return (
                    keeper_settings_source_class_factory(
                            secrets_manager=secrets_manager, keeper_secret_title=keeper_secret_title
                    )(settings_cls),
            )

    return KeeperSecretsClass
