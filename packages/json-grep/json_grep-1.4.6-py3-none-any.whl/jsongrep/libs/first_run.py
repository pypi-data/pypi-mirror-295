import os
from platformdirs import user_data_dir

class _NotFirstRun(Exception):
    pass

class FirstRun:
    def __init__(self, app_name: str, version: str = ""):
        self.app_name = app_name
        self.version = version
        self._user_data_path: str = os.path.join(user_data_dir(appname=self.app_name), "first_run.txt")

    def __enter__(self):
        if not self._is_first_run():
            raise _NotFirstRun()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == _NotFirstRun:
            print("This is not first run")
            

    def _is_first_run(self) -> bool:
        return False