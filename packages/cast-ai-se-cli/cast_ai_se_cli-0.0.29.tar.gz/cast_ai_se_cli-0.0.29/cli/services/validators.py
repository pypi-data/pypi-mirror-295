import logging
import re

from cast_ai.se.contollers.kubectl_controller import KubectlController

from cli.config_constants import CONFIG_TEMPLATE

logger = logging.getLogger(__name__)


def is_config_file_valid(config: dict, original_config=CONFIG_TEMPLATE) -> bool:
    keys1 = set(config.keys())
    keys2 = set(original_config.keys())

    if keys1 != keys2:
        logger.error(f"Found mismatch in configuration file keys: {keys1}!={keys2}")
        return False

    for key in keys1:
        value1 = config[key]
        value2 = original_config[key]
        is_dict1 = isinstance(value1, dict)
        is_dict2 = isinstance(value2, dict)

        if is_dict1 != is_dict2:
            logger.error(f"Found mismatch in configuration file: {value1}!={value2}")
            return False

        if is_dict1 and is_dict2:
            if not is_config_file_valid(value1, value2):
                return False
    return True


def is_cluster_id(cluster_id: str) -> bool:
    regex = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    match = re.search(regex, cluster_id)
    logger.debug(f"is {cluster_id} a match for cluster_id format ? => {str(match)}")
    return bool(match)


def validate_kubectl_context(kube_ctrl: KubectlController, cloud: str) -> None:
    identified_cloud_context = kube_ctrl.get_context_cloud_type()
    if not identified_cloud_context == cloud:
        logger.warning(f"Kubectl context({identified_cloud_context}) doesn't match the one on CAST ({cloud})")
