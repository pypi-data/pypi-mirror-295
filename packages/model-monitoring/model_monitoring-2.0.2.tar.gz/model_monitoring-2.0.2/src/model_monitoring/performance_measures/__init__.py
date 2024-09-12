# regression
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    explained_variance_score,
    median_absolute_error,
)

# classification
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    balanced_accuracy_score,
)

import warnings
import pandas as pd
import numpy as np
from typing import Dict
import inspect

from model_monitoring.imputer import cluster_imputing
from model_monitoring.utils import (
    check_size,
    convert_Int_series,
    convert_Int_dataframe,
    convert_date_columns_to_seconds,
    convert_cluster_labels,
)
from model_monitoring.performance_measures.performance_measures import (
    compute_metric,
    compute_unsupervised_metric,
)
from model_monitoring.additional_metrics import classification_clustering


class PerformancesMeasures:
    """Performance Measures Class."""

    def __init__(
        self,
        approach_type="supervised",
        model_type="auto",
        set_metrics="standard",
        new_metrics=None,
        impute_nans=False,
        **kwargs,
    ):
        """Performance Measures Class.

        Args:
            approach_type (str): Type of approach: "supervised" or "unsupervised". Defaults to 'supervised'.
            model_type (str): Modelling problem among supervised ones: "regression", "classification", "multiclass" and "auto", or unsupervised one: "clustering". Defaults to 'auto'.
            set_metrics (str, optional): Metrics settings. It can be set "standard" for classical ML metrics, "new" for setting a new dictionary of metrics and "add" for adding new metrics to the standard ones. Defaults to 'standard'.
            new_metrics (dict/list, optional): If supervised approach: Dictionary of new metrics as keys when "set_metrics" is set to "new" and "add", and one among ['pred','prob'] as values. If unsupervised approach: list of new metrics. Defaults to None.
            impute_nans (bool): for unsupervised approach, if True, NaNs are filled if False they are not. Defaults to False

        """
        if approach_type not in ["supervised", "unsupervised"]:
            raise ValueError(
                f"{approach_type} is not a valid approach, select one of the following:\n['supervised','unsupervised']"
            )
        else:
            self.approach_type = approach_type
        # Check approach_type and model_type

        if self.approach_type == "supervised":
            if model_type in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a supervised model, select one of the following:\n['auto', 'regression', 'classification', 'multiclass'], or select an unsupervised one between:\n['clustering']"
                )
            elif model_type not in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['auto', 'regression', 'classification', 'multiclass','clustering']"
                )
            else:
                self.model_type = model_type
                self.impute_nans = False
        else:
            if model_type in ["auto", "regression", "classification", "multiclass"]:
                raise ValueError(
                    f"{model_type} is not an unsupervised model, select one of the following:\n['clustering'], or select a supervised one between:\n['auto', 'regression', 'classification', 'multiclass']"
                )
            elif model_type not in ["clustering"]:
                raise ValueError(
                    f"{model_type} is not a valid algo_type. It should be one of the following:\n['auto', 'regression', 'classification', 'multiclass','clustering']"
                )
            else:
                self.model_type = model_type
                self.impute_nans = impute_nans
        # Check the set_metrics

        if set_metrics not in ["standard", "add", "new"]:
            raise ValueError(
                f"{set_metrics} is not a valid set_metrics. It should be one of the following:\n ['standard', 'add', 'new']"
            )
        self.set_metrics = set_metrics

        # Check new_metrics
        if self.set_metrics in ["add", "new"]:
            if self.approach_type == "supervised":
                if new_metrics is None:
                    self.new_metrics = {}
                else:
                    if isinstance(new_metrics, Dict):
                        if set(new_metrics.values()).issubset(set(["pred", "prob"])):
                            self.new_metrics = new_metrics
                        else:
                            raise ValueError(
                                f"{list(set(new_metrics.values()))} contains invalid input. Valid inputs are ['pred', 'prob']"
                            )
                    else:
                        raise ValueError(
                            f"{new_metrics} has not a valid format. It should be a dictionary containing functions as keys and one of ['pred', 'prob'] as values."
                        )
            else:
                if new_metrics is None:
                    self.new_metrics = []
                else:
                    if isinstance(new_metrics, list):
                        self.new_metrics = new_metrics
                    else:
                        raise ValueError(
                            f"{new_metrics} has not a valid format. It should be a list containing functions"
                        )
        else:
            self.new_metrics = new_metrics
        # Set the metrics for each set_metric case
        if self.set_metrics == "new":
            self.metrics = self.new_metrics
        if self.set_metrics in ["standard", "add"]:
            if self.model_type == "regression":
                self.metrics = {
                    mean_squared_error: "pred",
                    r2_score: "pred",
                    median_absolute_error: "pred",
                    explained_variance_score: "pred",
                }
            elif self.model_type == "classification":
                self.metrics = {
                    balanced_accuracy_score: "pred",
                    accuracy_score: "pred",
                    precision_score: "pred",
                    recall_score: "pred",
                    f1_score: "pred",
                    roc_auc_score: "prob",
                }

            elif self.model_type == "clustering":
                self.metrics = [classification_clustering]
            else:
                self.metrics = {balanced_accuracy_score: "pred", accuracy_score: "pred", roc_auc_score: "prob"}
            if self.set_metrics == "add":
                if self.approach_type == "supervised":
                    self.metrics = {**self.metrics, **self.new_metrics}
                else:
                    self.metrics = self.metrics + self.new_metrics

        # Check model_params
        self.predictions = None
        self.prob = None
        self.target = None
        self.perf_metrics = None
        self.cluster_labels = None
        self.data_matrix = None
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def compute_metrics(
        self,
        target=None,
        predictions=None,
        prob=None,
        cluster_labels=None,
        data_matrix=None,
        return_prop_true=True,
        classification_threshold=0.5,
        **kwargs,
    ):
        """Compute metrics performances.

        Args:
            target (np.array/pd.Series): target column
            predictions (np.array/pd.Series, optional): Predictions array. Defaults to None.
            prob (np.array/pd.Series, optional): Probabilities prob for classification. Defaults to None.
            cluster_labels (np.array/pd.Series, optional): Cluster labels array. Defaults to None
            data_matrix (dictionary/pd.Dataframe, optional): data to compute cluster metrics. Defaults to None
            return_prop_true (bool, optional): boolean that determines whether to return the portion of the target in binary classification. Defaults to True.
            classification_threshold (float, optional): threshold for binary classification predictions. Defaults to 0.5.

        Returns:
            dict: metrics performances
        """
        # Create perf_metric dict
        for k, v in kwargs.items():
            self.__dict__[k] = v
        perf_metrics = dict()
        # Metric if supervised approach
        if self.approach_type == "supervised":
            # Check one among predictions and prob exists
            if target is None:
                raise ValueError("target must not be None")
            if (predictions is None) and (prob is None):
                raise ValueError("at least one among predictions and prob must be not None")

            # Check size of the predictions and target
            if predictions is not None:
                check_size(predictions, target)

            # Check size of the target and prob
            if prob is not None:
                check_size(target, prob)

            if isinstance(target, np.ndarray):
                target = pd.Series(target, name="target")
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

            if self.model_type == "regression":
                if predictions is None:
                    raise ValueError("predictions not provided")

            self.target = convert_Int_series(target)
            if predictions is not None:
                self.predictions = convert_Int_series(predictions)
            else:
                self.predictions = predictions
            if prob is not None:
                self.prob = convert_Int_series(prob)
            else:
                self.prob = prob

            self.return_prop_true = return_prop_true
            self.classification_threshold = classification_threshold

            if self.model_type == "regression":
                for i, j in self.metrics.items():
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    if j == "pred":
                        perf_metrics[i.__name__] = compute_metric(
                            self.target, self.predictions, metric=i, **dict_to_use
                        )
                    else:
                        warnings.warn(
                            f"{j} is a wrong label for regression model type. Label {i.__name__} with 'pred'."
                        )
            elif self.model_type == "classification":
                if self.predictions is None:
                    try:
                        self.predictions = self.prob.apply(lambda x: 1 if x > self.classification_threshold else 0)
                    except Exception:
                        self.predictions = np.array([1 if i > self.classification_threshold else 0 for i in self.prob])
                for i, j in self.metrics.items():
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    # some metrics don't work well with 1 target value (e.g. roc_auc_score)
                    if vals == 1:
                        if i.__name__ in ["roc_auc_score", "lift_score", "gain_score"]:
                            warnings.warn(f"{i.__name__} cannot be used when target has a constant value.")
                            continue
                    if j == "prob":
                        if self.prob is None:
                            warnings.warn(f"{i.__name__} needs prob, but prob are not provided")
                        else:
                            perf_metrics[i.__name__] = compute_metric(self.target, self.prob, metric=i, **dict_to_use)
                    else:
                        perf_metrics[i.__name__] = compute_metric(
                            self.target, self.predictions, metric=i, **dict_to_use
                        )
                if self.return_prop_true:
                    perf_metrics["proportion_1"] = (self.target == 1).mean()  # Add proportion of 1 label
            elif self.model_type == "multiclass":
                if self.predictions is None:
                    self.predictions = pd.Series([np.argmax(x) for x in self.prob], name="prob")
                for i, j in self.metrics.items():
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    if i.__name__ in [
                        "precision_score",
                        "recall_score",
                        "f1_score",
                        "fbeta_score",
                        "brier_score_loss",
                        "class_likelihood_ratios",
                        "dcg_score",
                        "jaccard_score",
                        "log_loss",
                        "matthews_corrcoef",
                        "ndcg_score",
                    ]:
                        warnings.warn(f"{i.__name__} is used for binary classification")
                    elif j == "prob":
                        if self.prob is None:
                            warnings.warn(f"{i.__name__} needs prob, but prob are not provided")
                        else:
                            perf_metrics[i.__name__] = compute_metric(
                                self.target, self.prob, metric=i, multi_class="ovr"
                            )
                    else:
                        perf_metrics[i.__name__] = compute_metric(
                            self.target, self.predictions, metric=i, **dict_to_use
                        )
            else:
                raise ValueError("Invalid model type.")
        # Metric if unsupervised approach
        else:
            # data quality
            if (cluster_labels is None) or (data_matrix is None):
                raise ValueError("Both cluster_labels and data_matrix must be not None")
            else:
                check_size(data_matrix, cluster_labels)
                data_matrix = convert_date_columns_to_seconds(data_matrix)
            if not isinstance(cluster_labels, pd.Series):
                cluster_labels = pd.Series(cluster_labels, name="cluster_labels")
            cluster_labels = convert_Int_series(cluster_labels)

            if cluster_labels.isna().any():
                condition = ~cluster_labels.isna()
                cluster_labels = cluster_labels[condition].reset_index(drop=True)
                data_matrix = data_matrix[condition].reset_index(drop=True)

            vals = cluster_labels.nunique()
            # uniform cluster value and type
            cluster_labels = convert_cluster_labels(cluster_labels, vals)

            if not isinstance(data_matrix, pd.DataFrame):
                data_matrix = pd.DataFrame(data_matrix)
            data_matrix = convert_Int_dataframe(data_matrix)
            if data_matrix.isna().any().any():
                if self.impute_nans:
                    valid_params = inspect.signature(cluster_imputing).parameters.keys()
                    dict_to_use = {k: v for k, v in self.__dict__.items() if k in valid_params}

                    self.data_matrix, self.cluster_labels = cluster_imputing(data_matrix, cluster_labels, **dict_to_use)
                else:
                    self.data_matrix = data_matrix
                    self.cluster_labels = cluster_labels
            else:
                self.data_matrix = data_matrix
                self.cluster_labels = cluster_labels

            categorical_cols = self.data_matrix.select_dtypes(exclude=["number"]).columns
            if self.new_metrics:
                data_matrix_dummies = self.data_matrix.copy()
                data_matrix_dummies = pd.get_dummies(data_matrix_dummies, columns=categorical_cols)
            self.data_matrix[categorical_cols] = self.data_matrix[categorical_cols].astype("category")
            # warning for classification clustering
            # compute metrics
            if vals != 1:
                for i in self.metrics:
                    dict_to_use = {
                        k: v for k, v in self.__dict__.items() if k in inspect.signature(i).parameters.keys()
                    }
                    try:
                        if i.__name__ != "classification_clustering":
                            metric = compute_unsupervised_metric(
                                data_matrix_dummies, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                        else:
                            metric = compute_unsupervised_metric(
                                self.data_matrix, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                    except Exception:
                        if not self.impute_nans:
                            if self.data_matrix.isna().any().any():
                                raise ValueError(
                                    f"\n An error occured while computing {i.__name__}, the reason could be impute_nans is set to False, try set it as True while initializating the class"
                                )
                        else:
                            raise ValueError(
                                f"\n{i.__name__} is not a valid additional metric for clustering monitoring"
                            )
            # Many metrics don't work well with a single cluster
            else:
                for i in self.metrics:
                    try:
                        if i.__name__ != "classification_clustering":
                            metric = compute_unsupervised_metric(
                                data_matrix_dummies, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                        else:
                            metric = compute_unsupervised_metric(
                                self.data_matrix, self.cluster_labels, i, **dict_to_use
                            )
                            perf_metrics[i.__name__] = metric
                    except Exception:
                        warnings.warn(
                            f"\n{i.__name__} is not a valid additional metric for clustering monitoring with a single cluster"
                        )
                        pass
        self.perf_metrics = perf_metrics
        return self.perf_metrics
