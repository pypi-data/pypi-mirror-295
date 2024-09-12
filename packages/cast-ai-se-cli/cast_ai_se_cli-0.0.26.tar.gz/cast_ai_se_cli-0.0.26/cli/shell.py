"""
se-cli: The swiss army command-line for Cast.AI SE`s.

Usage:
    se-cli [-c <cluster_id>] [-d] demo <prep|off> <eks|aks|gcp>
    se-cli [-c <cluster_id>] [-d] [-n] snapshot <analyze> <basic|detailed|extra|csv>
    se-cli [-c <cluster_id>] [-d] audit <analyze>
    se-cli version

Options:
    -c, --cluster_id <cluster_id>  (Optional) Specify the cluster ID (will assume correct kubectl context)
    -d, --debug                    Enable debug logging
    -n, --no_cfg                   config.json will be ignored and will not be created - cluster_id should be provided

Commands:
    demo      Manage the demo environment
    snapshot  Manage snapshots
    audit     Manage audit logs
    version   Shows current version

Subcommands for "demo":
    on       Prep demo environment for demo (Get off hibernation)
    off      Hibernate demo environment
    refresh  Disable BinPacking and prep demo

Optional subcommands for "demo" (overrides -c, --cluster_id <cluster_id> picks cluster_id from config file of cloud)
    eks     Use EKS config cluster_id and context
    aks     Use AKS config cluster_id and context
    gcp     (not supported yet)

"""
import sys

from cli.orchestrators.demo_orch import DemoOrchestrator
from cli.orchestrators.snapshot_orch import SnapshotOrchestrator
from cli.orchestrators.audit_orch import AuditOrchestrator
from cli.services.general_responder_svc import GeneralResponder
from cli.services.misc_svc import init
from cli.services.version_svc import check_if_latest_version

from docopt import docopt


COMMANDS_TO_CLASS_MAPTABLE = {
    "demo": DemoOrchestrator,
    "snapshot": SnapshotOrchestrator,
    "audit": AuditOrchestrator,
    "version": GeneralResponder
}


def main():
    try:
        check_if_latest_version()
        parsed_options = docopt(__doc__, sys.argv[1:])
        cfg = init(parsed_options)
        orchestrator_class = COMMANDS_TO_CLASS_MAPTABLE[cfg.app_inputs["command"]]
        main_orch = orchestrator_class(cfg)
        main_orch.execute()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
