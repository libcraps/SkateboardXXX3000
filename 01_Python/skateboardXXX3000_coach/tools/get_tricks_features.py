from tools.trick_post_processing import *


def get_tricks_features(complete_sequence, events_interval, tricks_name):
    detail_report={}
    for i,trick_name in enumerate(tricks_name):
        # isolated_trick = complete_sequence.events_interval[i]
        isolated_trick=None #
        detail_report[trick_name] = get_trick_features(isolated_trick)
    print(detail_report)
    return detail_report

def get_trick_features(trick):
    report_feature_trick={}
    # en gros
    # report_feature_trick["height"] = get_height(trick)
    # report_feature_trick["azimuth"] = get_azimuth(trick)
    report_feature_trick["height"] = 666
    report_feature_trick["azimuth"] = 665

    return report_feature_trick