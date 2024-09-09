import pandas as pd

from .stats_tables import PlotStatsTables


class ClassificationPlotDriver:
    def __init__(
        self,
        true,
        pred,
        meta,
        pred_categorical,
        pred_logits,
        meta_pred_true,
        class_mappings,
        loss,
    ):
        self.plot_stats_tables = PlotStatsTables(
            true=true,
            pred_logits=pred_logits,
            pred_categorical=pred_categorical,
            meta_pred_true=meta_pred_true,
            class_mappings=class_mappings,
        )

    def plot_tp_tn_fp_fn(self, target_class=None, target_attribute_dict=None):
        return self.plot_stats_tables.tp_tn_fp_fn(
            target_class=target_class, target_attribute_dict=target_attribute_dict
        )

    def plot_statistics_classbased_table(self, target_attribute_dict=None):
        return self.plot_stats_tables.statistics_classbased_table(
            target_attribute_dict=target_attribute_dict
        )

    def plot_highlighted_overall_metrics(self):
        return self.plot_stats_tables.highlighted_overall_metrics()

    def plot_class_performances(self):
        return self.plot_stats_tables.class_performances()