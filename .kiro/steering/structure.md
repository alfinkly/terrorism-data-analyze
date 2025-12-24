# Project Structure

## Root Directory Layout

```
├── .git/                    # Git version control
├── .kiro/                   # Kiro IDE configuration and steering
├── .gitignore              # Git ignore patterns
├── LICENSE                 # Apache 2.0 license
├── gtd.xlsx               # Full Global Terrorism Database (not in git)
├── gtd-mini.xlsx          # Development subset dataset (not in git)
└── *.py                   # Analysis scripts
```

## Python Scripts Organization

### Core Analysis Scripts

- **`analysis.py`** - Main comprehensive analysis with regional comparisons
- **`analyze.py`** - Basic dataset exploration and statistics
- **`analyze_per_capita.py`** - Per-capita attack rate calculations

### Specialized Analysis Scripts

- **`kazakhstan_details.py`** - Weapon types and terrorist groups in Kazakhstan
- **`kazakhstan_rankings.py`** - Attack types, targets, and city rankings for Kazakhstan

### Utility Scripts

- **`create_mini_dataset.py`** - Creates development subset from full dataset

## File Naming Conventions

### Scripts

- Use lowercase with underscores: `analyze_per_capita.py`
- Descriptive names indicating purpose: `kazakhstan_details.py`

### Data Files

- Excel files: `.xlsx` extension
- Mini datasets: `-mini` suffix for development versions

### Output Files

- Charts: descriptive names with `.png` extension
- Examples: `attacks_by_region.png`, `kazakhstan_weapon_types.png`

## Code Organization Patterns

### Script Structure

1. Imports at top
2. Configuration constants (e.g., `USE_FULL_DATASET`)
3. Function definitions with docstrings
4. Main execution block with `if __name__ == "__main__":`

### Function Naming

- Use descriptive verb phrases: `load_data()`, `plot_attacks_by_region()`
- Analysis functions: `analyze_kazakhstan_data()`
- Ranking functions: `rank_countries_by_metric()`

### Data Processing Flow

1. Load data with error handling
2. Rename columns for consistency
3. Filter/process data as needed
4. Generate analysis and visualizations
5. Save outputs to project root

## Development Guidelines

- Keep scripts focused on single analysis themes
- Use consistent column renaming across all scripts
- Always include error handling for file operations
- Generate both console output and visual charts
- Use configuration flags to switch between datasets
