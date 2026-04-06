# Validation Metrics Guide

## Classification Metrics
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
- ROC AUC (for probability-based binary models when available)

## Regression Metrics
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R2 Score

## KNN Notes
- KNN Classification uses neighborhood voting
- KNN Regression uses neighborhood averaging
- Scaling matters a lot for KNN and SVM, so StandardScaler is included
