import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class ChangeLogger:
    """Maintains an append-only log.md file tracking all knowledge base changes"""

    def __init__(self, wiki_dir: Path):
        self.wiki_dir = wiki_dir
        self.log_file = wiki_dir / "log.md"
        self._ensure_log_file()

    def _ensure_log_file(self) -> None:
        """Create log.md if it doesn't exist"""
        if not self.log_file.exists():
            header = "# Knowledge Base Change Log\n\nAppend-only log of all ingestions, queries, and maintenance operations.\n\n"
            self.log_file.write_text(header, encoding="utf-8")
            logger.info(f"Created change log at {self.log_file}")

    def log_ingest(self, title: str, source_path: str, action: str = "ingest") -> None:
        """Log an ingestion operation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"## [{timestamp}] {action} | {title}\n\n"
        entry += f"- Source: `{source_path}`\n"
        entry += f"- Time: {timestamp}\n\n"

        self._append_entry(entry)

    def log_query(self, question: str, result_count: int) -> None:
        """Log a query operation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"## [{timestamp}] query | {question[:50]}...\n\n"
        entry += f"- Question: {question}\n"
        entry += f"- Results: {result_count} source(s)\n"
        entry += f"- Time: {timestamp}\n\n"

        self._append_entry(entry)

    def log_maintenance(self, operation: str, details: str = "") -> None:
        """Log a maintenance operation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"## [{timestamp}] maintenance | {operation}\n\n"
        entry += f"- Operation: {operation}\n"
        if details:
            entry += f"- Details: {details}\n"
        entry += f"- Time: {timestamp}\n\n"

        self._append_entry(entry)

    def log_merge(self, source_file: str, target_file: str) -> None:
        """Log a merge/duplicate detection operation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"## [{timestamp}] merge | Duplicate detection\n\n"
        entry += f"- Source: `{source_file}`\n"
        entry += f"- Target: `{target_file}`\n"
        entry += f"- Time: {timestamp}\n\n"

        self._append_entry(entry)

    def log_forward_links(self, updated_count: int, broken_count: int) -> None:
        """Log forward links application"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"## [{timestamp}] maintenance | Forward links applied\n\n"
        entry += f"- Updated: {updated_count} article(s)\n"
        entry += f"- Broken links found: {broken_count}\n"
        entry += f"- Time: {timestamp}\n\n"

        self._append_entry(entry)

    def _append_entry(self, entry: str) -> None:
        """Append an entry to the log file"""
        try:
            current_content = self.log_file.read_text(encoding="utf-8")
            updated_content = current_content + entry
            self.log_file.write_text(updated_content, encoding="utf-8")
            logger.debug(f"Logged entry to {self.log_file}")
        except Exception as e:
            logger.error(f"Failed to append to change log: {e}")

    def get_recent_entries(self, limit: int = 10) -> str:
        """Get the last N entries from the log"""
        if not self.log_file.exists():
            return "No change log entries yet."

        content = self.log_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Count heading markers (##) to get entries
        entries = []
        current_entry = []

        for line in lines:
            if line.startswith("## ["):
                if current_entry:
                    entries.append("\n".join(current_entry))
                current_entry = [line]
            elif current_entry:
                current_entry.append(line)

        if current_entry:
            entries.append("\n".join(current_entry))

        # Return last N entries
        recent = entries[-limit:] if entries else []
        return "\n\n".join(recent)
