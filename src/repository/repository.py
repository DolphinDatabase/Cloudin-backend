from utils.scheduler import scheduler


class Repository:

    DOWNLOAD_FOLDER_PATH:str

    def __init__(self, token: str, verification_interval: int = 10):
        self.verification_interval = verification_interval
        self.token = token

    def list(self) -> list:
        pass

    def upload(self, file: any, origin: any) -> None:
        pass

    def download(self, file: any) -> str:
        pass

    def start_verification(self) -> None:
        scheduler.add_job(self.list, "interval", self.verification_interval)
