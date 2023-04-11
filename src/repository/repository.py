from utils.scheduler import scheduler
from model.config import Config

class Repository:
    verification_interval: int = 10
    configuration: Config
    files: list = []

    def list(self) -> list:
        pass

    def upload(self, file: str) -> None:
        pass

    def download(self, file: str) -> None:
        pass

    def start_verification(self) -> None:
        scheduler.add_job(self.list, 'interval', self.verification_interval)
