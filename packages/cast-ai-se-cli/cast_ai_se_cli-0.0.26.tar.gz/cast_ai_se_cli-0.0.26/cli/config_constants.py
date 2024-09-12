CONFIG_TEMPLATE = {
    "CAST": {
        "CASTAI_API_TOKEN": "",
        "DEFAULT_CLUSTER_ID": ""
    },
    "EKS": {
        "K8S_CONTEXT": "",
        "CLUSTER_ID": "",
        "REGION": "",
        "NODE_GROUP": "",
        "CLUSTER_NAME": "",
        "AUTOSCALING_GROUP": "",
        "ACCESS_KEY": "",
        "ACCESS_SECRET_KEY": ""
    },
    "AKS": {
        "K8S_CONTEXT": "",
        "CLUSTER_ID": "",
        "CLIENT_ID": "",
        "CLIENT_SECRET": "",
        "TENANT_ID": "",
        "NODE_POOL": "",
        "SUBSCRIPTION_ID": "",
        "CLUSTER_NAME": "",
        "RESOURCE_GROUP": ""
    },
    "GKE": {
        "K8S_CONTEXT": "",
        "CLUSTER_ID": "",
        "PROJECT_ID": "",
        "ZONE": "us-east1-b",
        "CLUSTER_NAME": "",
        "NODE_POOL": "",
        "JSON_KEY_PATH": ""
    },
    "GENERAL": {
        "DEMO_NODE_COUNT": 7,
        "DEMO_REPLICAS": 2,
        "SCALING_TIMEOUT": 180

    },
    "KUBECTL": {
        "DEMO_OFF_CRONJOB": "hibernate-pause"
    },
}

CLI_INPUTS_TEMPLATE = {
    "demo": False,
    "demo_subcommand": "",
    "snapshot": False,
    "snapshot_subcommand": "",
    "audit": False,
    "audit_subcommand": "",
    "cluster_id": "",
    "help": False,
    "debug": False
}
