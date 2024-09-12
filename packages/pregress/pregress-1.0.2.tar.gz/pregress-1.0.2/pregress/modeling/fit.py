from .parse_formula import parse_formula
import statsmodels.api as sm
import pandas as pd

def fit(formula, data=None, method = "ols", dummies = True):
    """
    Fits a statistical model based on a specified formula and data.

    Parameters:
    - formula (str): A string representing the statistical formula (e.g., 'Y ~ X1 + X2 - X3').
    - data (DataFrame, optional): The dataset containing the variables specified in the formula.
    - method (str, optional): The method used for fitting the model. Defaults to 'ols' (Ordinary Least Squares).
                              Other methods can be implemented, such as logistic regression, random forest, etc.
    - dummies (bool, optional): A boolean indicating whether to automatically create dummy variables for categorical
                                predictors. Defaults to True.

    Returns:
    - model (statsmodels object): The fitted model object, which can be used for further analysis, such as 
                                  making predictions or evaluating model performance.

    Raises:
    - ValueError: If the input data is empty or the specified variables are not found in the data.

    Notes:
    - The function currently supports OLS (Ordinary Least Squares) regression. Additional methods like logistic 
      regression, random forest, and k-nearest neighbors can be added as needed.
    - The 'parse_formula' function is used to parse the formula and extract the response and predictor variables 
      from the dataset.
    - If 'dummies' is set to True, categorical variables in the predictors are converted into dummy/indicator 
      variables, with the first category dropped to avoid multicollinearity. Additionally, binary variables 
      (True/False) are converted to numeric (0/1) values.
    """
    
    Y_name, X_names, Y_out, X_out = parse_formula(formula, data)
    
    if method.lower() == "ols":
        if dummies:
            
            X_out = pd.get_dummies(X_out, drop_first=True)
            
            # Convert binary variables (True/False) to numeric (0/1)
            binary_columns = X_out.select_dtypes(include=['bool']).columns
            X_out[binary_columns] = X_out[binary_columns].astype(int)

        if X_out.empty:
            raise ValueError("The input data is empty or the specified variables are not found in the data.")

        model = sm.OLS(Y_out, X_out).fit()

#    if method.lower() == "logistic":
#    if method.lower() == "rf":
#    if method.lower() == "knn":
    return model
