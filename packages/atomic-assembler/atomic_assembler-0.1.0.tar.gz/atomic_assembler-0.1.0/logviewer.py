from textual.app import App, ComposeResult
from textual.widgets import DataTable, Input, Static
from textual.reactive import reactive
from textual import log
import re
from typing import List, Tuple


class LogViewer(App):
    """A Textual app to view and filter log entries."""

    CSS = """
    #log_table { height: 1fr; }
    #filter_input { dock: top; margin: 1 1; }
    #status_bar { height: 1; dock: bottom; }
    """

    log_entries: List[Tuple[str, str, str, str, str]] = []
    filter_text = reactive("")
    current_sort = reactive((None, True))  # (column_index, is_ascending)

    def compose(self) -> ComposeResult:
        """Define the layout of the app."""
        yield Input(placeholder="Filter logs...", id="filter_input")
        yield DataTable(id="log_table")
        yield Static(id="status_bar")

    def on_mount(self) -> None:
        """Initialize the app when it's mounted."""
        self.load_log_file()
        table = self.query_one(DataTable)
        table.add_columns("Timestamp", "Logger", "Level", "File:Line", "Message")
        self.update_table()

    def load_log_file(self) -> None:
        """
        Load log entries from the debug.log file.

        Each log entry is parsed and stored as a tuple in self.log_entries.
        """
        try:
            with open("debug.log", "r") as file:
                for line in file:
                    match = re.match(
                        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - ([\w\.]+) - (\w+) - ([\w\.]+):(\d+) - (.+)",
                        line.strip(),
                    )
                    if match:
                        timestamp, logger, level, file, line_num, message = (
                            match.groups()
                        )
                        self.log_entries.append(
                            (
                                timestamp,
                                logger,
                                level,
                                f"{file}:{line_num}",
                                message.strip(),
                            )
                        )
            log.info(f"Loaded {len(self.log_entries)} log entries")
        except FileNotFoundError:
            log.error("debug.log file not found")
        except Exception as e:
            log.error(f"Error reading log file: {str(e)}")

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Handle changes in the filter input.

        Update the filter text and refresh the table.
        """
        self.filter_text = event.value
        self.update_table()

    def update_table(self) -> None:
        """
        Update the DataTable with filtered and sorted entries.

        This method is called whenever the filter or sort changes.
        """
        table = self.query_one(DataTable)
        table.clear(columns=False)  # Clear rows but keep columns

        filtered_entries = self.get_filtered_entries()
        sorted_entries = self.sort_entries(filtered_entries)

        for entry in sorted_entries:
            table.add_row(*entry)

        self.query_one("#status_bar").update(f"Showing {len(filtered_entries)} entries")

    def get_filtered_entries(self) -> List[Tuple[str, str, str, str, str]]:
        """
        Filter log entries based on the current filter text.

        Supports negative filtering with a leading '-'.
        Supports column-specific filtering with 'column:filter'.
        Returns all entries if no filter is applied.
        """
        if not self.filter_text:
            return self.log_entries

        column_filters = {
            "timestamp": [],
            "logger": [],
            "level": [],
            "file:line": [],
            "message": [],
        }

        # Split filter text into column-specific filters
        for part in self.filter_text.split():
            if ":" in part:
                column, filter_text = part.split(":", 1)
                if column in column_filters:
                    column_filters[column].append(filter_text.lower())
            else:
                for column in column_filters:
                    column_filters[column].append(part.lower())

        def entry_matches(entry: Tuple[str, str, str, str, str]) -> bool:
            columns = ["timestamp", "logger", "level", "file:line", "message"]
            for i, column in enumerate(columns):
                for filter_text in column_filters[column]:
                    if filter_text.startswith("-"):
                        if filter_text[1:] in entry[i].lower():
                            return False
                    else:
                        if filter_text not in entry[i].lower():
                            return False
            return True

        return [entry for entry in self.log_entries if entry_matches(entry)]

    def sort_entries(
        self, entries: List[Tuple[str, str, str, str, str]]
    ) -> List[Tuple[str, str, str, str, str]]:
        """
        Sort the given entries based on the current sort column and direction.

        Returns the original list if no sorting is applied.
        """
        if self.current_sort[0] is not None:
            return sorted(
                entries,
                key=lambda x: x[self.current_sort[0]],
                reverse=not self.current_sort[1],
            )
        return entries

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected) -> None:
        """
        Handle column header selection for sorting.

        Toggle sort direction if the same column is selected,
        or set ascending sort for a new column.
        """
        if self.current_sort[0] == event.column_index:
            self.current_sort = (event.column_index, not self.current_sort[1])
        else:
            self.current_sort = (event.column_index, True)
        self.update_table()


if __name__ == "__main__":
    app = LogViewer()
    app.run()
