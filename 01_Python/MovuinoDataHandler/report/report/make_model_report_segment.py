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

    model_evaluated_names = list(metrics_per_model.keys())

    val_lim_segment = {
        "precision_0" :0.5,
        "precision_1" :0.5,
        "precision_2" :0.5,
        "precision_3" :0.5,
        "precision_4" :0.5,
        "recall_0" :0.5,
        "recall_1" :0.5,
        "recall_2" :0.5,
        "recall_3" :0.5,
        "recall_4" :0.5,
        "f1_score_0" :0.5,
        "f1_score_1" :0.5,
        "f1_score_2" :0.5,
        "f1_score_3" :0.5,
        "f1_score_4" :0.5,
        "iou_0" :0.5,
        "iou_1" :0.5,
        "iou_2" :0.5,
        "iou_3" :0.5,
        "iou_4" :0.5,
        "soft_max_incons_saga" :0.5,
        "soft_max_incons_0-3" :0.5,
        "soft_max_incons_0-2" :0.5,
        "soft_max_incons_2-3" :0.5,
    }
    val_lim_segment = config.valid_val
    sumup_segment = config.sumup

    # Tableau
    df_valid_eval = metrics_per_model[model_evaluated_names[0]]["mean"].copy()

    for v in val_lim_segment:
        col=list(v.keys())[0]
        val=list(v.values())[0]
        df_valid_eval.loc[:, [col]] = val

    df_report_eval_1 = {}
    df_report_eval_2 = {}
    df_report_cell_color_eval = {}

    columns_eval = metrics_per_model[model_evaluated_names[0]]["mean"].columns
    subgroups_eval = metrics_per_model[model_evaluated_names[0]]["mean"].index

    for model_name in model_evaluated_names:
        df_groups_eval = metrics_per_model[model_name]

        # ----- Basic metrics -------
        df_mean_eval = df_groups_eval["mean"]
        df_std_eval = df_groups_eval["std"]

        df_report_cell_color_eval = (df_mean_eval > df_valid_eval).astype(str)
        df_report_cell_color_eval = df_report_cell_color_eval.replace("True", "@cg")
        df_report_cell_color_eval = df_report_cell_color_eval.replace("False", "@cr")

        df_report_cell_color_intensity_eval = (
            ((pd.DataFrame.abs(df_mean_eval - df_valid_eval) / df_valid_eval) * 50 + 30)
            .round(0)
            .fillna(0)
            .astype(str)
        )

        df_report_eval_1[model_name] = (
            df_report_cell_color_eval
            + df_report_cell_color_intensity_eval
            + "@rb"
            + df_mean_eval.round(2).astype(str)
            + "@lb@lb@fns @pm "
            + df_std_eval.round(2).astype(str)
            + "@rb@rb"
        )
        df_report_eval_1[model_name] = df_report_eval_1[model_name].replace(
            "@cr0.0@rbnan@lb@lb@fns @pm nan@rb@rb", "-"
        )

    # transposing info in order to have comparaison of noedls for each subgroup
    for sub in subgroups_eval:
        df_report_eval_2[sub] = pd.DataFrame(
            index=model_evaluated_names, columns=columns_eval
        )
        df_mean_T = pd.DataFrame(index=model_evaluated_names, columns=columns_eval)

        for model_name in model_evaluated_names:
            df_report_eval_2[sub].loc[model_name] = df_report_eval_1[model_name].loc[
                sub
            ]
            df_mean_T.loc[model_name] = metrics_per_model[model_name]["mean"].loc[sub]

        df_report_max_cell = (df_mean_T == df_mean_T.max()).astype(str)
        df_report_bf = df_report_max_cell.replace("True", "@bf")
        df_report_bf = df_report_bf.replace("False", "")
        df_report_bf_rb = df_report_max_cell.replace("True", "@mrb")
        df_report_bf_rb = df_report_bf_rb.replace("False", "")

        df_report_eval_2[sub] = df_report_bf + df_report_eval_2[sub] + df_report_bf_rb

        # transposing info in order to have comparaison of noedls for each subgroup
        df_report_max_cell = (
            pd.DataFrame.abs(df_mean_T) == pd.DataFrame.abs(df_mean_T).min()
        ).astype(str)
        df_report_bf = df_report_max_cell.replace("True", "@bf")
        df_report_bf = df_report_bf.replace("False", "")
        df_report_bf_rb = df_report_max_cell.replace("True", "@mrb")
        df_report_bf_rb = df_report_bf_rb.replace("False", "")

    df_report_eval_3 = {}
    for s in list(df_report_eval_2.keys()):
        df_report_eval_3[s] = df_report_eval_2[s].loc[:,sumup_segment]

    data_eval = {
        "subgroup_per_model": df_report_eval_1,
        "model_per_subgroup": df_report_eval_2,
        "model_per_subgroup_sumup": df_report_eval_3,
    }


    data = {
        "eval": data_eval,
        # # "inconsistency": data_inconsistency,
    }
    template = latex_jinja_env.get_template("template_segment_compact.tex")
    rendeur = template.render(data)

    return rendeur
