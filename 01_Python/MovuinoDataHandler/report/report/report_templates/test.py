# -*- coding: utf-8 -*-
import os

import jinja2
from jinja2 import Template

print()
latex_jinja_env = jinja2.Environment(
    block_start_string="\BLOCK{",
    block_end_string="}",
    variable_start_string="\VAR{",
    variable_end_string="}",
    comment_start_string="\#{",
    comment_end_string="}",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.realpath("./report_test_jinja2")),
)
template = latex_jinja_env.get_template("template_detect.tex")
print(template.render(section1="Long Form", section2="Short Form"))

template = "Device {{ name }} is a {{ type }} located in the {{ site }} datacenter."

data = {
    "name": "waw-rtr-core-01",
    "site": "warsaw-01",
}

j2_template = Template(template)

print(j2_template.render(data))
