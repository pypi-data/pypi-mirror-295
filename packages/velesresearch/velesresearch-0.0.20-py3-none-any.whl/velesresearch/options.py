"Options objects definitions"

from pydantic import BaseModel
from collections.abc import Sequence


class QuestionOptions(BaseModel):
    "Options for Question object"
    required: bool = False
    answers_order: str = "none"
    placeholder: str | None = None
    inherit_answers: str | None = None
    inherit_answers_mode: str = "all"
    comment: bool = False
    comment_text: str = "Other"
    comment_placeholder: str = ""
    visible: bool = True
    other: bool = False
    other_text: str = "Other"
    other_placeholder: str = ""
    none: bool = False
    none_text: str = "None"
    clear_button: bool = False
    visible_if: str | None = None
    editable_if: str | None = None
    requied_if: str | None = None
    hide_number: bool = False
    range_min: int = 0
    range_max: int = 100
    pips_values: Sequence[int] = [0, 100]
    pips_text: Sequence[str] = ["0", "100"]
    allow_add_rows: bool = True
    allow_remove_rows: bool = True
    allow_rows_drag_and_drop: bool = False
    row_count: int = 1
    min_row_count: int = 0
    max_row_count: int = 1000
    add_row_text: str = "Add row"


class PageOptions(BaseModel):
    "Options for Page object"
    read_only: bool = False
    time_limit: int | None = None
    visible: bool = True
    navigation_visibility: str = "inherit"
    visible_if: str | None = None
    editable_if: str | None = None
    requied_if: str | None = None


class SurveyOptions(BaseModel):
    "Options for Survey object"
    language: str = "en"
    number_of_groups: int = 1
    timer_position: str = "none"
    timer_mode: str | None = None
    url_on_complete: str | None = None
    allow_previous: bool = True
    clear_invivsible_values: str | bool = "none"
    start_page: bool = False
