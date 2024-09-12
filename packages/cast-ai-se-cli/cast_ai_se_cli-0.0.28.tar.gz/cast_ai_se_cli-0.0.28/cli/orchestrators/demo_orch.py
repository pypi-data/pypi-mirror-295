import logging
import time

from cast_ai.se.contollers.kubectl_controller import KubectlController
from cast_ai.se.contollers.castai_controller import CastController
from cast_ai.se.contollers.eks_controller import EKSController
from cast_ai.se.contollers.aks_controller import AKSController
from cast_ai.se.contollers.gke_controller import GKEController

from cast_ai.se.models.execution_status import ExecutionStatus
from cast_ai.se.models.cloud_confs import AksConfig, EksConfig, GkeConfig

from cli.orchestrators.base_orch import BaseOrchestrator
from cli.services.validators import validate_kubectl_context
from cli.models.config import ConfigObject
from cli.models.demo_cfg import DemoConfigObject


class DemoOrchestrator(BaseOrchestrator):
    def __init__(self, cfg: ConfigObject):
        super().__init__(cfg)
        self._logger = logging.getLogger(__name__)

        self._cast_ctrl = CastController(cfg.app_config["CAST"]["CASTAI_API_TOKEN"], cfg.cid)
        self._kubectl_ctrl = KubectlController(cfg.context)

        self._initial_nodes = self._cast_ctrl.get_nodes()

        self._cloud_ctrl = None
        self._set_cloud_controller()
        self.demo_subcommand_mapping = {
            "prep": self.demo_prep_sequence,
            "off": self.demo_off_sequence,
        }
        validate_kubectl_context(self._kubectl_ctrl, self._cast_ctrl.cluster['providerType'])

    def execute(self) -> None:
        subcommand = self._cfg.app_inputs["demo_subcommand"]
        if subcommand in self.demo_subcommand_mapping:
            self.demo_subcommand_mapping[subcommand]()
        else:
            raise ValueError(f'Invalid option: {subcommand}')

    def demo_prep_sequence(self):
        start_time = time.time()
        demo_cfg = DemoConfigObject(self._cfg, self._cloud_ctrl)
        self._logger.info(f"{'=' * 80}< Starting demo-PREP sequence >{'=' * 80}")
        initial_nodes = self._cast_ctrl.get_nodes()

        if not self._cast_ctrl.is_downscaler_disabled():
            self.spinner_run("Disabling downscaler policy", lambda: self._cast_ctrl.disable_downscaler_policy())

        self.spinner_run(f"Scaling cloud nodes to {demo_cfg.scale_to}",
                         lambda: self._cloud_ctrl.scale(demo_cfg.scale_to))

        all_demo_nodes_up = self.spinner_run("Waiting for new nodes to be ready",
                                             lambda: self._wait_for_new_nodes(len(initial_nodes["items"]),
                                                                              demo_cfg.demo_count))

        self.spinner_run("Reconciling Cluster", lambda: self._cast_ctrl.reconcile())

        self.spinner_run(f"Scaling all deployments to {demo_cfg.replicas} replicas",
                         lambda: self._kubectl_ctrl.scale_deployments(demo_cfg.replicas))
        if all_demo_nodes_up.success:
            self.spinner_run(f'Deleting initial {len(initial_nodes["items"])} fallback nodes ',
                             lambda: self._cast_ctrl.delete_nodes(initial_nodes))
        else:
            print("❗❕ You may want to delete the nodes from previous state (e.g. Fallback nodes)...")

        print(f"It took {int(time.time() - start_time)} seconds to prep demo")

    def demo_off_sequence(self):
        demo_off_cronjob = self._cfg.app_config["KUBECTL"]["DEMO_OFF_CRONJOB"]
        self._logger.info(f"{'=' * 80}< Starting demo-OFF sequence >{'=' * 80} ")

        msg = "Scaling all deployments in default namespace to 0"
        self.spinner_run(msg, lambda: self._kubectl_ctrl.scale_deployments(0))

        self.spinner_run("Disabling CAST Unscheduled pods policy",
                         lambda: self._cast_ctrl.disable_unscheduled_pods_policy())

        msg = f"Manually triggering {demo_off_cronjob}"
        cronjob_triggered = (
            self.spinner_run(msg, lambda: self._kubectl_ctrl.trigger_cronjob(demo_off_cronjob)))

        if cronjob_triggered.success:
            self.spinner_run("Turning off autoscaling cloud", lambda: self._cloud_ctrl.disable_autoscaler())
        else:
            print("❗❕ You may want to turn off autoscaling manually...")

    def _wait_for_new_nodes(self, initial_node_count: int, demo_count: int) -> ExecutionStatus:
        try:
            self._logger.info(f"{'-' * 70}[ Waiting for new nodes to be ready ]")
            scaling_timeout = self._cfg.app_config["GENERAL"]["SCALING_TIMEOUT"]
            start_time = time.time()
            while True:
                nodes = self._cast_ctrl.get_nodes()
                self._logger.debug(f"Current:{len(nodes['items'])} "
                                   f"Initial:{initial_node_count} "
                                   f"Requested:{demo_count}")
                if len(nodes["items"]) == initial_node_count + demo_count:
                    all_nodes_ready = all(node["state"]["phase"] == "ready" for node in nodes["items"])
                    if all_nodes_ready:
                        self._logger.info(f"Waited {time.time() - start_time} for all new nodes to be ready...")
                        return ExecutionStatus()
                    else:
                        node_states = [node["state"]["phase"] for node in nodes["items"]]
                        node_states_str = ", ".join(node_states)
                        self._logger.debug(f"Node states: ({node_states_str})")
                if time.time() - start_time > int(scaling_timeout):
                    self._logger.warning(f"Timeout ({scaling_timeout}sec) reached while waiting for new nodes")
                    return ExecutionStatus(f"Timeout ({scaling_timeout}sec)")
                time.sleep(1)
        except Exception as e:
            self._logger.error(f"Something went wrong:[{str(e)}]")
            return ExecutionStatus(f"Something went wrong:[{str(e)}]")

    def _set_cloud_controller(self):
        match (self._cast_ctrl.cluster['providerType']):
            case "eks":
                self._cloud_ctrl = EKSController(EksConfig(self._cfg.app_config["EKS"]))
                self._logger.info("Orchestrator is using EKS as Cloud Controller")
            case "aks":
                self._cloud_ctrl = AKSController(AksConfig(self._cfg.app_config["AKS"]))
                self._logger.info("Orchestrator is using AKS as Cloud Controller")
            case "gke":
                self._cloud_ctrl = GKEController(GkeConfig(self._cfg.app_config["GKE"]))
                self._logger.info("Orchestrator is using GKE as Cloud Controller")
            case _:
                self._logger.error(f"Unsupported cloud {self._cast_ctrl.cluster['providerType']}")
                raise ValueError(f"{self._cast_ctrl.cluster['providerType']}")
