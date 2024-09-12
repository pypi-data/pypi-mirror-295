import logging

from cli.models.config import ConfigObject
from cli.services.version_svc import get_current_version


class GeneralResponder:
    def __init__(self, cfg: ConfigObject):
        self._logger = logging.getLogger(__name__)
        self._cfg = cfg
        self._commands_mapping = {
            "version": self._print_current_version,
        }

    def execute(self) -> None:
        if self._cfg.app_inputs["command"] in self._commands_mapping:
            self._commands_mapping[self._cfg.app_inputs["command"]]()
        else:
            raise ValueError(f'Invalid option: {self._cfg.app_config["command"]}')

    @staticmethod
    def _print_current_version():
        version = get_current_version()
        if version:
            print(f"CAST.AI-SE-CLI version = {get_current_version()}")
        else:
            print("There was an issue figuring out the version of this amazing CLI tool")
