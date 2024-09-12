import logging
import os
import json
from datetime import datetime

from docopt import ParsedOptions

from cli.config_constants import CONFIG_TEMPLATE, CLI_INPUTS_TEMPLATE
from cli.constants import CONFIG_PATH, SUPPORTED_COMMANDS
from cli.services.validators import is_config_file_valid, is_cluster_id


class ConfigObject:
    def __init__(self, parsed_inputs: ParsedOptions, config_file_path=CONFIG_PATH):
        self.config_file_path = config_file_path
        self._logger = logging.getLogger(__name__)
        self.app_config = None

        self.app_inputs = CLI_INPUTS_TEMPLATE
        self.cid = None
        self.context = None
        self._populate_parsed_inputs_data(parsed_inputs)
        self._setup_config()
        self._set_cid()

    def create_empty_template(self):
        self._logger.info(f"Creating empty {CONFIG_PATH} file")
        with open(self.config_file_path, "w") as config_file:
            json.dump(CONFIG_TEMPLATE, config_file)

    def _populate_parsed_inputs_data(self, parsed_inputs: ParsedOptions):
        self.app_inputs["demo"] = parsed_inputs["demo"]
        self.app_inputs["version"] = parsed_inputs["version"]
        self.app_inputs["demo_subcommand"] = parsed_inputs["<prep | off>"]
        self.app_inputs["snapshot"] = parsed_inputs["snapshot"]
        self.app_inputs["snapshot_subcommand"] = parsed_inputs["<basic | detailed | extra | csv>"]
        self.app_inputs["cloud"] = parsed_inputs["<eks | aks | gcp>"]
        self.app_inputs["audit"] = parsed_inputs["audit"]
        self.app_inputs["audit_subcommand"] = parsed_inputs["<analyze>"]
        self.app_inputs["cluster_id"] = parsed_inputs["--cluster_id"]
        self.app_inputs["no_cfg"] = parsed_inputs["--no_cfg"]
        self.app_inputs["debug"] = parsed_inputs["--debug"]

        for command, value in parsed_inputs.items():
            if command in SUPPORTED_COMMANDS and value:
                self.app_inputs["command"] = command

    def _set_cid(self):
        cloud = self.app_inputs["cloud"]
        if cloud:
            self._logger.info(f"Cluster id={self.app_config[cloud.upper()]['CLUSTER_ID']} will be used")
            self.cid = self.app_config[cloud.upper()]['CLUSTER_ID']
            self.context = self.app_config[cloud.upper()]['K8S_CONTEXT']
            return

        elif self.app_inputs["cluster_id"]:
            if is_cluster_id(self.app_inputs["cluster_id"]):
                self._logger.info(f"Custom cluster id={self.app_inputs['cluster_id']} will be used")
                self.cid = self.app_inputs["cluster_id"]
                return
            else:
                raise RuntimeError("--cluster_id did not match expected format")
        self.cid = self.app_config['CAST']['DEFAULT_CLUSTER_ID']

    def _setup_config(self):
        if self.app_inputs["no_cfg"]:
            if not self.app_inputs["cluster_id"]:
                raise RuntimeError("No cluster_id specified and -n flag was set (No value for cluster_id).")
            self.app_config = CONFIG_TEMPLATE
            return
        if not os.path.exists(self.config_file_path):
            self.create_empty_template()
            self._logger.critical("config.json was missing. Created an empty template.")
            raise RuntimeError("config.json was missing. Created an empty template.")
        with open(self.config_file_path, "r") as config_file:
            configuration_data = json.load(config_file)
        if not is_config_file_valid(configuration_data):
            self._handle_invalid_config_file()
        self.app_config = configuration_data

    def _handle_invalid_config_file(self):
        timestamp = datetime.now().strftime("%m_%d_%H_%M")
        backup_file_path = f"{self.config_file_path}.{timestamp}.json"
        os.rename(self.config_file_path, backup_file_path)
        self._logger.info(f"Config file was renamed to {backup_file_path} and up2date config created")
        self.create_empty_template()
        self._logger.critical("Invalid configuration file structure/version")
        raise RuntimeError("Invalid configuration file structure")
