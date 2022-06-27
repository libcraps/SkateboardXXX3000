# -*- coding: utf-8 -*-
import os

from omegaconf.dictconfig import DictConfig

from steps.make_model_report_detect import make_model_report_detect
from steps.make_model_report_segment import make_report_segment
from tools.model_report_detect import bold_max_metrics, dict_to_latex


def make_model_report(
    det_metrics_per_model, seg_metrics_per_model, config:DictConfig,_config: DictConfig
):

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
    \\newcommand\\rd{RD\\_999}
    \\newcommand\\rdtitle{Rokken Report Template}

    \\rhead{\\rd \\hspace{0.5mm} \\rdtitle}
    \\lhead{}

    \\begin{document}
    """

    end = """
    \n
    \\end{document}
    """

    bold_max_metrics(det_metrics_per_model[0])
    render_det = (
        "\\section{DETECTION}\n\\subsection{Model Comparison}"
        + dict_to_latex(det_metrics_per_model[0])
        + "\n\\subsection{Comparison by Group}\\begin{itemize}[leftmargin=0cm]"
        + det_metrics_per_model[1]
        + "\n\\end{itemize}"
    )

    render_seg = make_report_segment(metrics_per_model=seg_metrics_per_model,config=config.segment).result()

    # render_det=""
    # render_seg="ok"

    return beginning + render_det + render_seg + end
