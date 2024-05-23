# Module: Utils
# Author: Andre Batista <andrefmb@usp.br>
# License: MIT


# ---------------------------------------------------------------

# Helper functions

def compare(fn, list1, list2, padding=8):
    """
    a utility function intended to be used as a wrapper that simply prints
    the two lists before calling the relevant function
    the padding and copy stuff is for text alignment in ipython
    copy.copy ensures the ipython namespace isn't trampled by fix_list_lengths()
    if not using ipython, don't worry about this, it will work fine without
    """

    import copy
    print(" " * padding, list1)
    print(" " * padding, list2)

    list1 = copy.copy(list1)
    list2 = copy.copy(list2)

    return fn(list1, list2)


def fix_list_lengths(list1, list2, alert_if_same=False):
    """
    This function makes len(list1) == len(list2) -> True
    by adding 0s to the end of the shorter list
    (0s indicate nothing was detected)
    the list to be modified is copied before modification
    to preserve the integrity of the source data
    >>> fix_list_lengths([0,0,0,0,0], [0])
    ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])
    >>> fix_list_lengths([0], [0,0,0,0,0])
    ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])
    >>> fix_list_lengths([1], [1,1,1,1,1])
    ([1, 0, 0, 0, 0], [1, 1, 1, 1, 1])
    >>> fix_list_lengths([0, 1], [0,0,0,0,1])
    ([0, 1, 0, 0, 0], [0, 0, 0, 0, 1])
    >>> fix_list_lengths([1], [0], alert_if_same = True)
    The lists are already the same length
    ([1], [0])
    """

    import copy
    if len(list1) < len(list2):
        list1 = copy.copy(list1)
        for _ in range(len(list2) - len(list1)):
            list1.append(0)

    elif len(list1) > len(list2):
        list2 = copy.copy(list2)
        for _ in range(len(list1) - len(list2)):
            list2.append(0)

    elif alert_if_same == True:
        print("The lists are already the same length")

    return list1, list2


# ---------------------------------------------------------------

def safe_print(name, fn, *args, extra="", zerodevmsg=""):
    """
    This function tries to print a number, if that fails it doesn't stop the program
    """
    try:
        print("{} ({:.2f}) {}".format(name, fn(*args), extra))
    except ZeroDivisionError as e:
        if zerodevmsg is not "":
            print("{} cannot be printed: {}".format(name, zerodevmsg))
        else:
            print("{} cannot be printed: {}".format(name, e))
    except ValueError as e:
        print("{} cannot be printed: {}".format(name, e))


# ---------------------------------------------------------------

# Core binary classification functions

def true_positives(ground_truth, predicted):
    """
    This function returns the true positives as a list
    (also called the 'power')
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a == 1 and m == 1 else 0 for a, m in zip(ground_truth, predicted)]


tps = true_positives


def false_negatives(ground_truth, predicted):
    """
    This function returns the false negatives as a list
    (also called a 'Type 2 error')
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a == 1 and m == 0 else 0 for a, m in zip(ground_truth, predicted)]


fns = false_negatives


def false_positives(ground_truth, predicted):
    """
    This function returns the false positives as a list
    (also called a 'Type 1 error')
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a == 0 and m == 1 else 0 for a, m in zip(ground_truth, predicted)]


fps = false_positives


def true_negatives(ground_truth, predicted):
    """
    This function returns the true negatives as a list
    (also called "yeah, that was definitely nothing")
    """
    if not len(ground_truth) == len(predicted):
        ground_truth, predicted = fix_list_lengths(ground_truth, predicted)

    return [1 if a == 0 and m == 0 else 0 for a, m in zip(ground_truth, predicted)]


tns = true_negatives


# the following are the same as the above, but return an integer (not a list)

def true_positive(ground_truth, predicted):
    """
    This function measures the true positives as a value
    (also called the 'power')
    """
    return sum(true_positives(ground_truth, predicted))


tp = true_positive


def true_negative(ground_truth, predicted):
    """
    This function measures the true negatives as a value
    (also called "yeah, that was definitely nothing")
    """
    return sum(true_negatives(ground_truth, predicted))


tn = true_negative


def false_positive(ground_truth, predicted):
    """
    This function measures the false positives as a value
    (also called a 'Type 1 error')
    """
    return sum(false_positives(ground_truth, predicted))


fp = false_positive


def false_negative(ground_truth, predicted):
    """
    This function measures the false negatives as a value
    (also called a 'Type 2 error')
    """
    return sum(false_negatives(ground_truth, predicted))


fn = false_negative


# ---------------------------------------------------------------

# Measurement functions
# These are general functions that tell us about our data and results

def prevalence(ground_truth):
    """
    This function tells us what percentage of the dataset has a True (i.e. 1) state
    """
    return sum(ground_truth) / len(ground_truth)


def accuracy(ground_truth, predicted):
    """
    This function measures the accuracy rate
    """
    n_of_correct_classifications = (true_positive(ground_truth, predicted) +
                                    true_negative(ground_truth, predicted))

    return n_of_correct_classifications / len(ground_truth)


def error(ground_truth, predicted):
    """
    This function measures the error rate
    """
    n_of_incorrect_classifications = (false_positive(ground_truth, predicted) +
                                      false_negative(ground_truth, predicted))

    return n_of_incorrect_classifications / len(ground_truth)


# These functions give us rates of performance (ratios rather than values)
# This allows us to compare against other data sets of different sizes

def true_positive_rate(ground_truth, predicted):
    """
    This function measures the true positive rate
    (also called "recall", "sensitivity", or "probability of detection")
    """
    return true_positive(ground_truth, predicted) / sum(ground_truth)


tpr = true_positive_rate


def true_negative_rate(ground_truth, predicted):
    """
    This function measures the true negative rate
    (also called "specificity" or "ability to not see things that aren't there")
    note that the values of 'ground_truth' are inverted to compare against all negatives
    could also write as: (len(ground_truth) - sum(ground_truth))
    """
    return true_negative(ground_truth, predicted) / sum([1 if a == 0 else 0 for a in ground_truth])


tnr = true_negative_rate


def false_negative_rate(ground_truth, predicted):
    """
    This function measures the false negative rate
    (also called "miss rate")
    """
    return false_negative(ground_truth, predicted) / sum(ground_truth)


fnr = false_negative_rate


def false_positive_rate(ground_truth, predicted):
    """
    This function measures the false positive rate
    (also called "fall-out" or "rate of false alarm")
    note that the values of ground_truth are inverted to compare against all negatives
    could also write as: (len(ground_truth) - sum(ground_truth))
    """
    return false_positive(ground_truth, predicted) / sum([1 if a == 0 else 0 for a in ground_truth])


fpr = false_positive_rate


# These allow us to measure the predictor's tendancy toward accuracy (or not)
# In all four cases, 1 is perfect

def positive_predictive_value(ground_truth, predicted):
    """
    This function measures the positive predictive value
    (also called "precision" or "thanks for removing the cyst and not my brain")
    1 is perfect and means the system only detected what it should have.
    More than 1 means it detected more than it should have. < 1 is the inverse.
    note that this number can be greater than 1, thus the word 'value'
    """
    return (true_positive(ground_truth, predicted) /
            (true_positive(ground_truth, predicted) + false_positive(ground_truth, predicted)))


ppv = positive_predictive_value


def negative_predictive_value(ground_truth, predicted):
    """
    This function measures the negative predictive value
    (also called "that's not our son. Our son doesn't have fangs and a tail")
    1 is perfect and means the system only excluded what it should have.
    More than 1 means it excluded more than it should have. <1 is the inverse.
    note that this number can be greater than 1, thus the word 'value'
    """
    return (true_negative(ground_truth, predicted) /
            (true_negative(ground_truth, predicted) + false_negative(ground_truth, predicted)))


npv = negative_predictive_value


def false_discovery_rate(ground_truth, predicted):
    """
    This function measures the false disecovery rate
    (also called "whoops, sorry for the radiation and chemotherapy")
    """
    return (false_positive(ground_truth, predicted) /
            (true_positive(ground_truth, predicted) + false_positive(ground_truth, predicted)))


fdr = false_discovery_rate


def false_omission_rate(ground_truth, predicted):
    """
    This function measures the false omission rate
    (also called "I'm sure that fluffy bump we hit wasn't a bunny")
    """
    return (false_negative(ground_truth, predicted) /
            (true_negative(ground_truth, predicted) + false_negative(ground_truth, predicted)))


FOR = false_omission_rate
foR = false_omission_rate


# These functions measure the basis of the predictor

def positive_likelihood_ratio(ground_truth, predicted):
    """
    This function measures the positive likelihood ratio
    (also called " likelihood ratio for positive results")
    sensitivity / (1 - specificity)
    The bigger this number the better.
    """
    return (true_positive_rate(ground_truth, predicted) /
            (1 - true_negative_rate(ground_truth, predicted)))


plr = positive_likelihood_ratio


def negative_likelihood_ratio(ground_truth, predicted):
    """
    This function measures the negative likelihood ratio
    (also called " likelihood ratio for negative results")
    (1 - sensitivity) / specificity
    The smaller this number the better.
    """
    return ((1 - true_positive_rate(ground_truth, predicted)) /
            true_negative_rate(ground_truth, predicted))


nlr = negative_likelihood_ratio


def diagnostic_odds_ratio(ground_truth, predicted):
    """
    This function measures the diagnostic odds ratio
    (also called "detection_tendancy")
    Greater than 1 means the test is discriminating correctly.
    """
    return (positive_likelihood_ratio(ground_truth, predicted) /
            negative_likelihood_ratio(ground_truth, predicted))


dor = diagnostic_odds_ratio


# These functions I made up

def positive_unlikelihood_ratio(ground_truth, predicted):
    """
    This function measures the positive unlikelihood ratio
    (also called "")
    """
    return (false_positive_rate(ground_truth, predicted) /
            true_positive_rate(ground_truth, predicted))


def negative_unlikelihood_ratio(ground_truth, predicted):
    """
    This function measures the negative unlikelihood ratio
    (also called "")
    """
    return (false_negative_rate(ground_truth, predicted) /
            true_negative_rate(ground_truth, predicted))


def undiagnostic_odds_ratio(ground_truth, predicted):
    """
    This function measures the undiagnostic odds ratio
    (also called "")
    """
    return (negative_likelihood_ratio(ground_truth, predicted) /
            positive_likelihood_ratio(ground_truth, predicted))


def diagnostic_disodds_ratio(ground_truth, predicted):
    """
    This function measures the undiagnostic odds ratio
    (also called "")
    """
    return (positive_unlikelihood_ratio(ground_truth, predicted) /
            negative_unlikelihood_ratio(ground_truth, predicted))


def undiagnostic_disodds_ratio(ground_truth, predicted):
    """
    This function measures the undiagnostic disodds ratio
    (also called "")
    """
    return (negative_unlikelihood_ratio(ground_truth, predicted) /
            positive_unlikelihood_ratio(ground_truth, predicted))


# These are F score functions

def f1_score(ground_truth, predicted):
    """
    This function measures the f1 score
    (also called "balanced f score")
    """
    return (2 / ((1 / true_positive_rate(ground_truth, predicted)) +
                 (1 / positive_predictive_value(ground_truth, predicted))))


def f_score(ground_truth, predicted, beta=.5):
    """
    This function returns the f beta score
    (also called "unbalanced effing score")
    https://en.wikipedia.org/wiki/F1_score
    beta measures how much the true_positive_rate is weighted by
    increasing and decreasing the influence of false negatives
    high beta means true_positive_rate is more important to you than the
    false_negative_rate
    denominator broken up into 3 parts for ease of reading
    """
    numer = (1 + beta ** 2) * true_positive_rate(ground_truth, predicted)

    denom1 = ((1 + beta ** 2) * true_positive_rate(ground_truth, predicted))
    denom2 = ((beta ** 2) * false_negative_rate(ground_truth, predicted))
    denom3 = false_positive_rate(ground_truth, predicted)
    denoms = [denom1, denom2, denom3]
    return numer / sum([denom for denom in denoms if denom is not None])
        #### Calibration Metrics


# A statistical goodness- of-fit test to evaluate the difference between the predicted and observed event rates. The Hosmer-Lemeshow C test statistic is defined with an equal number of predicted scores divided into 10 groups. A p-value of 1 indicates the model is well-calibrated.


def hosmer_lemeshow(y_true, y_score):
    """
    Calculate the Hosmer Lemeshow to assess whether
    or not the observed event rates match expected
    event rates.
    Assume that there are 10 groups:
    HL = \\sum_{g=1}^G \\frac{(O_{1g} - E_{1g})^2}{N_g \\pi_g (1- \\pi_g)}
    """
    import numpy as np
    import pandas as pd

    from scipy.stats import chi2

    try:
        n_grp = 10  # number of groups
        if type(y_true) is not np.ndarray:
            y_true = y_true.values.ravel()

        # create the dataframe
        df = pd.DataFrame({"score": y_score, "target": y_true})

        # sort the values
        df = df.sort_values("score")
        # shift the score a bit
        df["score"] = np.clip(df["score"], 1e-8, 1 - 1e-8)
        df["rank"] = list(range(df.shape[0]))
        # cut them into 10 bins
        df["score_decile"] = pd.qcut(df["rank"], n_grp, duplicates="raise")
        # sum up based on each decile
        obsPos = df["target"].groupby(df.score_decile).sum()
        obsNeg = df["target"].groupby(df.score_decile).count() - obsPos
        exPos = df["score"].groupby(df.score_decile).sum()
        exNeg = df["score"].groupby(df.score_decile).count() - exPos
        hl = (((obsPos - exPos) ** 2 / exPos) + ((obsNeg - exNeg) ** 2 / exNeg)).sum()

        # https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
        # Re: p-value, higher the better Goodness-of-Fit
        p_value = 1 - chi2.cdf(hl, n_grp - 2)

        return p_value
    except:
        return 0


# A statistical test to evaluate whether the Brier score is extreme. Spiegelhalter [24] observed that the expectation and variance of the Brier score could be cal- culated under the null hypothesis that the true unknown probability of the event was equivalent to the estimated probability. Thus, one could determine whether it was dif- ferent from the observed prevalence. A p-value of 1 denotes a well-calibrated model.


def spiegelhalter(y_true, y_score):
    import numpy as np
    from scipy.stats import norm

    try:
        if type(y_true) is not np.ndarray:
            y_true = y_true.values.ravel()
        top = np.sum((y_true - y_score) * (1 - 2 * y_score))
        bot = np.sum((1 - 2 * y_score) ** 2 * y_score * (1 - y_score))
        sh = top / np.sqrt(bot)

        # https://en.wikipedia.org/wiki/Z-test
        # Two-tailed test
        # Re: p-value, higher the better Goodness-of-Fit
        p_value = norm.sf(np.abs(sh)) * 2

        return p_value
    except:
        return 0


# ScaledBrierscore A standardized,prevalent-independent version of the Brier score with the range between 0 and 1. The score accounts for the mean prevalence of the event by dividing the Brier score by the “maximum" Brier score achieved by simply predicting the prevalence of the event. A perfect model achieves a scaled Brier score of 1


def scaled_brier_score(y_true, y_score):
    import numpy as np
    from sklearn.metrics import brier_score_loss

    try:
        if type(y_true) is not np.ndarray:
            y_true = y_true.values.ravel()
        brier = brier_score_loss(y_true, y_score, pos_label=1)
        # calculate the mean of the probability
        p = np.mean(y_true)
        brier_scaled = 1 - brier / (p * (1 - p))
        return brier_scaled
    except:
        return 0


# ---------------------------------------------------------------

def binary_classification_metrics(ground_truth, prediction, prediction_proba, show_results=True):
    """
    This function prints a selection of the most common binary classification
    measurements
    safe_print is a function that prevents against ZeroDivisionErrors


    """

    from sklearn.metrics import (
        roc_curve,
        auc,
    )

    import pandas as pd
    import matplotlib.pyplot as plt
    from IPython.display import display

    from sklearn.metrics import confusion_matrix, precision_recall_curve, average_precision_score
    from sklearn.calibration import calibration_curve

    import warnings
    warnings.filterwarnings("ignore")

    fprate, tprate, thresholds = roc_curve(ground_truth, prediction_proba, pos_label=1)

    monitor = pd.DataFrame(
        [
            ["Ground Truth Prevalence", ". . . ", prevalence(ground_truth)],
            ["Test set Prevalence", ". . . ", prevalence(prediction)],
            ["True positive rate (recall)", ". . . ", tpr(ground_truth, prediction)],
            ["False positive rate", ". . . ", fpr(ground_truth, prediction)],
            ["Positive predictive value (precision)", ". . . ", ppv(ground_truth, prediction)],
            ["True negative rate (specificity)", ". . . ", tnr(ground_truth, prediction)],
            ["False negative rate", ". . . ", fnr(ground_truth, prediction)],
            ["Negative predictive value", ". . . ", npv(ground_truth, prediction)],
            ["Positive likelihood ratio (bigger is better)", ". . . ", plr(ground_truth, prediction)],
            ["Negative likelihood ratio (smaller is better)", ". . . ", nlr(ground_truth, prediction)],
            ["Diagnostic odds ratio", ". . . ", dor(ground_truth, prediction)],
            ["Accuracy", ". . . ", accuracy(ground_truth, prediction)],
            ["F1 score", ". . . ", f1_score(ground_truth, prediction)],
            ["Accuracy", ". . . ", accuracy(ground_truth, prediction)],
            ["ROC AUC", ". . . ", auc(fprate, tprate)],
            ["ROC AUC (95% CI)", ". . . ", ["{0:0.2f}".format(i) for i in AUC_CI(ground_truth, prediction_proba._values)]],
            ["Scaled Brier Score", ". . . ", scaled_brier_score(ground_truth, prediction_proba)],
            ["Hosmer_Lemeshow p-value", ". . . ", hosmer_lemeshow(ground_truth, prediction_proba)],
            ["Spiegelhalter p-value", ". . . ", spiegelhalter(ground_truth, prediction_proba)],

        ],
        columns=["", " ", "   "],
    ).set_index("")
    if show_results:
        display(monitor)

        fig = plt.figure(figsize=(15, 20))
        fig.tight_layout(pad=3.0)
        # plt.subplots_adjust(top=0.99, right=0.99)
        ### MATRIZ DE CONFUSAO
        ax_mc = plt.subplot2grid((14, 2), (0, 0), rowspan=3, colspan=1)
        ### ROC CURVE
        ax_roc = plt.subplot2grid((14, 2), (4, 0), rowspan=3, colspan=1)
        ### PRECISION RECALL
        ax_pr = plt.subplot2grid((14, 2), (4, 1), rowspan=3, colspan=1)
        ### CALIBRACAO
        ax_cal = plt.subplot2grid((14, 2), (8, 0), rowspan=3, colspan=1)

        lw = 2
        ax_roc.plot(fprate, tprate,
                    lw=2, label='ROC curve (area = %0.2f)' % auc(fprate, tprate))
        ax_roc.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        ax_roc.set_xlim([0.0, 1.0])
        ax_roc.set_ylim([0.0, 1.05])
        ax_roc.set_xlabel('False Positive Rate')
        ax_roc.set_ylabel('True Positive Rate')
        ax_roc.set_title('Receiver operating characteristic')
        ax_roc.legend(loc="lower right")
        # ax_roc.plot()

        CM = confusion_matrix(ground_truth, prediction)

        # matriz de confusao
        labels = ["True Neg", "False Pos", "False Neg", "True Pos"]
        categories = ["False", "True"]
        make_confusion_matrix(
            CM,
            group_names=labels,
            categories=categories,
            cmap="binary",
            ax=ax_mc,
            title="Confusion Matrix",
        )

        ### GRAFICO DE CALIBRACAO
        ##Fernando Fernandes - 2024-02-12 - Removido o parametro normalize (deprecated)
        fraction_of_positives, mean_predicted_value = calibration_curve(
            ground_truth, prediction_proba, n_bins=10
        )

        ax_cal.plot(
            mean_predicted_value,
            fraction_of_positives,
            "s-",
            label="Scaled Brier %0.2f" % scaled_brier_score(ground_truth, prediction_proba)
        )

        ax_cal.set_ylabel("Fraction of positives")
        ax_cal.set_ylim([-0.05, 1.05])
        ax_cal.legend(loc="lower right")
        ax_cal.set_title("Calibration plot")
        ax_cal.set_xlabel("Mean predicted value")

        ax_cal.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
        # ax_cal.plot()

        # precision-recall curve
        precision, recall, thresholds = precision_recall_curve(
            ground_truth, prediction_proba, pos_label=1
        )

        # AUC score that summarizes the precision recall curve
        avg_precision = average_precision_score(ground_truth, prediction_proba)
        # figPR, axPR = plt.subplots()
        label = "Precision Recall AUC: {:.2f}".format(avg_precision)
        ax_pr.plot(recall, precision, lw=2, label=label)
        ax_pr.set_xlabel("Recall")
        ax_pr.set_ylabel("Precision")
        ax_pr.set_title("Precision Recall Curve")
        ax_pr.legend()
        # ax_pr.plot()

        plt.show()

        import seaborn as sns

        res_0 = []
        res_1 = []

        for i, p in enumerate(prediction_proba):
            if ground_truth.iloc[i] > 0:
                res_1.append(p)
            else:
                res_0.append(p)

        normalized_res_0 = []
        for i in res_0:
            normalized_res_0.append(remap(i, 0, 1, -2, 2))
        normalized_res_1 = []

        for i in res_1:
            normalized_res_1.append(remap(i, 0, 1, -2, 2))
        sns.distplot(normalized_res_0, hist=False, kde_kws={"shade": True}, color='b', label='Class 0')
        sns.distplot(normalized_res_1, hist=False, kde_kws={"shade": True}, color='r', label='Class 1')
        plt.xlabel('risk scores')
        plt.ylabel('Density')
        plt.legend()
        plt.show()

    return monitor


def make_confusion_matrix(
        cf,
        group_names=None,
        categories="auto",
        count=True,
        percent=True,
        cbar=True,
        xyticks=True,
        xyplotlabels=True,
        sum_stats=False,
        figsize=None,
        cmap="Blues",
        title=None,
        ax=None,
):
    """
    This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.
    Arguments
    ---------
    cf:            confusion matrix to be passed in
    group_names:   List of strings that represent the labels row by row to be shown in each square.
    categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'
    count:         If True, show the raw number in the confusion matrix. Default is True.
    cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                   Default is True.
    xyticks:       If True, show x and y ticks. Default is True.
    xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.
    sum_stats:     If True, display summary statistics below the figure. Default is True.
    figsize:       Tuple representing the figure size. Default will be the matplotlib rcParams value.
    cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                   See http://matplotlib.org/examples/color/colormaps_reference.html

    title:         Title for the heatmap. Default is None.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    # CODE TO GENERATE TEXT INSIDE EACH SQUARE
    blanks = ["" for i in range(cf.size)]

    if group_names and len(group_names) == cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if percent:
        group_percentages = [
            "{0:.2%}".format(value) for value in cf.flatten() / np.sum(cf)
        ]
    else:
        group_percentages = blanks

    box_labels = [
        f"{v1}{v2}{v3}".strip()
        for v1, v2, v3 in zip(group_labels, group_counts, group_percentages)
    ]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0], cf.shape[1])

    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
    if sum_stats:
        # Accuracy is sum of diagonal divided by total observations
        accuracy = np.trace(cf) / float(np.sum(cf))

        # if it is a binary confusion matrix, show some more stats
        if len(cf) == 2:
            # Metrics for Binary Confusion Matrices
            precision = cf[1, 1] / sum(cf[:, 1])
            recall = cf[1, 1] / sum(cf[1, :])
            f1_score = 2 * precision * recall / (precision + recall)
            stats_text = "\n\nAccuracy={:0.3f}\nPrecision={:0.3f}\nRecall={:0.3f}\nF1 Score={:0.3f}".format(
                accuracy, precision, recall, f1_score
            )
        else:
            stats_text = "\n\nAccuracy={:0.3f}".format(accuracy)
    else:
        stats_text = ""

    # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
    if figsize == None:
        # Get default figure size if not set
        figsize = plt.rcParams.get("figure.figsize")

    if xyticks == False:
        # Do not show categories if xyticks is False
        categories = False

    # MAKE THE HEATMAP VISUALIZATION
    if ax is None:
        plt.figure(figsize=figsize)
        sns.heatmap(
            cf,
            annot=box_labels,
            fmt="",
            cmap=cmap,
            cbar=cbar,
            xticklabels=categories,
            yticklabels=categories,
        )
        if xyplotlabels:
            plt.ylabel("True label")
            plt.xlabel("Predicted label" + stats_text)
        else:
            plt.xlabel(stats_text)
        if title:
            plt.title(title)
    else:
        sns.heatmap(
            cf,
            annot=box_labels,
            fmt="",
            cmap=cmap,
            cbar=cbar,
            xticklabels=categories,
            yticklabels=categories,
            ax=ax,
        )
        if xyplotlabels:
            ax.set_ylabel("True label")
            ax.set_xlabel("Predicted label" + stats_text)
        if title:
            ax.set_title(title)


# ------------------------------------------------------------


### PARA CALCULO DO INTERVALO DE CONFIANCA DE UMA CURVA ROC


def AUC_CI(y_true, predicted_proba, alpha=0.95):
    import numpy as np
    from scipy import stats

    auc, auc_cov = delong_roc_variance(y_true, predicted_proba)

    auc_std = np.sqrt(auc_cov)
    lower_upper_q = np.abs(np.array([0, 1]) - (1 - alpha) / 2)

    ci = stats.norm.ppf(lower_upper_q, loc=auc, scale=auc_std)

    ci[ci > 1] = 1
    # print("AUC [just to confirm]:", auc)
    # print("AUC COV:", auc_cov)
    return ci


# AUC comparison adapted from
# https://github.com/Netflix/vmaf/
def compute_midrank(x):
    """Computes midranks.
    Args:
       x - a 1D numpy array
    Returns:
       array of midranks
    """

    import numpy as np

    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1)
        i = j
    T2 = np.empty(N, dtype=float)
    # Note(kazeevn) +1 is due to Python using 0-based indexing
    # instead of 1-based in the AUC formula in the paper
    T2[J] = T + 1
    return T2


def compute_midrank_weight(x, sample_weight):
    """Computes midranks.
    Args:
       x - a 1D numpy array
    Returns:
       array of midranks
    """

    import numpy as np

    J = np.argsort(x)
    Z = x[J]
    cumulative_weight = np.cumsum(sample_weight[J])
    N = len(x)
    T = np.zeros(N, dtype=np.float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = cumulative_weight[i:j].mean()
        i = j
    T2 = np.empty(N, dtype=np.float)
    T2[J] = T
    return T2


def fastDeLong(predictions_sorted_transposed, label_1_count, sample_weight):
    if sample_weight is None:
        return fastDeLong_no_weights(predictions_sorted_transposed, label_1_count)
    else:
        return fastDeLong_weights(
            predictions_sorted_transposed, label_1_count, sample_weight
        )


def fastDeLong_weights(predictions_sorted_transposed, label_1_count, sample_weight):
    """
    The fast version of DeLong's method for computing the covariance of
    unadjusted AUC.
    Args:
       predictions_sorted_transposed: a 2D numpy.array[n_classifiers, n_examples]
          sorted such as the examples with label "1" are first
    Returns:
       (AUC value, DeLong covariance)
    Reference:
     @article{sun2014fast,
       title={Fast Implementation of DeLong's Algorithm for
              Comparing the Areas Under Correlated Receiver Oerating Characteristic Curves},
       author={Xu Sun and Weichao Xu},
       journal={IEEE Signal Processing Letters},
       volume={21},
       number={11},
       pages={1389--1393},
       year={2014},
       publisher={IEEE}
     }
    """

    import numpy as np

    # Short variables are named as they are in the paper
    m = label_1_count
    n = predictions_sorted_transposed.shape[1] - m
    positive_examples = predictions_sorted_transposed[:, :m]
    negative_examples = predictions_sorted_transposed[:, m:]
    k = predictions_sorted_transposed.shape[0]

    tx = np.empty([k, m], dtype=float)
    ty = np.empty([k, n], dtype=float)
    tz = np.empty([k, m + n], dtype=float)
    for r in range(k):
        tx[r, :] = compute_midrank_weight(positive_examples[r, :], sample_weight[:m])
        ty[r, :] = compute_midrank_weight(negative_examples[r, :], sample_weight[m:])
        tz[r, :] = compute_midrank_weight(
            predictions_sorted_transposed[r, :], sample_weight
        )
    total_positive_weights = sample_weight[:m].sum()
    total_negative_weights = sample_weight[m:].sum()
    pair_weights = np.dot(sample_weight[:m, np.newaxis], sample_weight[np.newaxis, m:])
    total_pair_weights = pair_weights.sum()
    aucs = (sample_weight[:m] * (tz[:, :m] - tx)).sum(axis=1) / total_pair_weights
    v01 = (tz[:, :m] - tx[:, :]) / total_negative_weights
    v10 = 1.0 - (tz[:, m:] - ty[:, :]) / total_positive_weights
    sx = np.cov(v01)
    sy = np.cov(v10)
    delongcov = sx / m + sy / n
    return aucs, delongcov


def fastDeLong_no_weights(predictions_sorted_transposed, label_1_count):
    """
    The fast version of DeLong's method for computing the covariance of
    unadjusted AUC.
    Args:
       predictions_sorted_transposed: a 2D numpy.array[n_classifiers, n_examples]
          sorted such as the examples with label "1" are first
    Returns:
       (AUC value, DeLong covariance)
    Reference:
     @article{sun2014fast,
       title={Fast Implementation of DeLong's Algorithm for
              Comparing the Areas Under Correlated Receiver Oerating
              Characteristic Curves},
       author={Xu Sun and Weichao Xu},
       journal={IEEE Signal Processing Letters},
       volume={21},
       number={11},
       pages={1389--1393},
       year={2014},
       publisher={IEEE}
     }
    """

    import numpy as np

    # Short variables are named as they are in the paper
    m = label_1_count
    n = predictions_sorted_transposed.shape[1] - m
    positive_examples = predictions_sorted_transposed[:, :m]
    negative_examples = predictions_sorted_transposed[:, m:]
    k = predictions_sorted_transposed.shape[0]

    tx = np.empty([k, m], dtype=float)
    ty = np.empty([k, n], dtype=float)
    tz = np.empty([k, m + n], dtype=float)
    for r in range(k):
        tx[r, :] = compute_midrank(positive_examples[r, :])
        ty[r, :] = compute_midrank(negative_examples[r, :])
        tz[r, :] = compute_midrank(predictions_sorted_transposed[r, :])
    aucs = tz[:, :m].sum(axis=1) / m / n - float(m + 1.0) / 2.0 / n
    v01 = (tz[:, :m] - tx[:, :]) / n
    v10 = 1.0 - (tz[:, m:] - ty[:, :]) / m
    sx = np.cov(v01)
    sy = np.cov(v10)
    delongcov = sx / m + sy / n
    return aucs, delongcov


def calc_pvalue(aucs, sigma):
    """Computes log(10) of p-values.
    Args:
       aucs: 1D array of AUCs
       sigma: AUC DeLong covariances
    Returns:
       log10(pvalue)
    """

    import numpy as np
    import scipy.stats

    l = np.array([[1, -1]])
    z = np.abs(np.diff(aucs)) / np.sqrt(np.dot(np.dot(l, sigma), l.T))
    return np.log10(2) + scipy.stats.norm.logsf(z, loc=0, scale=1) / np.log(10)


def compute_ground_truth_statistics(ground_truth, sample_weight):
    import numpy as np

    assert np.array_equal(np.unique(ground_truth), [0, 1])
    order = (-ground_truth).argsort()
    label_1_count = int(ground_truth.sum())
    if sample_weight is None:
        ordered_sample_weight = None
    else:
        ordered_sample_weight = sample_weight[order]

    return order, label_1_count, ordered_sample_weight


def delong_roc_variance(ground_truth, predictions, sample_weight=None):
    """
    Computes ROC AUC variance for a single set of predictions
    Args:
       ground_truth: np.array of 0 and 1
       predictions: np.array of floats of the probability of being class 1
    """

    import numpy as np
    order, label_1_count, ordered_sample_weight = compute_ground_truth_statistics(
        ground_truth, sample_weight
    )
    predictions_sorted_transposed = predictions[np.newaxis, order]
    aucs, delongcov = fastDeLong(
        predictions_sorted_transposed, label_1_count, ordered_sample_weight
    )
    assert (
            len(aucs) == 1
    ), "There is a bug in the code, please forward this to the developers"
    return aucs[0], delongcov


# -------------------------------------------------------------------------


def run_hyperopt_classification(
        model_name,
        model_space,
        x_train,
        y_train,
        scoring="f1",
        cv=3,
        max_evals=20,
        verbose=False,
        persistIterations=True,
):
    print("LABDAPS --- Running Hyperopt Bayesian Optimization")
    print("reloaded")

    import pandas as pd
    import time
    import datetime
    from hyperopt import fmin, tpe, Trials, space_eval
    from sklearn.model_selection import cross_val_score

    def objective(space):
        ### MODEL SELECTION

        if model_name == "lr":
            # logistic regression
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(**space)

        elif model_name == "rf":
            # print("Setting model as RandomForestClassifier")
            from sklearn.ensemble import RandomForestClassifier

            model = RandomForestClassifier(**space, n_jobs=-1)
            if verbose:
                print("Hyperparameters: ", space)

        elif model_name == "xgb":
            # print("Setting model as XGBClassifier")
            from xgboost import XGBClassifier

            model = XGBClassifier(**space, objective="binary:logistic", nthread=-1)
            if verbose:
                print("Hyperparameters: ", space)

        elif model_name == "dt":
            # print("Setting model as DecisionTreeClassifier")
            from sklearn.tree import DecisionTreeClassifier

            model = DecisionTreeClassifier(**space)
            if verbose:
                print("Hyperparameters: ", space)

        elif model_name == "catboost":
            # print("Setting model as CatBoost")
            from catboost import CatBoostClassifier

            model = CatBoostClassifier(**space)
            if verbose:
                print("Hyperparameters: ", space)

        elif model_name == "extratrees":
            # print("Setting model as CatBoost")
            from sklearn.ensemble import ExtraTreesClassifier

            model = ExtraTreesClassifier(**space, n_jobs=-1)
            if verbose:
                print("Hyperparameters: ", space)


        elif model_name == "svc":
            from sklearn.svm import SVC

            model = SVC(**space)
            if verbose:
                print("Hyperparameters: ", space)

        elif model_name == "ann":
            # print("Setting model as ANN")
            from sklearn import neural_network

            model = neural_network.MLPClassifier(**space)
            if verbose:
                print("Hyperparameters: ", space)

        elif model_name == "lgb":
            import lightgbm as lgb

            model = lgb.LGBMClassifier(**space, n_jobs=-1, random_state=42)

            if verbose:
                print("Hyperparameters: ", space)

        elif model_name == "knn":
            from sklearn.neighbors import KNeighborsClassifier

            model = KNeighborsClassifier(**space)

            if verbose:
                print("Hyperparameters: ", space)

        else:
            # print("ERRO: Especifique um nome valido para model_name: rf, xgb, dt ou catboost")
            raise Exception(
                "Invalid model_name - Please specify one of the supported model_name: rf, xgb, ann, dt, svc, lgr, knn or catboost"
            )
        score = cross_val_score(
            model, x_train, y_train, cv=3, scoring=scoring, verbose=False, n_jobs=-1
        ).mean()
        score = 1 - score  ## ajusta para a funcao de minimizacao.

        return score

    start = time.time()
    trials = Trials()
    best = fmin(
        objective,
        space=model_space,
        algo=tpe.suggest,
        max_evals=max_evals,
        trials=trials,
    )

    if persistIterations:
        # Save the hyperparameter at each iteration to a csv file
        param_values = [x["misc"]["vals"] for x in trials.trials]
        param_values = [
            {key: value for key in x for value in x[key]} for x in param_values
        ]
        param_values = [space_eval(model_space, x) for x in param_values]

        param_df = pd.DataFrame(param_values)
        param_df[scoring] = [1 - x for x in trials.losses()]
        param_df.index.name = "Iteration"
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d-%H:%M")
        param_df.to_csv(f"Hyperopt_{model_name}_{st}.csv")
        print(f"Arquivo Hyperopt_{model_name}_{st}.csv gerado com sucesso.")

    print(
        f"Hyperopt search took %.2f seconds for {max_evals} candidates"
        % ((time.time() - start))
    )
    # print(-best_score, best)
    print("** Best Hyperparameters are: **")
    print(space_eval(model_space, best))


# -----------------------------------------------------------------


def get_all_column_names(df):
    return df.columns.values.tolist()


def count_distinct_values_column(df, colname):
    import pandas as pd
    return pd.DataFrame(df[colname].value_counts(dropna=False)).rename(
        columns={0: "Count"}
    )


def count_null_per_column(df):
    """Missing value count per column grouped by column name"""
    import pandas as pd
    return pd.DataFrame(df.isnull().sum()).rename(columns={0: "# of Nulls"})


def unique_values_per_column(df):
    import pandas as pd
    unique_counts = {}
    for idx in df.columns.values:
        # cnt=len(df[idx].unique())
        cnt = df[idx].nunique()
        unique_counts[idx] = cnt
    unique_ctr = pd.DataFrame([unique_counts]).T
    unique_ctr_2 = unique_ctr.rename(columns={0: "# Unique Values"})
    return unique_ctr_2


def particular_values_per_column(df, values):
    import pandas as pd
    import numpy as np
    counts = {}
    for idx in df.columns.values:
        cnt = np.sum(df[idx].isin(values).values)
        counts[idx] = cnt
    ctr = pd.DataFrame([counts]).T
    ctr_2 = ctr.rename(columns={0: "# Values as %s" % values})
    return ctr_2


def get_column_datatypes(df):
    import pandas as pd
    dtype = {}
    for idx in df.columns.values:
        dt = df[idx].dtype
        dtype[idx] = dt
    ctr = pd.DataFrame([dtype]).T
    ctr_2 = ctr.rename(columns={0: "datatype"})
    return ctr_2


def column_summaries(df):
    import pandas as pd

    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    particular_ctr = particular_values_per_column(df, [0])
    unique_ctr = unique_values_per_column(df)
    statistical_summary = df.describe().T
    datatypes = get_column_datatypes(df)
    
    #Adicionado parâmetro para numeric_only para evitar erro ao montar a tabela - 2024-02-12 - Fernando
    skewed = pd.DataFrame(df.skew(numeric_only=True)).rename(columns={0: "skew"})
    mis_val_table = pd.concat(
        [
            mis_val,
            mis_val_percent,
            unique_ctr,
            particular_ctr,
            datatypes,
            skewed,
            statistical_summary,
        ],
        axis=1,
    )
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: "Missing Values", 1: "% missing of Total Values"}
    )
    return mis_val_table_ren_columns


def filter_dataframe(df, filter_columns):
    df_filtered = df
    for feature in filter_columns:
        values = filter_columns[feature]
        if len(values) == 1:
            df_filtered = df_filtered[df_filtered[feature] == values[0]]
        elif len(values) == 2:
            df_filtered = df_filtered[
                (df_filtered[feature] >= values[0])
                & (df_filtered[feature] <= values[1])
                ]
    return df_filtered


def filter_dataframe_percentile(df, filter_columns):
    df_filtered = df
    for feature in filter_columns:
        quantiles = filter_columns[feature]
        values = df[feature].quantile(quantiles).values
        if len(values) == 1:
            # if only one value present assume upper quantile
            df_filtered = df_filtered[df_filtered[feature] <= values[0]]
        elif len(values) == 2:
            df_filtered = df_filtered[
                (df_filtered[feature] >= values[0])
                & (df_filtered[feature] <= values[1])
                ]
    return df_filtered


def detect_nan_columns(df):
    import numpy as np
    columns = df.columns.values.tolist()
    for colname in columns:
        if np.sum(np.isnan(df[colname])) > 0:
            print(colname)


def label_encode_field(df, df_test, field):
    from sklearn.preprocessing import LabelEncoder
    df[field] = df[field].fillna("-1")
    df_test[field] = df_test[field].fillna("-1")
    brand_df = df[field].append(df_test[field])
    brand_df.fillna("-1")
    label_encoder = LabelEncoder()
    encoder = label_encoder.fit(brand_df.values)
    encoded_t = encoder.transform(df_test[field].fillna("-1").values)
    df_test[field + "_transformed"] = encoded_t
    encoded_df = encoder.transform(df[field].fillna("-1").values)
    df[field + "_transformed"] = encoded_df


# -----------------------------------------------


def remap(x, oMin, oMax, nMin, nMax):
    # range check
    if oMin == oMax:
        print("Warning: Zero input range")
        return None

    if nMin == nMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin:
        reverseOutput = True

    portion = (x - oldMin) * (newMax - newMin) / (oldMax - oldMin)
    if reverseInput:
        portion = (oldMax - x) * (newMax - newMin) / (oldMax - oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result
