import sys
import unittest
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
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold
from sklearn.metrics import silhouette_score
import statsmodels.api as sm
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

from megaprofiler import MegaProfiler


class TestMegaProfiler(unittest.TestCase):

    def setUp(self):
        """Sample datasets for testing."""
        self.data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [5, 6, 7, np.nan, 9],
            'C': ['cat', 'dog', 'cat', 'cat', 'dog'],
            'D': [1.1, 2.2, np.nan, 4.4, 5.5],
            'E': pd.date_range(start='1/1/2020', periods=5)
        })
        
        self.prior_data = pd.DataFrame({
            'A': [2, 3, 4, 5, 6],
            'B': [5, 5, 7, 8, 10],
            'C': ['cat', 'dog', 'cat', 'cat', 'dog'],
            'D': [1.2, 2.1, 3.3, 4.5, 5.1],
            'E': pd.date_range(start='1/1/2019', periods=5)
        })

        # target column
        self.target_column = 'A'

        self.X_train = self.data.drop(columns=[self.target_column])
        self.y_train = self.data[self.target_column]


    def test_basic_profile_analysis(self):
        """Test the basic profile analysis."""
        profile = MegaProfiler.basic_profile_analysis(self.data)
        self.assertIn('columns', profile)
        self.assertIn('A', profile['columns'])
        self.assertEqual(profile['missing_values']['B'], 1)


    def test_pearson_correlation_analysis(self):
        """Test Pearson correlation analysis."""
        correlation_matrix = MegaProfiler.pearson_correlation_analysis(self.data)
        self.assertAlmostEqual(correlation_matrix.loc['A', 'B'], 1.0, places=2)


    def test_covariance_analysis(self):
        """Test covariance matrix generation."""
        covariance_matrix = MegaProfiler.covariance_analysis(self.data)
        self.assertIn('A', covariance_matrix.columns)
        self.assertIn('B', covariance_matrix.index)


    def test_zscore_outlier_analysis(self):
        """Test z-score based outlier detection."""
        outliers = MegaProfiler.zscore_outlier_analysis(self.data)
        self.assertTrue(outliers.empty)


    def test_iqr_outlier_analysis(self):
        """Test IQR-based outlier detection."""
        outliers = MegaProfiler.iqr_outlier_analysis(self.data)
        self.assertTrue(outliers.empty)


    def test_data_drift_analysis(self):
        """Test data drift analysis."""
        drift_summary = MegaProfiler.data_drift_analysis(self.data, self.prior_data)
        self.assertIn('A', drift_summary)
        self.assertAlmostEqual(drift_summary['A']['drift'], 1.0)


    def test_categorical_data_analysis(self):
        """Test analysis on categorical columns."""
        analysis = MegaProfiler.categorical_data_analysis(self.data)
        self.assertIn('C', analysis)
        self.assertEqual(analysis['C']['mode'], 'cat')


    def test_text_data_analysis(self):
        """Test basic text data analysis."""
        text_data = pd.DataFrame({'text': ['hello world', 'machine learning is cool']})
        tfidf_matrix = MegaProfiler.text_data_analysis(text_data, 'text')
        self.assertEqual(tfidf_matrix.shape, (2, 6))


    def test_data_imbalance_analysis(self):
        """Test data imbalance analysis."""
        imbalance = MegaProfiler.data_imbalance_analysis(self.data, 'C')
        self.assertAlmostEqual(imbalance['cat'], 0.6)


    def test_data_skewness(self):
        """Test skewness calculation."""
        skew_summary = MegaProfiler.data_skewness(self.data)
        self.assertAlmostEqual(skew_summary['A'], 0.0, places=1)


    def test_data_kurtosis(self):
        """Test kurtosis calculation."""
        kurtosis_summary = MegaProfiler.data_kurtosis(self.data)
        self.assertAlmostEqual(kurtosis_summary['A'], -1.3, places=1)


    def test_memory_usage_analysis(self):
        """Test memory usage profiling."""
        memory_usage = MegaProfiler.memory_usage_analysis(self.data)
        self.assertIn('A', memory_usage.index)


    def test_validate(self):
        """Test the dataset validation method."""
        rules = [
            {'column': 'A', 'condition': 'no_missing', 'message': 'A has missing values.'},
            {'column': 'B', 'condition': 'range', 'min': 4, 'max': 10, 'message': 'B out of range.'}
        ]
        violations = MegaProfiler.validate(self.data, rules)
        self.assertIn('B out of range.', violations)


    def test_time_series_analysis(self):
        """Test time series decomposition."""
        self.data['E'] = pd.date_range(start='1/1/2020', periods = 5, freq = 'D') 
        decomposition = MegaProfiler.time_series_analysis(self.data, 'E')
        self.assertTrue(hasattr(decomposition, 'trend'))
        self.assertTrue(hasattr(decomposition, 'seasonal'))

    def test_pca_analysis(self):
        """Test PCA analysis."""
        pca_result, explained_variance = MegaProfiler.pca_analysis(self.data)
        self.assertEqual(len(explained_variance), 2)  # Expecting 2 components
        self.assertEqual(pca_result.shape[1], 2)


    def test_isolation_forest_analysis(self):
        """Test Isolation Forest for anomaly detection."""
        self.data = self.data.fillna(0)
        anomaly_labels = MegaProfiler.isolation_forest_analysis(self.data)
        self.assertEqual(len(anomaly_labels), len(self.data))
        self.assertIn(-1, anomaly_labels)  # -1 represents anomalies


    def test_feature_importance_analysis(self):
        """Test feature importance using RandomForest."""
        self.data = self.data.fillna(0) 
        importance = MegaProfiler.feature_importance_analysis(self.data, self.target_column)
        self.assertIn('importance', importance.columns)


    def test_multicollinearity_analysis(self):
        """Test multicollinearity using VIF."""
        vif_data = MegaProfiler.multicollinearity_analysis(self.data)
        self.assertIn('feature', vif_data.columns)
        self.assertIn('VIF', vif_data.columns)


    def test_normality_test(self):
        """Test Shapiro-Wilk normality test."""
        normality_results = MegaProfiler.normality_test(self.data)
        self.assertGreater(normality_results['A'], 0)  # p-value should be greater than 0


    def test_ttest_analysis(self):
        """Test t-test between two numerical features."""
        t_stat, p_val = MegaProfiler.ttest_analysis(self.data, 'A', 'B')
        self.assertLessEqual(p_val, 1)


    def test_chi_square_test(self):
        """Test Chi-squared test for categorical features."""
        chi2_stat, p_val, _, _ = MegaProfiler.chi_square_test(self.data, 'C', 'D')
        self.assertLessEqual(p_val, 1)


    def test_kmeans_clustering(self):
        """Test KMeans clustering."""
        self.data = self.data.fillna(0)
        clusters = MegaProfiler.kmeans_clustering(self.data)
        self.assertEqual(len(clusters), len(self.data))


    def test_tsne_analysis(self):
        """Test t-SNE dimensionality reduction."""
        tsne_result = MegaProfiler.tsne_analysis(self.data, n_components=2)
        self.assertEqual(tsne_result.shape[1], 2)


    def test_smote_balancing(self):
        """Test SMOTE for data balancing."""
        self.data = self.data.fillna(0)
        X_res, y_res = MegaProfiler.smote_balancing(self.data, self.target_column)
        self.assertEqual(len(X_res), len(y_res))


    def test_undersampling_balancing(self):
        """Test undersampling for data balancing."""
        X_res, y_res = MegaProfiler.undersampling_balancing(self.data, self.target_column)
        self.assertLessEqual(len(X_res), len(self.data))


    def test_recursive_feature_elimination(self):
        """Test Recursive Feature Elimination (RFE)."""
        self.data = self.data.fillna(0)
        selected_features = MegaProfiler.recursive_feature_elimination(self.data, self.target_column)
        self.assertLessEqual(len(selected_features), len(self.data.columns))


    def test_silhouette_analysis(self):
        """Test Silhouette Analysis for clustering."""
        self.data = self.data.fillna(0)
        clusters = MegaProfiler.kmeans_clustering(self.data)
        score = MegaProfiler.silhouette_analysis(self.data, clusters)
        self.assertGreaterEqual(score, -1)
        self.assertLessEqual(score, 1)



if __name__ == '__main__':
    unittest.main()
