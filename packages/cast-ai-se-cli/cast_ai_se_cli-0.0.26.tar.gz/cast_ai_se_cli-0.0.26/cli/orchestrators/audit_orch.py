import logging
import time
from datetime import datetime
from typing import Dict

from cli.models.config import ConfigObject
from cli.orchestrators.base_orch import BaseOrchestrator

from cast_ai.se.contollers.castai_controller import CastController


class AuditOrchestrator(BaseOrchestrator):
    def __init__(self, cfg: ConfigObject):
        super().__init__(cfg)
        self._logger = logging.getLogger(__name__)

        self._cast_ctrl = CastController(cfg.app_config["CAST"]["CASTAI_API_TOKEN"], cfg.cid)

        self.audit_subcommand_mapping = {
            "analyze": self.audit_analyze_sequence,
        }

    def execute(self) -> None:
        subcommand = self._cfg.app_inputs["audit_subcommand"]
        if subcommand in self.audit_subcommand_mapping:
            self.audit_subcommand_mapping[subcommand]()
        else:
            raise ValueError(f'Invalid option: {subcommand}')

    def audit_analyze_sequence(self):
        start_time = time.time()
        try:
            audit_logs = self._cast_ctrl.get_audit()
            error_log_items = list(filter(lambda log_item: "error" in log_item.get("event", {}), audit_logs["items"]))
            if error_log_items:
                print(f"\n{'=' * 20}< Found {len(error_log_items)} log items with errors "
                      f"in {len(audit_logs['items'])} total log items >{'=' * 20}")
                for log_item in error_log_items:
                    event_id, event_time, event_type = self.extract_log_item_essentials(log_item)
                    error_details = log_item["event"]["error"]["details"]

                    print(f"| {event_time} | {event_id} | {event_type} | {error_details} |")
            else:
                print(f"{'=' * 20}< No errors found in log items >{'=' * 20}")

            interr_prediction_events = list(filter(lambda log_item: "interruptionPredictionNodesToRebalance" in
                                                                    log_item.get("eventType", {}), audit_logs["items"]))
            if interr_prediction_events:
                print(f"\n{'=' * 20}< Found {len(interr_prediction_events)} interruptions "
                      f"in {len(audit_logs['items'])} total log items >{'=' * 20}")
                for log_item in interr_prediction_events:
                    self.analyze_interruption(audit_logs, log_item)

            node_delete_events = list(filter(lambda log_item: "nodeDeleted" in
                                                              log_item.get("eventType", {}), audit_logs["items"]))
            if node_delete_events:
                print(f"\n{'=' * 20}< Found {len(node_delete_events)} node deletions "
                      f"in {len(audit_logs['items'])} total log items >{'=' * 20}")
                for log_item in node_delete_events:
                    event_id, event_time, event_type = self.extract_log_item_essentials(log_item)
                    node_instance = log_item["event"]["node"]["instanceId"]
                    instance_type = log_item["event"]["node"]["instanceType"]
                    is_spot = log_item["event"]["node"]["spot"]
                    node_type = "On-Demand"
                    if is_spot:
                        node_type = "Spot"

                    print(f"| {event_time} | {event_id} | {event_type} | {node_instance} | {instance_type} | {node_type} |")

        except Exception as e:
            self._logger.error(f"Something went wrong:[{str(e)}]")
        print(f"It took {int(time.time() - start_time)} seconds to analyze")

    def analyze_interruption(self, audit_logs, log_item):
        event_id, event_time, event_type = self.extract_log_item_essentials(log_item)
        instance_type = log_item["event"]["instance_type"]
        nodes = log_item["event"]["node_ids"]
        print(f"{event_type} for {instance_type} at {event_time}")
        for node in nodes:
            node_events = list(filter(lambda log_item: node in log_item.get(
                "event", {}).get("node", {}).get("id", {}), audit_logs["items"]))
            storted_node_events = sorted(node_events, key=lambda x: x['time'])
            print(f"\n{'=' * 10}< {node} events found for  >{'=' * 10}")
            time_of_last_event = None
            for event in storted_node_events:
                time_between_events = None
                node_event_time = datetime.strptime(event["time"], '%Y-%m-%dT%H:%M:%S.%fZ')
                if time_of_last_event is not None:
                    time_between_events = node_event_time - time_of_last_event
                node_event_type = event["eventType"]
                node_event_id = event["id"]
                time_between_events_str = "N/A"
                if time_between_events is not None:
                    total_seconds = time_between_events.total_seconds()
                    total_minutes = total_seconds / 60
                    time_between_events_str = (f"The total seconds since the last event was "
                                               f"{str(total_seconds)} ({str(total_minutes)} minutes)")

                print(f"| {node_event_time} | {node_event_id} | {node_event_type} | "
                      f"{time_between_events_str}")
                time_of_last_event = node_event_time

    @staticmethod
    def extract_log_item_essentials(log_item: Dict) -> tuple[str, str, str]:
        event_type = log_item["eventType"]
        event_id = log_item["id"]
        event_time = log_item["time"]
        return event_id, event_time, event_type
