import pandas as pd
import numpy as np
import warnings
from typing import Callable, List
import inspect

# classification
from model_monitoring.fairness_measures.fairness_measures import (
    statistical_parity_difference,
    disparate_impact_ratio,
    predictive_parity_difference,
    equal_opportunity_difference,
    average_odds_difference,
)

# regression
from model_monitoring.fairness_measures.fairness_measures import ddre_independence, ddre_separation, ddre_sufficiency

from model_monitoring.utils import (
    check_size,
    convert_Int_dataframe,
    convert_Int_series,
    convert_date_columns_to_seconds,
    convert_cluster_labels,
)
from model_monitoring.fairness_measures.fairness_measures import compute_metric_fairness


class FairnessMeasures:
    """Fairness Measures Class."""

    def __init__(
        self, approach_type="supervised", model_type="auto", set_metrics="standard", new_metrics=None, **kwargs
    ):
        """Fairness Measures Class.

        Args:
            approach_type (str): Approach type among "supervised" and "unsupervised". Defaults to "supervised".
            model_type (str): Modelling problem among "regression", "classification", "multiclass", "clustering" and "auto".
            set_metrics (str, optional): Metrics settings. It can be set "standard" for classical fairness metrics, "new" for setting a new dictionary of metrics and "add" for adding new metrics to the standard ones. Defaults to 'standard'.
            new_metrics (list, optional): list of new metrics when "set_metrics" is set to "new" and "add". Defaults to None.
        """
        # Check the approach_type
        if approach_type not in ["supervised", "unsupervised"]:
            raise ValueError(
                f"{approach_type} is not a valid approach_type. It should be one of the following:\n['supervised', 'unsupervised']"
            )
        else:
            self.approach_type = approach_type

        # Check the model_type
        if approach_type == "supervised":
            if model_type in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type for supervised approach. Select 'unsupervised' as approach_type or one of the following model_type:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            elif model_type not in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            else:
                self.model_type = model_type

        else:
            if model_type in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type for unsupervised approach. Select 'supervised' as approach_type or one of the following model_type:\n['clustering']"
                )
            elif model_type not in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['clustering']"
                )
            else:
                self.model_type = model_type

        # Check the set_metrics
        if set_metrics not in ["standard", "add", "new"]:
            raise ValueError(
                f"{set_metrics} is not a valid set_metrics. It should be one of the following:\n ['standard', 'add', 'new']"
            )
        self.set_metrics = set_metrics

        # Check new_metrics
        if self.set_metrics in ["add", "new"]:
            if new_metrics is None:
                self.new_metrics = []
            else:
                if isinstance(new_metrics, List):
                    self.new_metrics = new_metrics
                elif isinstance(new_metrics, Callable):
                    self.new_metrics = [new_metrics]
                else:
                    raise ValueError(f"{new_metrics} has not a valid format. It should be a list containing functions")

        # Set the metrics for each set_metric case
        if self.set_metrics == "new":
            self.metrics = self.new_metrics
        if self.set_metrics in ["standard", "add"]:
            if self.model_type == "regression":
                self.metrics = [ddre_independence, ddre_separation, ddre_sufficiency]
            elif self.model_type == "classification":
                self.metrics = [
                    statistical_parity_difference,
                    disparate_impact_ratio,
                    predictive_parity_difference,
                    equal_opportunity_difference,
                    average_odds_difference,
                ]
            elif self.model_type == "clustering":
                self.metrics = [ddre_independence]
            else:
                self.metrics = [
                    statistical_parity_difference,
                    predictive_parity_difference,
                    equal_opportunity_difference,
                    average_odds_difference,
                ]
            if self.set_metrics == "add":
                self.metrics = self.metrics + self.new_metrics

        self.target = None
        self.predictions = None
        self.X_fair = None
        self.fair_feat = None
        self.perf_metrics = None

        for k, v in kwargs.items():
            self.__dict__[k] = v

    def compute_metrics(self, predictions, X_fair, target=None, fair_feat=None, return_prop_true=True, **kwargs):
        """Compute fairness metrics.

        Args:
            target (np.array/pd.Series): target column
            X_fair (pd.DataFrame/pd.Series): data to be analyzed for fairness metric.
            predictions (np.array/pd.Series): Predictions (or cluster labels) array. Defaults to None
            fair_feat (str/list, optional): list of features (or list of features) to be analyzed for fairness metric. Defaults to None.
            return_prop_true (bool, optional): boolean that determines whether to return the portion of the target in binary classification. Defaults to None.

        Returns:
            dict: fairness metrics performances
        """
        for k, v in kwargs.items():
            self.__dict__[k] = v
        if isinstance(predictions, np.ndarray):
            predictions = pd.Series(predictions, name="predictions")
        if isinstance(X_fair, pd.Series):
            X_fair = pd.DataFrame(X_fair, index=X_fair.index, columns=[X_fair.name])
        if isinstance(fair_feat, str):
            fair_feat = [fair_feat]
        self.predictions = convert_Int_series(predictions)
        if fair_feat is None:
            fair_feat = X_fair.columns

        X_fair = convert_Int_dataframe(X_fair)
        self.X_fair = convert_date_columns_to_seconds(X_fair)
        self.fair_feat = fair_feat
        perf_metrics = dict()

        # Check size of the target and the features to be analyzed
        check_size(predictions, X_fair)
        if self.approach_type == "supervised":
            if target is None:
                raise ValueError('Target must not be None if approach_type is "supervised"')
            # Check size of the predictions and target
            check_size(predictions, target)
            check_size(target, X_fair)
            if isinstance(target, np.ndarray):
                target = pd.Series(target, name="target")
            self.target = convert_Int_series(target)
            vals = target.nunique()
            if vals == 1:
                warnings.warn("The target column selected is constant")
            elif self.model_type == "auto":
                if vals <= 2:
                    self.model_type = "classification"
                elif vals < 11:
                    self.model_type = "multiclass"
                else:
                    self.model_type = "regression"
            self.return_prop_true = return_prop_true

            if self.model_type in ["regression", "classification", "multiclass"]:
                for i in self.metrics:
                    dict_feat = dict()
                    for z in self.fair_feat:
                        dict_to_use = {
                            k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                        }
                        dict_labels = dict()
                        for j in self.X_fair[z].dropna().drop_duplicates().values:
                            if isinstance(j, List) or isinstance(j, np.ndarray):
                                j_str = ", ".join(map(str, j))
                                perc_label = (
                                    self.X_fair[z][(self.X_fair[z] == j).all(axis=1)].shape[0] / self.X_fair[z].shape[0]
                                )
                            else:
                                j_str = j
                                perc_label = self.X_fair[z][self.X_fair[z] == j].shape[0] / self.X_fair[z].shape[0]
                            dict_labels[j_str] = [
                                compute_metric_fairness(
                                    self.target,
                                    self.predictions,
                                    metric=i,
                                    fair_attr=self.X_fair[z],
                                    unpriv_group=j,
                                    **dict_to_use,
                                ),
                                perc_label,
                            ]
                            if self.model_type == "classification":
                                if self.return_prop_true:
                                    try:  # One Fairness Attribute
                                        dict_labels[j_str].append(
                                            (self.target[self.X_fair[z] == j] == 1).mean()
                                        )  # Add proportion of 1 label
                                    except Exception:  # More Fairness Attributes
                                        dict_labels[j_str].append(
                                            (self.target[(self.X_fair[z] == j).all(axis=1)] == 1).mean()
                                        )  # Add proportion of 1 label
                        if isinstance(z, List):
                            z_str = ", ".join(map(str, z))
                        else:
                            z_str = z
                        dict_feat[z_str] = dict_labels
                    perf_metrics[i.__name__] = dict_feat
            else:
                raise ValueError("Invalid model type.")
        # Unsupervised approach
        elif self.approach_type == "unsupervised":
            if self.target is not None:
                self.target = None
            if self.model_type == "clustering":
                vals = predictions.nunique()
                predictions = convert_cluster_labels(predictions, vals)
                if vals == 1:
                    warnings.warn("There is a single cluster")
                for i in self.metrics:
                    dict_feat = dict()
                    for z in self.fair_feat:
                        dict_to_use = {
                            k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                        }

                        dict_labels = dict()
                        for j in self.X_fair[z].dropna().drop_duplicates().values:
                            if isinstance(j, List) or isinstance(j, np.ndarray):
                                j_str = ", ".join(map(str, j))
                                perc_label = (
                                    self.X_fair[z][(self.X_fair[z] == j).all(axis=1)].shape[0] / self.X_fair[z].shape[0]
                                )
                            else:
                                j_str = j
                                perc_label = self.X_fair[z][self.X_fair[z] == j].shape[0] / self.X_fair[z].shape[0]
                            dict_labels[j_str] = [
                                compute_metric_fairness(
                                    self.target,
                                    self.predictions,
                                    metric=i,
                                    fair_attr=self.X_fair[z],
                                    unpriv_group=j,
                                    **dict_to_use,
                                ),
                                perc_label,
                            ]
                        if isinstance(z, List):
                            z_str = ", ".join(map(str, z))
                        else:
                            z_str = z
                        dict_feat[z_str] = dict_labels
                    perf_metrics[i.__name__] = dict_feat
            else:
                raise ValueError("Invalid model type.")
        self.perf_metrics = perf_metrics
        return self.perf_metrics
