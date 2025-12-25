import create_mini_dataset
import analyze
import analyze_per_capita
import success_rate_analysis
import seasonal_patterns
import deadliest_attacks
import group_analysis
import target_vulnerability
import decade_comparison
import kazakhstan_rankings
import kazakhstan_details


def main():
    # 1. Create a smaller dataset for faster testing (optional)
    # create_mini_dataset.create_mini_dataset(rows_to_keep=5000)

    # 2. Perform initial analysis
    analyze.run_analysis()

    # 3. Analyze attacks per capita
    analyze_per_capita.run_analysis()

    # 4. Analyze success rates
    success_rate_analysis.run_analysis()

    # 5. Analyze seasonal patterns
    seasonal_patterns.run_analysis()

    # 6. Analyze deadliest attacks
    deadliest_attacks.run_analysis()

    # 7. Analyze terrorist groups
    group_analysis.run_analysis()

    # 8. Analyze target vulnerability
    target_vulnerability.run_analysis()

    # 9. Compare decades
    decade_comparison.run_analysis()

    # 10. Find Kazakhstan's rankings
    kazakhstan_rankings.run_analysis()

    # 11. Get details on attacks in Kazakhstan
    kazakhstan_details.run_analysis()


if __name__ == "__main__":
    main()
