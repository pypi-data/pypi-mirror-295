import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.preprocessing import (
    LabelEncoder,
    OneHotEncoder,
    StandardScaler,
    RobustScaler,
)
from scipy import stats
from scipy.stats import skew, kurtosis
import warnings

warnings.filterwarnings("ignore")

path = input("Please enter the path of your csv file: ")

df = pd.read_csv(path)

class Inspection:
    """
    Inspection class used to inspect and summarize key statistics and information about a given DataFrame.
    The Inspection class provides detailed insights into the DataFrame's size, shape, dimensions,
    column types, missing and duplicated values, numerical and categorical columns, skewness, and
    kurtosis of numerical data.

    Attributes:
    -----------
    DataFrame

    Methods:
    --------
    __init__(df):
        Initializes the Inspection class with a DataFrame.

    inspect():
        Provides a detailed analysis of the DataFrame including size, shape, dimensions, column details,
        data types, missing and duplicated values, and summary statistics of numerical columns,
        including skewness and kurtosis.

    Example:
    --------
    >>> import pandas as pd
    >>> from scipy.stats import skew, kurtosis

    >>> # Sample DataFrame creation
    >>> data = {
    ...     'A': [1, 2, 3, 4, 5],
    ...     'B': [2.5, 3.6, 8.9, 7.3, 1.2],
    ...     'C': ['X', 'Y', 'Z', 'X', 'Y'],
    ...     'D': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'])
    ... }
    >>> df = pd.DataFrame(data)

    >>> # Initialize the Inspection class
    >>> inspection = Inspection(df)

    >>> # Perform inspection
    >>> inspection.inspect()

    Output:
    --------
    Processing column for calculating skewness: A
    Skewness of 'A': 0.0
    'A' is Approximately Symmetric.

    Processing column for kurtosis calculation: A
    Kurtosis of 'A': -1.2
    'A' is Platykurtic (light tails of outliers).

    ...
    (other outputs summarizing the DataFrame)
    ...
    """

    def __init__(df):
        """
        Initializes the Inspection class with a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to be inspected.

        Returns:
        --------
        None
        """
        df = df

    def inspect():
        """
        Provides a detailed analysis of the DataFrame, including size, shape, dimensions, column details,
        data types, missing and duplicated values, and summary statistics of numerical columns, including
        skewness and kurtosis.

        Parameters:
        -----------
        None

        Returns:
        --------
        Detailed report of the Dataframe

        The method prints out the following information:
        - Total number of elements in the DataFrame
        - Shape of the DataFrame
        - Number of dimensions of the DataFrame
        - Basic information about the DataFrame (using `info()`)
        - Statistical summary (using `describe()`)
        - Names and count of columns
        - Data types of the columns
        - Number and percentage of duplicated values
        - Number and percentage of missing values
        - Summary of numerical and categorical columns
        - Correlation matrix of numerical columns
        - Skewness and kurtosis calculations for numerical columns

        """

        size = df.size
        shape = df.shape
        dimentions = df.ndim
        info = df.info()
        summary = df.describe()
        columns = df.columns
        n_col = len(columns)
        types = df.dtypes
        duplicated = df.duplicated().sum()
        p_dup = duplicated / (len(df) * 100)
        missing = df.isnull().sum()
        p_miss = missing / (len(df) * 100)
        numeric = df.select_dtypes(include=["int64", "float64"])
        n_num = len(numeric)
        categoical = df.select_dtypes(exclude=["int64", "float64"])
        n_cat = len(categoical)
        datetime = df.select_dtypes(include=["datetime64"])
        corr = df.corr(numeric_only=True)

        for col in numeric.columns:
            print(f"\nProcessing column for calculating skewness: {col}")

            skewness_value = skew(
                numeric[col].dropna()
            )  # Dropping NaN to avoid skew calculation issues
            print(f"Skewness of '{col}': {skewness_value}")

            if skewness_value > 1:
                print(f"'{col}' is Highly Positively Skewed(Right Skewed).")
            elif 0.5 < skewness_value <= 1:
                print(f"'{col}' is Moderately Positively Skewed.")
            elif -0.5 <= skewness_value <= 0.5:
                print(f"'{col}' is Approximately Symmetric.")
            elif -1 <= skewness_value < -0.5:
                print(f"'{col}' is Moderately Negatively Skewed(Left Skewed).")
            else:
                print(f"'{col}' is Highly Negatively Skewed.")

        for col in numeric.columns:
            print(f"\nProcessing column for kurtosis calculation: {col}")

            kurtosis_value = kurtosis(
                numeric[col].dropna()
            )  # Dropping NaN to avoid calculation issues
            print(f"Kurtosis of '{col}': {kurtosis_value}")

            if kurtosis_value > 0:
                print(f"'{col}' is Leptokurtic (heavy tails of outliers).")
            elif kurtosis_value == 0:
                print(f"'{col}' is Mesokurtic (normal distribution).")
            else:
                print(f"'{col}' is Platykurtic (light tails of outliers).")

        print("Total no. of elements: ", size)
        print("*" * 100)
        print("Shape of the dataset: ", shape)
        print("*" * 100)
        print("Dimentions of the dataset: ", dimentions)
        print("*" * 100)
        print("Information of the dataset: ", info)
        print("*" * 100)
        print("Statistical summary of the dataset: ", summary)
        print("*" * 100)
        print("Name of the columns: ", columns)
        print("*" * 100)
        print("Total no. of columns: ", n_col)
        print("*" * 100)
        print("Datatypes of the dataset: ", types)
        print("*" * 100)
        print("No. of duplicated values: ", duplicated)
        print("*" * 100)
        print("Percentage (%) of duplicated values: ", p_dup * 100)
        print("*" * 100)
        print("No. of missing values: ", missing)
        print("*" * 100)
        print("Percentage (%) of missing values: ", p_miss * 100)
        print("*" * 100)
        print("Numerical columns are: ", numeric)
        print("*" * 100)
        print("No. of numrerical columns are: ", n_num)
        print("*" * 100)
        print("Categoical cloumns are: ", categoical)
        print("*" * 100)
        print("No. of categoical columns are: ", n_col)
        print("*" * 100)
        print("Date type columns are: ", datetime)
        print("*" * 100)
        print("Numerical correlations: ", corr)
        print("*" * 100)


class DataTypeHandler:
    """
    DataTypeHandler class to handle data type conversions for columns in a pandas DataFrame.

    The DataTypeHandler class provides methods to convert DataFrame columns to various data types,
    such as string, integer, float, and datetime. Each method includes error handling and provides
    feedback if the conversion fails.

    Parameters:
        -----------
        Column Name : pandas.DataFrame's Column name
            The DataFrame column name to be inspected.

        Returns:
        --------
        Converted Datatype of the specified column

    Methods
    -------
    __init__(df)
        Initializes the class with a DataFrame.

    to_string(col)
        Converts a specified column in the DataFrame to string type.

    to_int(col)
        Converts a specified column in the DataFrame to integer type.

    to_float(col)
        Converts a specified column in the DataFrame to float type.

    to_datetime(col)
        Converts a specified column in the DataFrame to datetime type.

    Example
    -------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': ['2023-01-01', '2023-02-01', '2023-03-01']})
    >>> handler = DataTypeHandler(df)
    >>> handler.to_string('A')
    Converted column 'A' to string.
    >>> handler.to_int('A')
    Converted column 'A' to int.
    >>> handler.to_float('A')
    Converted column 'A' to float.
    >>> handler.to_datetime('B')
    Converted column 'B' to datetime from int.
    """

    def __init__(df):
        """
        Initializes the DataTypeHandler class with a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to be inspected.

        Returns:
        --------
        None
        """
        df = df

    def to_string(col):
        """
        Converts a specified column in the DataFrame to string type.

        Parameters
        ----------
        col : str
            The column name to be converted to string.

        Returns
        -------
        String converted column of the specified column.

        Example
        -------
        >>> handler.to_string('A')
        Converted column 'A' to string.
        """

        try:
            df[col] = df[col].astype(str)
            print(f"Converted column '{col}' to string.")
        except Exception as e:
            print(f"Error converting '{col}' to string: {e}")

    def to_int(col):
        """
        Converts a specified column in the DataFrame to integer type.

        Parameters
        ----------
        col : str
            The column name to be converted to integer.

        Returns
        -------
        Integer converted column of the specified column.

        Example
        -------
        >>> handler.to_int('A')
        Converted column 'A' to int.
        """
        try:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            print(f"Converted column '{col}' to int.")
        except Exception as e:
            print(f"Error converting '{col}' to int: {e}")

    def to_float(col):
        """
        Converts a specified column in the DataFrame to float type.

        Parameters
        ----------
        col : str
            The column name to be converted to float.

        Returns
        -------
        Float converted column of the specified column.

        Example
        -------
        >>> handler.to_float('A')
        Converted column 'A' to float.
        """
        try:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)
            print(f"Converted column '{col}' to float.")
        except Exception as e:
            print(f"Error converting '{col}' to float: {e}")

    def to_datetime(col):
        """
        Converts a specified column in the DataFrame to datetime type.

        Parameters
        ----------
        col : str
            The column name to be converted to datetime.

        Returns
        -------
        Datetime converted column of the specified column.

        Example
        -------
        >>> handler.to_datetime('B')
        Converted column 'B' to datetime from int.
        """
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            print(f"Converted column '{col}' to datetime from int.")
        except Exception as e:
            print(f"Error converting '{col}' to datetime from int: {e}")


class MissingValueHandler:
    """
    A class for handling missing values in a pandas DataFrame using various imputation techniques.

    This class provides several methods for filling missing values in numeric columns of a DataFrame
    using mean, median, mode, forward fill, backward fill, linear interpolation, and polynomial interpolation.
    It also provides a method to drop rows with missing values in a specified column.

    Methods
    -------
    __init__(df):
        Initializes the MissingValueHandler with a DataFrame.
    mean(col):
        Fills missing values in the specified column using the mean.
    median(col):
        Fills missing values in the specified column using the median.
    mode(col):
        Fills missing values in the specified column using the mode.
    b_fill(col):
        Fills missing values in the specified column using backward fill.
    f_fill(col):
        Fills missing values in the specified column using forward fill.
    linear(col):
        Fills missing values in the specified column using linear interpolation.
    polynomial(col):
        Fills missing values in the specified column using second-order polynomial interpolation.
    drop(col):
        Drops rows with missing values in the specified column.

    Example
    -------
    # Example usage:
    import pandas as pd

    # Create a sample DataFrame
    data = {'A': [1, 2, None, 4, 5],
            'B': [None, 2, 3, None, 5],
            'C': ['a', 'b', 'c', 'd', None]}

    df = pd.DataFrame(data)

    # Initialize the MissingValueHandler class with the DataFrame
    handler = MissingValueHandler(df)

    # Fill missing values in column 'A' using mean
    handler.mean('A')

    # Fill missing values in column 'B' using median
    handler.median('B')

    # Drop rows with missing values in column 'C'
    handler.drop('C')
    """

    def __init__(df):
        """
        Initializes the Inspection class with a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to be inspected.

        Returns:
        --------
        None
        """
        df = df

    def mean(col):
        """
        Fills missing values in the specified column using the mean.

        Parameters
        ----------
        col : str
            The name of the column to fill missing values.

        Returns
        -------
        Missed values column/row filled with its mean value.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                mean_value = df[col].mean()
                df[col].fillna(mean_value, inplace=True)
                print(f"Filled missing values in '{col}' with mean: {mean_value}")
            else:
                print(f"Cannot fill for column '{col}' as it is non-numeric")

        except Exception as e:
            print(f"Cannot fill mean for column '{col}' due to '{e}'.")

    def median(col):
        """
        Fills missing values in the specified column using the median.

        Parameters
        ----------
        col : str
            The name of the column to fill missing values.

        Returns
        -------
        Missed values column/row filled with its median value.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
                print(f"Filled missing values in '{col}' with mean: {median_value}")
            else:
                print(f"Cannot fill for column '{col}' as it is non-numeric")

        except Exception as e:
            print(f"Cannot fill median for column '{col}' due to '{e}'.")

    def mode(col):
        """
        Fills missing values in the specified column using the mode.

        Parameters
        ----------
        col : str
            The name of the column to fill missing values.

        Returns
        -------
        Missed values column/row filled with its mode value.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                median_value = df[col].mode().iloc[0]
                df[col].fillna(median_value, inplace=True)
                print(f"Filled missing values in '{col}' with mean: {median_value}")
            else:
                print(f"Cannot fill for column '{col}' as it is non-numeric")

        except Exception as e:
            print(f"Cannot fill mode for column '{col}' due to '{e}'.")

    def b_fill(col):
        """
        Fills missing values in the specified column using backward fill.

        Parameters
        ----------
        col : str
            The name of the column to fill missing values.

        Returns
        -------
        Missed values column/row filled with its Backward fill value.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                df[col].bfill(inplace=True)
                print(f"Filled missing values in '{col}' using backward fill.")
            else:
                print(f"Cannot fill for column '{col}' as it is non-numeric")

        except Exception as e:
            print(f"Cannot bfill for column '{col}' due to '{e}'.")

    def f_fill(col):
        """
        Fills missing values in the specified column using forward fill.

        Parameters
        ----------
        col : str
            The name of the column to fill missing values.

        Returns
        -------
        Missed values column/row filled with its Forward fill value.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                df[col].ffill(inplace=True)
                print(f"Filled missing values in '{col}' using forward fill.")
            else:
                print(f"Cannot fill for column '{col}' as it is non-numeric")

        except Exception as e:
            print(f"Cannot ffill for column '{col}' due to '{e}'.")

    def linear(col):
        """
        Fills missing values in the specified column using linear interpolation(y=mx+c).

        Parameters
        ----------
        col : str
            The name of the column to fill missing values.

        Returns
        -------
        Missed values column/row filled with its linear interpolation value.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                df[col] = df[col].interpolate(method="linear")
                print(f"Filled missing values in '{col}' using linear value.")
            else:
                print(f"Cannot fill for column '{col}' as it is non-numeric")

        except Exception as e:
            print(f"Cannot linear fill for column '{col}' due to '{e}'.")

    def polynomial(col):
        """
        Fills missing values in the specified column using 2nd order quadratic interpolation(ax^2+bx+c=0).

        Parameters
        ----------
        col : str
            The name of the column to fill missing values.

        Returns
        -------
        Missed values column/row filled with its quadratic interpolation value.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                df[col] = df[col].interpolate(method="polynomial", order=2)
                print(f"Filled missing values in '{col}' using polynomial value.")
            else:
                print(f"Cannot fill for column '{col}' as it is non-numeric")

        except Exception as e:
            print(f"Cannot polynomial fill for column '{col}' due to '{e}'.")

    def drop(col):
        """
        Drops rows with missing values in the specified column.

        Parameters
        ----------
        col : str
            The name of the column to drop rows with missing values.

        Returns
        -------
        Dropped/Deleted column/row
        """
        try:
            initial_count = df.shape[0]
            df.dropna(subset=[col], inplace=True)
            final_count = df.shape[0]
            print(
                f"Dropped rows with missing values in '{col}'. Rows removed: {initial_count - final_count}"
            )
        except Exception as e:
            print(f"Cannot drop/delete values for column '{col}' due to '{e}'.")


class OutlierHander:
    """
    OutlierHander class for handling outliers in a pandas DataFrame using IQR and Z-score capping methods.

    The class provides methods to cap the outliers in numeric columns of a DataFrame using
    Interquartile Range (IQR) and Z-score methods.

    Methods
    -------
    iqr_capping(col):
        Caps the outliers in the specified column based on the IQR method.

    zscore_capping(col):
        Caps the outliers in the specified column based on the Z-score method.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data on which outlier capping will be applied.

    Example
    -------
    >>> # Example usage of the OutlierHandler class:
    >>> data = {'A': [1, 2, 3, 4, 100], 'B': [10, 20, 30, 40, 500]}
    >>> df = pd.DataFrame(data)
    >>> handler = OutlierHandler(df)
    >>> handler.iqr_capping('A')  # Applies IQR capping on column 'A'
    >>> handler.zscore_capping('B')  # Applies Z-score capping on column 'B'
    """

    def __init__(df):
        """
        Initializes the Inspection class with a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to be inspected.

        Returns:
        --------
        None
        """
        df = df

    def iqr_capping(col):
        """
        Caps the outliers in the specified column using the IQR (Interquartile Range) method.

        This method calculates the IQR of the column and caps the values outside
        the lower and upper bounds defined by the IQR rule.

        Parameters
        ----------
        col : str
            The name of the column to apply IQR capping on.

        Returns
        -------
        None

        Example
        -------
        >>> handler.iqr_capping('A')
        Outliers in 'A' have been capped using the IQR method.
        Lower Bound: -2.5, Upper Bound: 8.5
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                # Cap the values outside the bounds
                df[col] = np.where(
                    df[col] < lower_bound,
                    lower_bound,
                    np.where(df[col] > upper_bound, upper_bound, df[col]),
                )

                print(f"Outliers in '{col}' have been capped using the IQR method.")
                print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
            else:
                print(f"Cannot apply IQR capping to non-numeric column '{col}'.")

        except Exception as e:
            print("Cannot perform IQR outlier capping to the column '{col}' due to {e}")

    def zscore_capping(col):
        """
        Caps the outliers in the specified column using the Z-score method.

        This method uses the Z-score to identify outliers and caps values
        that fall outside a specified threshold.

        Parameters
        ----------
        col : str
            The name of the column to apply Z-score capping on.

        Returns
        -------
        None

        Example
        -------
        >>> handler.zscore_capping('B')
        Outliers in 'B' have been capped using the Z-score method with a threshold of 3.
        Lower Bound: -25.0, Upper Bound: 125.0
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                threshold = 3
                mean = df[col].mean()
                std = df[col].std()
                z_scores = stats.zscore(df[col].dropna())

                lower_bound = mean - threshold * std
                upper_bound = mean + threshold * std

                # Cap the values outside the bounds based on Z-score threshold
                df[col] = np.where(
                    z_scores < -threshold,
                    lower_bound,
                    np.where(z_scores > threshold, upper_bound, df[col]),
                )

                print(
                    f"Outliers in '{col}' have been capped using the Z-score method with a threshold of {col}."
                )
                print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
            else:
                print(f"Cannot apply Z-score capping to non-numeric column '{col}'.")
        except Exception as e:
            print(
                "Cannot perform Z-Score outlier capping to the column '{col}' due to {e}"
            )


class NumericalScaler:
    """
    A class for scaling numerical columns in a DataFrame using different scalers.

    The NumericalScaler class provides functionality to scale numerical columns
    in a pandas DataFrame using either the Standard Scaler or the Robust Scaler
    from the scikit-learn library. It automatically detects if the specified column
    is numeric before applying the scaling.

    Methods
    -------
    __init__(df)
        Initializes the class with a DataFrame.

    standardscaler(col)
        Applies Standard Scaler to a specified numerical column in the DataFrame.

    robustscaler(col)
        Applies Robust Scaler to a specified numerical column in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the columns to be scaled.

    Example
    -------
    >>> data = {'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50], 'C': ['a', 'b', 'c', 'd', 'e']}
    >>> df = pd.DataFrame(data)
    >>> scaler = NumericalScaler(df)
    >>> scaler.standardscaler('A')
    'A' has been scaled using Standard Scaler.
    >>> scaler.robustscaler('B')
    'B' has been scaled using Robust Scaler.
    """

    def __init__(df):
        """
        Initializes the Inspection class with a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to be inspected.

        Returns:
        --------
        None
        """
        df = df

    def standardscaler(col):
        """
        Scales the specified numerical column using Standard Scaler.

        The Standard Scaler standardizes features by removing the mean and scaling
        to unit variance, which is beneficial for normally distributed data.

        Parameters
        ----------
        col : str
            The name of the column to be scaled.

        Returns
        -------
        Scaled column of the specified cloumn name

        Example
        -------
        >>> scaler = NumericalScaler(df)
        >>> scaler.standardscaler('A')
        'A' has been scaled using Standard Scaler.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                scaler = StandardScaler()
                df[[col]] = scaler.fit_transform(df[[col]])
                print(f"'{col}' has been scaled using Standard Scaler.")
            else:
                print(f"Cannot apply Standard Scaler to non-numeric column '{col}'.")
        except Exception as e:
            print(f"Cannot apply Standard Scaler to column '{col}' due to '{e}'")

    def robustscaler(col):
        """
        Scales the specified numerical column using Robust Scaler.

        The Robust Scaler scales features using statistics that are robust to
        outliers by removing the median and scaling according to the interquartile
        range, making it useful for data with outliers.

        Parameters
        ----------
        col : str
            The name of the column to be scaled.

        Returns
        -------
        Scaled column of the specified cloumn name

        Example
        -------
        >>> scaler = NumericalScaler(df)
        >>> scaler.robustscaler('B')
        'B' has been scaled using Robust Scaler.
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                scaler = RobustScaler()
                df[[col]] = scaler.fit_transform(df[[col]])
                print(f"'{col}' has been scaled using Robust Scaler.")
            else:
                print(f"Cannot apply Robust Scaler to non-numeric column '{col}'.")
        except Exception as e:
            print(f"Cannot apply Robust Scaler to column '{col}' due to '{e}'")


class VariableTransformer:
    """
    VariableTransformer class used for transforming columns in a DataFrame using various techniques such as binning,
    log transformation, square root transformation, label encoding, and one-hot encoding.

    Methods
    -------
    binner(col, bins):
        Performs binning on a numerical column.

    log_transformer(col):
        Applies a log transformation to a numerical column.

    sqrt_transformer(col):
        Applies a square root transformation to a numerical column.

    label_encoding(col):
        Applies label encoding to a categorical column.

    one_hot_encoding(col):
        Applies one-hot encoding to a categorical column.

    Examples
    --------
    # Sample DataFrame
    >>> data = {'Age': [23, 45, 12, 36, 50], 'Salary': [40000, 50000, 10000, 60000, 75000], 'Gender': ['Male', 'Female', 'Female', 'Male', 'Female']}
    >>> df = pd.DataFrame(data)

    # Initialize the transformer
    >>> transformer = VariableTransformer(df)

    # Binning 'Age' column
    >>> transformer.binner('Age', bins=[0, 20, 40, 60])

    # Log transforming 'Salary' column
    >>> transformer.log_transformer('Salary')

    # Square root transforming 'Salary' column
    >>> transformer.sqrt_transformer('Salary')

    # Label encoding 'Gender' column
    >>> transformer.label_encoding('Gender')

    # One-hot encoding 'Gender' column
    >>> transformer.one_hot_encoding('Gender')
    """

    def __init__(df):
        """
        Initializes the Inspection class with a DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to be inspected.

        Returns:
        --------
        None
        """
        df = df

    def binner(col, bins):
        """
        Perform binning on a numerical column.

        Parameters
        ----------
        col : str
            The name of the column to be binned.
        bins : list
            The boundaries for the bins.

        Returns
        -------
        Binned transfomation of the specified column.

        Example
        -------
        >>> transformer.binner('Age', bins=[0, 20, 40, 60])
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                df[col] = pd.cut(df[col], bins=bins, include_lowest=True)
                print(f"'{col}' has been binned into {len(bins)-1} categories.")
            else:
                print(
                    f"Binning can only be applied to numeric columns. '{col}' is not numeric."
                )
        except Exception as e:
            print(f"Cannot apply Binning to column '{col}' due to '{e}'")

    def log_transformer(col):
        """
        Apply log transformation to a numerical column.

        Parameters
        ----------
        col : str
            The name of the column to be log-transformed.

        Returns
        -------
        Logarithmic transformation of the specified column.

        Example
        -------
        >>> transformer.log_transformer('Salary')
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                df[col] = np.log1p(df[col])  # log1p to handle log(0)
                print(f"Log transformation applied to '{col}'.")
            else:
                print(
                    f"Log transformation can only be applied to numeric columns. '{col}' is not numeric."
                )
        except Exception as e:
            print(f"Cannot apply Log transformation to column '{col}' due to '{e}'")

    def sqrt_transformer(col):
        """
        Apply square root transformation to a numerical column.

        Parameters
        ----------
        col : str
            The name of the column to be square root transformed.

        Returns
        -------
        Squared root transformation of the specified column.


        Example
        -------
        >>> transformer.sqrt_transformer('Salary')
        """
        try:
            if df[col].dtype in ["int64", "float64"]:
                df[col] = np.sqrt(df[col])
                print(f"Square root transformation applied to '{col}'.")
            else:
                print(
                    f"Square root transformation can only be applied to numeric columns. '{col}' is not numeric."
                )
        except Exception as e:
            print(
                f"Cannot apply Square root transformation to column '{col}' due to '{e}'"
            )

    def label_encoding(col):
        """
        Apply label encoding to a categorical column.

        Parameters
        ----------
        col : str
            The name of the column to be label encoded.

        Returns
        -------
        Label encoded transformation of the specified column.

        Example
        -------
        >>> transformer.label_encoding('Gender')
        """
        try:
            if df[col].dtype == "object":
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                print(f"Label encoding applied to '{col}'.")
            else:
                print(
                    f"Label encoding can only be applied to categorical columns. '{col}' is not categorical."
                )
        except Exception as e:
            print(f"Cannot apply Label encoding to column '{col}' due to '{e}'")

    def one_hot_encoding(col):
        """
        Apply one-hot encoding to a categorical column.

        Parameters
        ----------
        col : str
            The name of the column to be label encoded.

        Returns
        -------
        One-hot encoded transformation of the specified column.

        Example
        -------
        >>> transformer.one_encoding('Gender')
        """
        try:
            if df[col].dtype == "object":
                one_hot_encoder = OneHotEncoder(
                    sparse_output=False, handle_unknown="ignore"
                )
                df[col] = one_hot_encoder.fit_transform(df[[col]])
                print(f"One-hot encoding applied to '{col}'.")
            else:
                print(
                    f"One-hot encoding can only be applied to categorical columns. '{col}' is not categorical."
                )
        except Exception as e:
            print(f"Cannot apply One-hot encoding to column '{col}' due to '{e}'")
