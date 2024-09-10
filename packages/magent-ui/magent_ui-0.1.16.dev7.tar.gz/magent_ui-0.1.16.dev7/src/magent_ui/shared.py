# shared
from multiprocessing import Manager
from .service import au_service, AUService
from .config import AppConfig, app_config


class SharedManager:
    def __init__(self):
        self.manager = Manager()
        self.shared = self.manager.dict()
        self.shared['au_service'] = au_service
        self.shared['app_config'] = app_config

    def get_shared(self):
        return self.shared

    def get_config(self) -> AppConfig:
        return self.shared.get('app_config', None)

    def get_service(self) -> AUService:
        return self.shared.get('au_service', None)

    def cleanup(self):
        self.shared.clear()
        self.manager.shutdown()
