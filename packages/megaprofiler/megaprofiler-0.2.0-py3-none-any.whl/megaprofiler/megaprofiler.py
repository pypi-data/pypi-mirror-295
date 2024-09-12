import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import silhouette_score
import statsmodels.api as sm
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

class MegaProfiler:

    @classmethod
    def basic_profile_analysis(cls, data):
        """Generate a basic profile of the dataset."""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        profile = {
            "columns": data.columns.tolist(),
            "missing_values": data.isnull().sum().to_dict(),
            "data_types": data.dtypes.to_dict(),
            "unique_values": data.nunique().to_dict(),
            "summary_statistics": data.describe().to_dict(),
        }

        return profile


    @classmethod
    def pearson_correlation_analysis(cls, data):
        """Returns the correlation matrix for numerical columns."""
        numerical_data = data.select_dtypes(include=[np.number])
        return numerical_data.corr(method = "pearson")
    

    @classmethod
    def covariance_analysis(cls, data):
        """Returns the covariance matrix for numerical columns."""
        numerical_data = data.select_dtypes(include=[np.number])
        return numerical_data.cov()
    

    @classmethod
    def missing_data_heatmap(cls, data):
        """Generate a heatmap of missing values in the dataset."""
        plt.figure(figsize = (10, 7))
        sns.heatmap(data.isnull(), cbar = False, cmap = "viridis")
        plt.title("-- MISSING DATA HEATMAP --")
        plt.show()


    @classmethod
    def zscore_outlier_analysis(cls, data, threshold = 3):
        """Detect outliers using z-score."""
        data = data.select_dtypes(include=[np.number])
        z_scores = np.abs(stats.zscore(data.select_dtypes(include = [np.number])))
        outliers = (z_scores > threshold).any(axis = 1)
        
        return data[outliers]
    

    @classmethod
    def iqr_outlier_analysis(cls, data):
        """Detect outliers using IQR (Inter-Quartile Range)."""
        data = data.select_dtypes(include=[np.number])
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1

        return data[((data < (q1 - 1.5 * iqr)) | (data > (q3 + 1.5 * iqr))).any(axis = 1)]
    

    @classmethod
    def data_drift_analysis(cls, current_data, prior_data):
        """Detect data drift by comparing basic statistics between two datasets."""
        drift_summary = {}
        for col in current_data.columns:
            if current_data[col].dtype != object:
                drift_summary[col] = {
                    'current_mean': current_data[col].mean(),
                    'previous_mean': prior_data[col].mean(),
                    'drift': np.abs(current_data[col].mean() - prior_data[col].mean())
                }

        return drift_summary
    

    @classmethod 
    def categorical_data_analysis(cls, data):
        """Perform analysis on categorical columns."""
        analysis = {}
        for col in data.select_dtypes(include=['object']).columns:
            analysis[col] = {
                'unique_values': data[col].unique().tolist(),
                'mode': data[col].mode()[0],
                'value_counts': data[col].value_counts().to_dict()
            }

        return analysis


    @classmethod
    def text_data_analysis(cls, data, text_column):
        """Perform basic NLP analysis on a text column."""
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(data[text_column].fillna(''))

        return tfidf_matrix


    @classmethod
    def data_imbalance_analysis(cls, data, target_column):
        """Detect class imbalance by examining the distribution of target labels."""

        return data[target_column].value_counts(normalize=True)
    

    @classmethod
    def data_skewness(cls, data):
        """Compute skewness for numerical columns."""
        skew_summary = {}
        for col in data.select_dtypes(include=[np.number]):
            skew_summary[col] = stats.skew(data[col].dropna())

        return skew_summary
    

    @classmethod
    def data_kurtosis(cls, data):
        """Compute kurtosis for numerical columns."""
        kurtosis_summary = {}
        for col in data.select_dtypes(include=[np.number]):
            kurtosis_summary[col] = stats.kurtosis(data[col].dropna())

        return kurtosis_summary


    @classmethod
    def memory_usage_analysis(cls, data):
        """Profile the memory usage of each column in the dataset."""

        return data.memory_usage(deep = True)


    @classmethod
    def time_series_analysis(cls, data, time_column, period = 1):
        """Perform basic time series analysis including decomposition and autocorrelation."""
        decomposition = sm.tsa.seasonal_decompose(data[time_column].dropna(), model='additive', period = period)

        return decomposition
    


    @classmethod
    def validate(cls, data, rules):

        """Validate the dataset against provided rules."""
        violations = []
        
        for rule in rules:
            column = rule.get('column')
            condition = rule.get('condition')
            message = rule.get('message', "Validation failed")
            
            if column not in data.columns:
                violations.append(f"Column '{column}' not found in data.")
                continue

            # Check for missing values
            if condition == 'no_missing':
                if data[column].isnull().sum() > 0:
                    violations.append(message)

            # Check for data types
            elif condition == 'data_type':
                expected_type = rule.get('expected_type')
                if not pd.api.types.is_dtype_equal(data[column].dtype, expected_type):
                    violations.append(message)

            # Check for value range
            elif condition == 'range':
                min_val, max_val = rule.get('min'), rule.get('max')
                if not data[column].between(min_val, max_val).all():
                    violations.append(message)

        return violations


    @classmethod
    def pca_analysis(cls, data, n_components = 2):
        """Perform Principal Component Analysis on numerical columns."""
        numerical_data = data.select_dtypes(include = [np.number]).dropna()
        pca = PCA(n_components = n_components)
        pca_result = pca.fit_transform(numerical_data)
        explained_variance = pca.explained_variance_ratio_
        return pca_result, explained_variance


    @classmethod
    def isolation_forest_analysis(cls, data, contamination = 0.1):
        """Detect anomalies using Isolation Forest on numerical columns."""
        numerical_data = data.select_dtypes(include = [np.number]).dropna()
        isolation_forest = IsolationForest(contamination = contamination, random_state = 21)
        anomaly_labels = isolation_forest.fit_predict(numerical_data)
        return anomaly_labels


    @classmethod
    def feature_importance_analysis(cls, data, target_column):
        """Analyze feature importance using RandomForest."""
        numerical_data = data.select_dtypes(include = [np.number]).dropna()
        X = numerical_data
        y = data[target_column]
        rf = RandomForestClassifier(random_state = 21)
        rf.fit(X, y)
        feature_importances = pd.DataFrame(rf.feature_importances_, index = X.columns, columns = ['importance'])
        return feature_importances


    @classmethod
    def multicollinearity_analysis(cls, data):
        """Detect multicollinearity using Variance Inflation Factor (VIF) on numerical columns."""
        numerical_data = data.select_dtypes(include = [np.number]).dropna()
        vif_data = pd.DataFrame()
        vif_data["feature"] = numerical_data.columns
        vif_data["VIF"] = [variance_inflation_factor(numerical_data.values, i) for i in range(numerical_data.shape[1])]
        return vif_data


    @classmethod
    def normality_test(cls, data):
        """Perform a Shapiro-Wilk test for normality on numerical columns."""
        numerical_data = data.select_dtypes(include = [np.number])
        normality_results = {}
        for col in numerical_data.columns:
            normality_results[col] = stats.shapiro(numerical_data[col].dropna()).pvalue
        return normality_results


    @classmethod
    def ttest_analysis(cls, data, numerical_feature_1, numerical_feature_2):
        """Perform a t-test between two numerical columns."""
        return stats.ttest_ind(data[numerical_feature_1].dropna(), data[numerical_feature_2].dropna())
    

    @classmethod
    def chi_square_test(cls, data, categorical_column_1, categorical_column_2):
        """Perform a Chi-squared test between two categorical columns."""
        contingency_table = pd.crosstab(data[categorical_column_1], data[categorical_column_2])
        return stats.chi2_contingency(contingency_table)


    @classmethod
    def kmeans_clustering(cls, data, n_clusters = 3):
        """Perform K-Means clustering on numerical columns."""
        numerical_data = data.select_dtypes(include=[np.number]).dropna()
        kmeans = KMeans(n_clusters = n_clusters, random_state = 21)
        clusters = kmeans.fit_predict(numerical_data)
        return clusters


    @classmethod
    def tsne_analysis(cls, data, n_components = 2, perplexity = 2):
        """Perform t-SNE dimensionality reduction on numerical columns."""
        numerical_data = data.select_dtypes(include = [np.number]).dropna()
        tsne = TSNE(n_components = n_components, perplexity = perplexity, random_state = 21)
        tsne_result = tsne.fit_transform(numerical_data)
        return tsne_result
    

    @classmethod
    def smote_balancing(cls, data, target_column):
        """Balance data using SMOTE (for classification problems)."""
        numerical_data = data.select_dtypes(include = [np.number])
        X = numerical_data
        y = data[target_column]
        smote = SMOTE(random_state = 21)
        X_res, y_res = smote.fit_resample(X, y)
        return X_res, y_res


    @classmethod
    def undersampling_balancing(cls, data, target_column):
        """Balance data using Random Undersampling."""
        numerical_data = data.select_dtypes(include = [np.number])
        X = numerical_data
        y = data[target_column]
        undersampler = RandomUnderSampler(random_state = 21)
        X_res, y_res = undersampler.fit_resample(X, y)
        return X_res, y_res


    @classmethod
    def recursive_feature_elimination(cls, data, target_column, n_features_to_select = 5):
        """Perform Recursive Feature Elimination (RFE) on numerical columns."""
        numerical_data = data.select_dtypes(include = [np.number])
        X = numerical_data
        y = data[target_column]
        model = LogisticRegression()
        rfe = RFE(model, n_features_to_select=n_features_to_select)
        rfe.fit(X, y)
        return X.columns[rfe.support_].tolist()  # Returns the selected features


    @classmethod
    def cross_validation_analysis(cls, X, y, cv = 3):
        """Perform k-fold cross-validation and return the mean and std of scores."""
        return cross_val_score(RandomForestClassifier(random_state = 21), X, y, cv = cv).mean(), cross_val_score(RandomForestClassifier(random_state = 21), X, y, cv = cv).std()


    @classmethod
    def silhouette_analysis(cls, data, cluster_labels):
        """Perform Silhouette Analysis for clustering."""
        numerical_data = data.select_dtypes(include = [np.number])
        score = silhouette_score(numerical_data, cluster_labels)
        return score  # Higher silhouette score indicates better-defined clusters


if __name__ == "__main__":

    print("please import to use.")

