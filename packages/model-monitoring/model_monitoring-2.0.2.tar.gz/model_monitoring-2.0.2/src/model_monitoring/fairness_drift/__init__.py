import pandas as pd
import warnings
from typing import Dict

from model_monitoring.utils import check_metrics_sets
from model_monitoring.config import read_config

from model_monitoring.fairness_drift.fairness_drift import (
    check_fairness_groups,
)

params = read_config(config_dir="config", name_params="params.yml")
standard_threshold = params["fairness_treshold"]


class FairnessDrift:
    """Fairness Drift Class."""

    def __init__(self, fair_metrics_curr, config_threshold=None):
        """Fairness Drift Class.

        Args:
            fair_metrics_curr (dict): dictionary containing current fairness metrics perfomances
            config_threshold (dict, optional): dictionary containing threshold settings. Defaults to None.
        """
        if not isinstance(fair_metrics_curr, Dict):
            raise ValueError(
                "Fairness metrics in input has not a valid format. It should be a dictionary containing functions as keys and values as values."
            )
        if config_threshold is None:
            config_threshold = standard_threshold

        check_metrics = [
            i for i in fair_metrics_curr.keys() if (i not in config_threshold.keys()) and (i != "proportion_1")
        ]
        if len(check_metrics) > 0:
            warnings.warn(f"{check_metrics} do not have threshold settings in config_threshold")

        list_com_metrics = list(set(fair_metrics_curr.keys()).intersection(set(config_threshold.keys())))
        fair_metrics_curr_com = {x: fair_metrics_curr[x] for x in list_com_metrics}

        # initialize reduced report with variables and groups
        self.report_reduced = pd.DataFrame(
            [
                {"vars": key, "groups": group, "curr_perc_label": values[1]}
                if len(values) == 2
                else {"vars": key, "groups": group, "curr_perc_label": values[1], "proportion_1_curr": values[2]}
                for key, groups in fair_metrics_curr_com[list(fair_metrics_curr_com.keys())[0]].items()
                for group, values in groups.items()
            ]
        )
        for x in fair_metrics_curr_com.keys():
            self.report_reduced[x + "_curr_perf"] = [
                values[0] for key, groups in fair_metrics_curr_com[x].items() for group, values in groups.items()
            ]
        # for output report columns ordering according to current percentage label
        self.report_reduced = self.report_reduced.sort_values(by=["vars", "curr_perc_label"], ascending=[True, False])

        self.fair_metrics_curr = fair_metrics_curr
        self.config_threshold = config_threshold
        self.perf_metrics_stor = None
        self.relative_reduced = False

    def get_absolute_reduced(self):
        """Load on the reduced report the absolute alert on current fairness metrics performances."""
        # Generation Alert
        for x in self.report_reduced.groups.values:
            warning_red = ""
            warning_yellow = ""
            for a in [y[:-10] for y in self.report_reduced.columns if "curr_perf" in y]:
                absolute_red = self.config_threshold[a]["absolute"]["red"]
                absolute_yellow = self.config_threshold[a]["absolute"]["yellow"]

                if self.config_threshold[a]["logic"] == "decrease":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if absolute_red != "None":
                        if curr_perf < absolute_red:
                            if warning_red == "":
                                warning_red += f"Red Alert for {a}"
                            else:
                                warning_red += f", {a}"
                        else:
                            if absolute_yellow != "None":
                                if (curr_perf > absolute_red) and (curr_perf < absolute_yellow):
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"
                    else:
                        if absolute_yellow != "None":
                            if curr_perf < absolute_yellow:
                                if warning_yellow == "":
                                    warning_yellow += f"Yellow Alert for {a}"
                                else:
                                    warning_yellow += f", {a}"

                elif self.config_threshold[a]["logic"] == "increase":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if absolute_red != "None":
                        if curr_perf > absolute_red:
                            if warning_red == "":
                                warning_red += f"Red Alert for {a}"
                            else:
                                warning_red += f", {a}"
                        else:
                            if absolute_yellow != "None":
                                if (curr_perf < absolute_red) and (curr_perf > absolute_yellow):
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"
                    else:
                        if absolute_yellow != "None":
                            if curr_perf > absolute_yellow:
                                if warning_yellow == "":
                                    warning_yellow += f"Yellow Alert for {a}"
                                else:
                                    warning_yellow += f", {a}"

                elif self.config_threshold[a]["logic"] == "axial":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if absolute_red != "None":
                        if (curr_perf > max(absolute_red)) or (curr_perf < min(absolute_red)):
                            if warning_red == "":
                                warning_red += f"Red Alert for {a}"
                            else:
                                warning_red += f", {a}"
                        else:
                            if absolute_yellow != "None":
                                if ((curr_perf < max(absolute_red)) and (curr_perf > min(absolute_red))) and (
                                    (curr_perf > max(absolute_yellow)) or (curr_perf < min(absolute_yellow))
                                ):
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"
                    else:
                        if absolute_yellow != "None":
                            if (curr_perf > max(absolute_yellow)) or (curr_perf < min(absolute_yellow)):
                                if warning_yellow == "":
                                    warning_yellow += f"Yellow Alert for {a}"
                                else:
                                    warning_yellow += f", {a}"
                else:
                    raise ValueError(
                        f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                    )
            if (warning_red != "") and (warning_yellow != ""):
                warning = warning_red + ", " + warning_yellow
            else:
                warning = warning_red + warning_yellow
            self.report_reduced.loc[self.report_reduced.groups == x, "absolute_warning"] = warning

        # Locate Absolute_warning before Stor_Perc_label
        if self.relative_reduced:
            absolute_warning = self.report_reduced.pop("absolute_warning")

            self.report_reduced.insert(
                self.report_reduced.columns.get_loc("stor_perc_label"), "absolute_warning", absolute_warning
            )

    def get_relative_reduced(self, fair_metrics_stor):
        """Load on the reduced report the historichal fairness metrics performances, drift compared to the current fairness performances and relative alert on drift.

        Args:
            fair_metrics_stor (dict): dictionary containing historichal fairness metrics perfomances.
        """
        # re-initialize report
        if self.relative_reduced:
            list_drop = [
                x
                for x in self.report_reduced.columns
                if (x in ["stor_perc_label", "drift_perc", "relative_warning", "proportion_1_stor"])
                or ("stor_perf" in x)
            ]
            self.report_reduced = self.report_reduced.drop(columns=list_drop)

        # Check if the metrics are the same
        check_metrics_sets(metrics_1=fair_metrics_stor, metrics_2=self.fair_metrics_curr)

        list_com_metrics = list(set(fair_metrics_stor.keys()).intersection(set(self.fair_metrics_curr.keys())))
        self.fair_metrics_stor = {x: fair_metrics_stor[x] for x in list_com_metrics}
        stor_report_reduced = pd.DataFrame(
            [
                {"vars": key, "groups": group, "stor_perc_label": values[1]}
                if len(values) == 2
                else {"vars": key, "groups": group, "stor_perc_label": values[1], "proportion_1_stor": values[2]}
                for key, groups in self.fair_metrics_stor[list(self.fair_metrics_stor.keys())[0]].items()
                for group, values in groups.items()
            ]
        )
        for x in self.fair_metrics_stor.keys():
            stor_report_reduced[x + "_stor_perf"] = [
                values[0] for key, groups in self.fair_metrics_stor[x].items() for group, values in groups.items()
            ]

        # Check if the fairness group are the same
        list_no_join = check_fairness_groups(self.report_reduced, stor_report_reduced, multiindex=False)

        # Add historical fairness performances to the reduced report and limit to common fairness groups
        self.report_reduced = self.report_reduced.merge(stor_report_reduced, how="inner", on=["vars", "groups"])

        # Generation Drift
        for a in [y[:-10] for y in self.report_reduced.columns if "stor_perf" in y]:
            if self.config_threshold[a]["logic"] in ["decrease", "increase"]:
                for x in self.report_reduced.groups.values:
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    if stor_perf > 0:
                        self.report_reduced.loc[self.report_reduced.groups == x, "drift_perc_" + a] = (
                            (curr_perf - stor_perf) / stor_perf * 100
                        )
                    else:
                        self.report_reduced.loc[self.report_reduced.groups == x, "drift_perc_" + a] = (
                            (stor_perf - curr_perf) / stor_perf * 100
                        )
                drift = self.report_reduced.pop("drift_perc_" + a)
                self.report_reduced.insert(
                    self.report_reduced.columns.get_loc(a + "_stor_perf") + 1, "drift_perc_" + a, drift
                )

            elif self.config_threshold[a]["logic"] == "axial":
                axial_point = self.config_threshold[a]["axial_point"]
                for x in self.report_reduced.groups.values:
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    self.report_reduced.loc[self.report_reduced.groups == x, "drift_perc_" + a] = (
                        (abs(curr_perf - axial_point) - abs(stor_perf - axial_point))
                        / abs(stor_perf - axial_point)
                        * 100
                    )
                drift = self.report_reduced.pop("drift_perc_" + a)
                self.report_reduced.insert(
                    self.report_reduced.columns.get_loc(a + "_stor_perf") + 1, "drift_perc_" + a, drift
                )

            else:
                raise ValueError(
                    f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                )

        # Generation Alert
        for x in self.report_reduced.groups.values:
            warning_red = ""
            warning_yellow = ""
            for a in [y[:-10] for y in self.report_reduced.columns if "curr_perf" in y]:
                relative_red = self.config_threshold[a]["relative"]["red"]
                relative_yellow = self.config_threshold[a]["relative"]["yellow"]
                absolute_tol = self.config_threshold[a]["relative"]["absolute_tol"]

                if self.config_threshold[a]["logic"] == "decrease":
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    if relative_red != "None":
                        # check absolute tollerance for relative alert
                        if abs(curr_perf - stor_perf) >= absolute_tol:
                            drift_perf = self.report_reduced.loc[
                                self.report_reduced.groups == x, "drift_perc_" + a
                            ].values[0]
                            if drift_perf < relative_red * 100:
                                if warning_red == "":
                                    warning_red += f"Red Alert for {a}"
                                else:
                                    warning_red += f", {a}"
                            else:
                                if relative_yellow != "None":
                                    if (drift_perf > relative_red * 100) and (drift_perf < relative_yellow * 100):
                                        if warning_yellow == "":
                                            warning_yellow += f"Yellow Alert for {a}"
                                        else:
                                            warning_yellow += f", {a}"
                    else:
                        if relative_yellow != "None":
                            # check absolute tollerance for relative alert
                            if abs(curr_perf - stor_perf) >= absolute_tol:
                                drift_perf = self.report_reduced.loc[
                                    self.report_reduced.groups == x, "drift_perc_" + a
                                ].values[0]
                                if drift_perf < relative_yellow * 100:
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"

                elif self.config_threshold[a]["logic"] in ["increase", "axial"]:
                    curr_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_curr_perf"].values[0]
                    stor_perf = self.report_reduced.loc[self.report_reduced.groups == x, a + "_stor_perf"].values[0]
                    if relative_red != "None":
                        # check absolute tollerance for relative alert
                        if abs(curr_perf - stor_perf) >= absolute_tol:
                            drift_perf = self.report_reduced.loc[
                                self.report_reduced.groups == x, "drift_perc_" + a
                            ].values[0]
                            if drift_perf > relative_red * 100:
                                if warning_red == "":
                                    warning_red += f"Red Alert for {a}"
                                else:
                                    warning_red += f", {a}"
                            else:
                                if relative_yellow != "None":
                                    if (drift_perf < relative_red * 100) and (drift_perf > relative_yellow * 100):
                                        if warning_yellow == "":
                                            warning_yellow += f"Yellow Alert for {a}"
                                        else:
                                            warning_yellow += f", {a}"
                    else:
                        if relative_yellow != "None":
                            # check absolute tollerance for relative alert
                            if abs(curr_perf - stor_perf) >= absolute_tol:
                                drift_perf = self.report_reduced.loc[
                                    self.report_reduced.groups == x, "drift_perc_" + a
                                ].values[0]
                                if drift_perf > relative_yellow * 100:
                                    if warning_yellow == "":
                                        warning_yellow += f"Yellow Alert for {a}"
                                    else:
                                        warning_yellow += f", {a}"

                else:
                    raise ValueError(
                        f"{self.config_threshold[a]['logic']} is not a valid logic for {a} metric. Choose between ['increase','decrease','axial']."
                    )
            if (warning_red != "") and (warning_yellow != ""):
                warning = warning_red + ", " + warning_yellow
            else:
                warning = warning_red + warning_yellow
            self.report_reduced.loc[self.report_reduced.groups == x, "relative_warning"] = warning

        self.relative_reduced = True

    def get_report_reduced(self):
        """Return the reduced report.

        Returns:
            pd.DataFrame: reduced report of the class
        """
        return self.report_reduced
