from tabulate import tabulate

class ReportGenerator:

    @classmethod
    def generate_report(cls, profile):
        """Generates a report of the data profile."""
        report = []
        
        # Columns
        report.append("Columns:")
        report.append(tabulate([[col] for col in profile['columns']], headers=["Column Name"]))
        
        # Data types
        report.append("\nData Types:")
        data_types_table = [[col, dtype] for col, dtype in profile['data_types'].items()]
        report.append(tabulate(data_types_table, headers=["Column", "Data Type"]))
        
        # Missing values
        report.append("\nMissing Values:")
        missing_values_table = [[col, missing] for col, missing in profile['missing_values'].items()]
        report.append(tabulate(missing_values_table, headers=["Column", "Missing Count"]))
        
        # Unique values
        report.append("\nUnique Values:")
        unique_values_table = [[col, unique] for col, unique in profile['unique_values'].items()]
        report.append(tabulate(unique_values_table, headers=["Column", "Unique Count"]))
        
        # Summary statistics
        report.append("\nSummary Statistics:")
        summary_stats_table = []
        for col, stats in profile['summary_statistics'].items():
            for stat, value in stats.items():
                summary_stats_table.append([col, stat, value])
        report.append(tabulate(summary_stats_table, headers=["Column", "Statistic", "Value"]))
        
        return "\n".join(report)
