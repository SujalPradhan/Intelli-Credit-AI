from datetime import datetime, timezone


class PipelineLogger:
    """Collects structured logs for each stage of the research pipeline."""

    def __init__(self):
        self._logs: list[dict] = []

    def log(self, stage: str, data: dict | list | str) -> None:
        """Append a timestamped log entry for a pipeline stage."""
        entry = {
            "stage": stage,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }
        self._logs.append(entry)

    def get_logs(self) -> list[dict]:
        """Return all collected pipeline logs."""
        return list(self._logs)
