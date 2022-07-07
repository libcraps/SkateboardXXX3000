# -*- coding: utf-8 -*-
import os
import jinja2
from pathlib import Path

def make_report_latex(data):

    beginning = """
    \\documentclass[a4paper,11pt]{article}
    \\usepackage{booktabs}
    % \\usepackage{xcolor}
    \\usepackage[table]{xcolor}
    \\usepackage[utf8]{inputenc}
    \\usepackage{fancyhdr}
    \\usepackage{sectsty}

    \\usepackage{multirow}
    \\usepackage{hyperref}
    \\usepackage{graphicx}
    \\usepackage{caption}
    \\usepackage{mathtools}
    \\usepackage{ragged2e}
    \\usepackage{tcolorbox}
    \\usepackage{stackengine}
    \\usepackage{enumitem}
    \\usepackage{longtable}
    \\usepackage{multirow}
    \\usepackage{tabularx}

    \\usepackage{float}
    \\floatstyle{plaintop}
    \\restylefloat{table}


    \\usepackage[margin=0cm]{caption}
    \\setlength{\\topmargin}{-45pt}
    \\setlength{\\oddsidemargin}{-3mm}
    \\setlength{\\textheight}{25cm}
    \\setlength{\\textwidth}{172mm}

    \\usepackage{fancyhdr}
    \\setlength{\\headheight}{15.2pt}
    \\pagestyle{fancy}


    %\\usepackage[showframe=true]{geometry}
    \\usepackage{geometry}
     \\geometry{
        total={170mm,257mm},
        left=10mm,
        top=20mm,
        }


    \\setlength{\\columnsep}{8mm}

    \\allsectionsfont{\\centering}

    %%%START HERE!
    %%%Input the RD number and report title here. It will update the title and header automatically :)
    \\newcommand\\rd{Rapport}
    \\newcommand\\rdtitle{SkateboardXXX3000}

    \\rhead{\\rd \\hspace{0.5mm} \\rdtitle}
    \\lhead{}

    \\begin{document}
    """

    end = """
    \n
    \\end{document}
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
    template = latex_jinja_env.get_template("template_coach.tex")
    render = template.render(data)

    return beginning + render + end
