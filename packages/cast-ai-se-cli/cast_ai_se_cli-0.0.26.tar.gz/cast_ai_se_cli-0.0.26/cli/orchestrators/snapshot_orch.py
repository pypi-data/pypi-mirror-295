from cast_ai.se.contollers.snapshot_controller import SnapshotController
from cast_ai.se.models.misc_data_models import ReportDetailLevel
from cast_ai.se.services.snapshot_analysis_svc import SnapshotAnalyzer

from cli.models.config import ConfigObject
from cli.orchestrators.base_orch import BaseOrchestrator


class SnapshotOrchestrator(BaseOrchestrator):
    def __init__(self, cfg: ConfigObject):
        super().__init__(cfg)
        self._snapshot_ctrl = SnapshotController(cast_api_key=cfg.app_config["CAST"]["CASTAI_API_TOKEN"],
                                                 default_cluster_id=cfg.cid,
                                                 json_key_path=cfg.app_config["GKE"]["JSON_KEY_PATH"])
        self._snapshot_analyzer = SnapshotAnalyzer(self._snapshot_ctrl.raw_snapshot)
        self._snapshot_subcommand_mapping = {
            "brief": self.generate_brief_report,
            "detailed": self.generate_detailed_report,
            "extra": self.generate_extra_detailed_report,
            "csv": self.generate_csv_detailed_report,
        }

    def execute(self) -> None:
        subcommand = self._cfg.app_inputs["snapshot_subcommand"]
        if subcommand in self._snapshot_subcommand_mapping:
            self._snapshot_subcommand_mapping[subcommand]()
        else:
            raise ValueError(f'Invalid option: {subcommand}')

    def generate_brief_report(self):
        print(self._snapshot_analyzer.get_refined_snapshot_report(detail_lvl=ReportDetailLevel.BASIC))

    def generate_detailed_report(self):
        print(self._snapshot_analyzer.get_refined_snapshot_report(detail_lvl=ReportDetailLevel.DETAILED))

    def generate_extra_detailed_report(self):
        print(self._snapshot_analyzer.get_refined_snapshot_report(detail_lvl=ReportDetailLevel.EXTRA))

    def generate_csv_detailed_report(self):
        self._snapshot_analyzer.get_refined_snapshot_csv_report()
