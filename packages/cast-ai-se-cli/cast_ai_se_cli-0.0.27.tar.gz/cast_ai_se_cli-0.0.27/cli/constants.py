PACKAGE_NAME = "cast-ai-se-cli"

DEMO_OFF_CRONJOB = "hibernate-pause"
# DEMO_ON_CRONJOB = "hibernate-resume"

# DEBUG LOGS
LOG_DIR = "logs"
LOG_FILE = "all_logs.log"

CONFIG_PATH = "config.json"
SUPPORTED_COMMANDS = ["demo", "snapshot", "audit", "version"]

EPHEMERAL_NODE_STATUSES = ["deleted", "deleting", "draining", "cordoned"]
SUPPORTED_K8S = ['EKS', 'AKS', 'GKE']
