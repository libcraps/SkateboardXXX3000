# -*- coding: utf-8 -*-
import os
from operator import index, sub
from pathlib import Path

import jinja2
import pandas as pd
from prefect import task
from prefect.tasks import task_input_hash
from sqlalchemy import true
from omegaconf.dictconfig import DictConfig

@task()
def make_report_segment(metrics_per_model: dict, config:DictConfig):
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
        loader=jinja2.FileSystemLoader(Path("./report/report_templates")),
    )


    data = {
        "eval": data_eval,
        # # "inconsistency": data_inconsistency,
    }
    template = latex_jinja_env.get_template("template_segment_compact.tex")
    rendeur = template.render(data)

    return rendeur
