# iacovbr_icu_mv_public

## Description

This repository contains the codes used in a study that compared different data aggregations of Brazilian hospitals to predict Intensive Care Unit admission (ICU) and Mechanical Ventilation (MV) in patients with COVID-19. The machine learning algorithms trained were XGBoost, catboost, and lightGBM, which are considered state-of-the-art for structured data.

For each outcome, Jupyter Notebooks are divided according to the aggregation strategy (from strategies 1 to 8 described in the paper). There is a dropdown to choose a hospital in each notebook, and each notebook was run 14 times, once for each of the 14 hospitals.

All codes used MLflow libraries created by the laboratory to manage and monitor model executions. MLflow allows you to track experiments, record metrics, parameters, and model results, facilitating comparison between different modeling strategies.

This repository also includes the code for metadata analysis used to evaluate which characteristics of predictor distributions could be associated with more effective training strategies in each hospital.

## Requirements

- Python 3.10.0
- Libraries listed in requirements.txt

To install dependencies, run: pip install -r requirements.txt
