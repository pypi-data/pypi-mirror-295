from typing import Callable
from yaspin import yaspin

from cast_ai.se.models.execution_status import ExecutionStatus

from cli.models.config import ConfigObject
from cli.models.timed_text import TimedText


class BaseOrchestrator:
    def __init__(self, cfg: ConfigObject):
        self._cfg = cfg

    @staticmethod
    def spinner_run(msg: str, action: Callable[[], ExecutionStatus]) -> ExecutionStatus:
        with yaspin(text=TimedText(msg)) as spinner:
            try:
                result = action()
                if result.success:
                    spinner.ok("✅ [Success]")
                else:
                    spinner.fail(f"😢 [Failed:{result.error_message}]")
                return result
            except Exception as e:
                spinner.fail(f"💥 [Failed:{str(e)}]")
