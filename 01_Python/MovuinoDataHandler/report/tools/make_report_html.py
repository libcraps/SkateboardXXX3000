# -*- coding: utf-8 -*-
import os
import jinja2
from pathlib import Path

def make_report_html(data):

    beginning = """
    <!DOCTYPE html>
    <html lang="fr">
    """

    end = """
    """

    latex_jinja_env = jinja2.Environment(
    block_start_string="\BLOCK{",
    block_end_string="}",
    variable_start_string="\VAR{",
    variable_end_string="}",
    comment_start_string="\#{",
    comment_end_string="}",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=False,
    lstrip_blocks=False,
    autoescape=False,
    loader=jinja2.FileSystemLoader(Path("./report/")),
    )

    print(Path("report/").exists())
    template = latex_jinja_env.get_template("template_coach.html")
    render = template.render(data)

    return beginning + render + end
