"Wrappers for different question types."

from .tools import question
from .structure import Question, QuestionOptions


def radio(
    label, question_text, *answers, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for radio type."
    return question(
        label,
        question_text,
        *answers,
        question_type="radio",
        description=description,
        options=options,
        add_code=add_code,
    )


def checkbox(
    label, question_text, *answers, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for checkbox type."
    return question(
        label,
        question_text,
        *answers,
        question_type="checkbox",
        description=description,
        options=options,
        add_code=add_code,
    )


def text(
    label, question_text, *answers, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for text type."
    return question(
        label,
        question_text,
        *answers,
        question_type="text",
        description=description,
        options=options,
        add_code=add_code,
    )


def text_long(
    label, question_text, *answers, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for text_long type."
    return question(
        label,
        question_text,
        *answers,
        question_type="text_long",
        description=description,
        options=options,
        add_code=add_code,
    )


def dropdown(
    label, question_text, *answers, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for dropdown type."
    return question(
        label,
        question_text,
        *answers,
        question_type="dropdown",
        description=description,
        options=options,
        add_code=add_code,
    )


def dropdown_multi(
    label, question_text, *answers, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for dropdown_multi type."
    return question(
        label,
        question_text,
        *answers,
        question_type="dropdown_multi",
        description=description,
        options=options,
        add_code=add_code,
    )


def yes_no(
    label, question_text, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for yes_no type."
    return question(
        label,
        question_text,
        question_type="yes_no",
        description=description,
        options=options,
        add_code=add_code,
    )


def ranking(
    label, question_text, *answers, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for ranking type."
    return question(
        label,
        question_text,
        *answers,
        question_type="ranking",
        description=description,
        options=options,
        add_code=add_code,
    )


def info(label: str, text: str, options=None, add_code=None) -> Question:
    "Wrapper around question function for info type."
    return question(label, text, question_type="info", options=options)


def slider(
    label: str,
    question_text,
    range_min=0,
    range_max=100,
    pips_values=[0, 100],
    pips_text=["0", "100"],
    description=None,
    options=None,
    add_code=None,
) -> Question | list[Question]:
    "Wrapper around question function for slider type."
    if len(pips_text) != len(pips_values):
        raise ValueError("Length of pips_text and pips_values must be equal.")
    if not options:
        options = QuestionOptions()
    else:
        options = options.copy()
    setattr(options, "range_min", range_min)
    setattr(options, "range_max", range_max)
    setattr(options, "pips_values", pips_values)
    setattr(options, "pips_text", pips_text)

    return question(
        label,
        question_text,
        question_type="slider",
        description=description,
        options=options,
        add_code=add_code,
    )


def matrix(
    label, columns, *rows, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for matrix type."
    return question(
        label,
        columns,
        rows,
        question_type="matrix",
        description=description,
        options=options,
        add_code=add_code,
    )


def matrix_dynamic(
    label, question_text, columns, description=None, options=None, add_code=None
) -> Question | list[Question]:
    "Wrapper around question function for matrix_dymamic type."
    return question(
        label,
        question_text,
        columns,
        question_type="matrix_dynamic",
        description=description,
        options=options,
        add_code=add_code,
    )
