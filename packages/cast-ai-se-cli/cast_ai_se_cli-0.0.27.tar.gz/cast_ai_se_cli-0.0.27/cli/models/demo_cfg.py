from cast_ai.se.contollers.cloud_controller import CloudController

from cli.models.config import ConfigObject


class DemoConfigObject:
    def __init__(self, cfg: ConfigObject, cloud_controller: CloudController):
        self.demo_count = int(cfg.app_config["GENERAL"]["DEMO_NODE_COUNT"])
        self.replicas = int(cfg.app_config["GENERAL"]["DEMO_REPLICAS"])
        ready_nodes = cloud_controller.get_node_count()
        match cfg.app_inputs["cloud"]:
            case "eks":
                self.scale_to = self.demo_count + ready_nodes
            case "gke":
                self.scale_to = self.demo_count + ready_nodes
            case "aks":
                # Either it`s from hibernation and then the expectancy is ready_nodes = 1 or 0
                # or Refresh then it might be higher then 1
                self.scale_to = self.demo_count + ready_nodes if ready_nodes > 1 else self.demo_count
