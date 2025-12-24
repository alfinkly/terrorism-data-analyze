# Technology Stack

## Core Technologies

- **Python 3.x** - Primary programming language
- **Uv** - for .venv creation and dependency management
- **pandas** - Data manipulation and analysis
- **matplotlib** - Plotting and visualization
- **seaborn** - Statistical data visualization
- **countryinfo** - Population data retrieval

## Data Formats

- **Excel (.xlsx)** - Primary data storage format
- **PNG** - Chart output format

## Development Workflow

### Dataset Management

- Use `gtd-mini.xlsx` for development and testing
- Switch to `gtd.xlsx` for production analysis
- Toggle between datasets using configuration flags (e.g., `USE_FULL_DATASET`)

### Common Commands

```bash
# Create mini dataset for development
uv run python create_mini_dataset.py

# Run basic analysis
uv run python analyze.py

# Generate comprehensive analysis
uv run python analysis.py

# Country-specific analysis
uv run python kazakhstan_details.py
uv kazakhstan_rankings.py

# Per-capita analysis (requires internet for population data)
uv run python analyze_per_capita.py
```

## Code Conventions

### Column Renaming Pattern

All scripts use consistent column renaming for easier access:

```python
df.rename(columns={
    'iyear':'Year', 'imonth':'Month', 'iday':'Day',
    'country_txt':'Country', 'region_txt':'Region',
    'attacktype1_txt':'AttackType', 'target1':'Target',
    'nkill':'Killed', 'nwound':'Wounded',
    'gname':'Group', 'targtype1_txt':'Target_type',
    'weaptype1_txt':'Weapon_type'
}, inplace=True)
```

### Error Handling

- Always use try/except for file loading operations
- Provide clear error messages for missing files
- Handle missing data with `.fillna()` or `.dropna()`

### Visualization Standards

- Save all plots as PNG files to project root
- Use `plt.tight_layout()` before saving
- Include descriptive titles and axis labels
- Use seaborn for statistical plots, matplotlib for basic charts
