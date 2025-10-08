import json
import os
from typing import List

NB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'portfolio', 'kaggle_kernel_python', 'kaggle_portfolio_notebook.ipynb'))

IMPORT_MARKER = '# Load required libraries\n'
DATA_LOAD_MARKER = '# Load Cyclistic Bike Share Data\n'

# Lines to insert into the data loading cell near the top (after introductory prints)
DATASET_DETECTION_LINES: List[str] = [
    "# Detect Kaggle dataset path or local fallback\n",
    "dataset_base = '/kaggle/input/cyclistic-eda-derived-metrics' if os.path.exists('/kaggle/input/cyclistic-eda-derived-metrics') else '../kaggle_dataset'\n",
    "data_source = 'kaggle' if os.path.exists('/kaggle/input/cyclistic-eda-derived-metrics') else 'local'\n",
    "member_dist_df = pd.read_csv(f\"{dataset_base}/member_distribution.csv\") if os.path.exists(f\"{dataset_base}/member_distribution.csv\") else None\n",
    "daily_usage_df = pd.read_csv(f\"{dataset_base}/daily_usage.csv\") if os.path.exists(f\"{dataset_base}/daily_usage.csv\") else None\n",
    "monthly_usage_df = pd.read_csv(f\"{dataset_base}/monthly_usage.csv\") if os.path.exists(f\"{dataset_base}/monthly_usage.csv\") else None\n",
]

# Lines to append at the end of the data loading cell to define commonly used tables
DATASET_VARIABLES_LINES: List[str] = [
    "# Derived member distribution and usage tables (prefer Kaggle dataset if available)\n",
    "if member_dist_df is not None:\n",
    "    member_distribution = member_dist_df\n",
    "else:\n",
    "    member_distribution = cyclistic_data['member_casual'].value_counts().rename_axis('member_type').reset_index(name='count')\n",
    "    member_distribution['percentage'] = member_distribution['count'] / member_distribution['count'].sum() * 100\n",
    "\n",
    "if daily_usage_df is not None:\n",
    "    daily_usage = daily_usage_df\n",
    "else:\n",
    "    daily_usage = cyclistic_data.groupby(['day_name','member_casual']).size().unstack(fill_value=0).reset_index()\n",
    "\n",
    "if monthly_usage_df is not None:\n",
    "    monthly_usage = monthly_usage_df\n",
    "else:\n",
    "    monthly_usage = cyclistic_data.groupby(['month_name','member_casual']).size().unstack(fill_value=0).reset_index()\n",
]


def ensure_os_import(import_cell_source: List[str]) -> List[str]:
    """Ensure 'import os' exists after numpy import in the import cell."""
    if any(line.strip() == 'import os' for line in import_cell_source):
        return import_cell_source
    # Find index after numpy import; fallback to after warnings import
    insert_idx = None
    for i, line in enumerate(import_cell_source):
        if line.strip() == 'import numpy as np':
            insert_idx = i + 1
            break
    if insert_idx is None:
        for i, line in enumerate(import_cell_source):
            if line.strip() == 'import warnings':
                insert_idx = i + 1
                break
    if insert_idx is None:
        insert_idx = 1  # after first line
    new_source = import_cell_source[:insert_idx] + ['import os\n'] + import_cell_source[insert_idx:]
    return new_source


def patch_data_loading_cell(cell_source: List[str]) -> List[str]:
    """Insert dataset detection lines near the top and dataset variables at the end."""
    # Insert detection lines after the initial intro prints, find the line with License print or the blank after
    insert_top_idx = None
    for i, line in enumerate(cell_source):
        if 'License: Divvy Data License Agreement' in line:
            insert_top_idx = i + 1
            break
    if insert_top_idx is None:
        # fallback: after the comment block
        for i, line in enumerate(cell_source[:20]):
            if line.strip() == '':
                insert_top_idx = i + 1
                break
    if insert_top_idx is None:
        insert_top_idx = 0

    # Only insert detection lines if not already present
    already = any('dataset_base' in l for l in cell_source)
    new_source = cell_source[:]
    if not already:
        new_source = new_source[:insert_top_idx] + DATASET_DETECTION_LINES + new_source[insert_top_idx:]

    return new_source


def insert_variables_cell(nb_cells: List[dict], after_index: int) -> None:
    """Insert a new code cell defining member_distribution, daily_usage, monthly_usage after the given index."""
    new_cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [line + ('' if line.endswith('\n') else '\n') for line in DATASET_VARIABLES_LINES]
    }
    nb_cells.insert(after_index + 1, new_cell)


def patch_member_distribution_plot(nb_cells: List[dict]) -> None:
    """Modify the Member Distribution plotting cell to use member_distribution with Kaggle metrics fallback."""
    md_idx = None
    for i, cell in enumerate(nb_cells):
        if cell.get('cell_type') == 'markdown':
            src = ''.join(cell.get('source', []))
            if 'Member vs Casual Distribution' in src:
                md_idx = i
                break
    if md_idx is None:
        return
    # Find next code cell
    plot_idx = None
    for j in range(md_idx + 1, len(nb_cells)):
        if nb_cells[j].get('cell_type') == 'code':
            plot_idx = j
            break
    if plot_idx is None:
        return
    new_source = [
        "# Member Distribution plot using provided dataset metrics when available\n",
        "print('👥 Member Distribution:')\n",
        "try:\n",
        "    md_df = member_distribution.copy()\n",
        "except NameError:\n",
        "    md_df = cyclistic_data['member_casual'].value_counts().rename_axis('member_type').reset_index(name='count')\n",
        "    md_df['percentage'] = md_df['count'] / md_df['count'].sum() * 100\n",
        "print(md_df[['member_type','count','percentage']])\n",
        "plt.figure(figsize=(8,5))\n",
        "sns.barplot(data=md_df, x='member_type', y='count', palette=['#0a7bc2', '#f4a620'])\n",
        "plt.title('Member vs Casual Distribution')\n",
        "plt.xlabel('Rider Type')\n",
        "plt.ylabel('Ride Count')\n",
        "for index, row in md_df.iterrows():\n",
        "    plt.text(index, row['count'] + max(md_df['count'])*0.01, f\"{row['percentage']:.1f}%\", ha='center')\n",
        "plt.show()\n",
    ]
    nb_cells[plot_idx]['source'] = new_source


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb.get('cells', [])

    # Patch import cell
    for cell in cells:
        if cell.get('cell_type') == 'code':
            src = cell.get('source', [])
            if src and src[0] == IMPORT_MARKER:
                cell['source'] = ensure_os_import(src)
                break

    # Patch data loading cell and record its index
    load_idx = None
    for idx, cell in enumerate(cells):
        if cell.get('cell_type') == 'code':
            src = cell.get('source', [])
            if src and src[0] == DATA_LOAD_MARKER:
                cells[idx]['source'] = patch_data_loading_cell(src)
                load_idx = idx
                break

    # Insert variables cell after data load if definitions are missing anywhere
    has_member_distribution = False
    for cell in cells:
        if cell.get('cell_type') == 'code':
            src = ''.join(cell.get('source', []))
            if 'member_distribution =' in src:
                has_member_distribution = True
                break
    if not has_member_distribution and load_idx is not None:
        insert_variables_cell(cells, load_idx)

    # Patch member distribution plotting cell to use metrics
    patch_member_distribution_plot(cells)

    # Write back with ASCII-safe encoding
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump({'cells': cells, **{k: v for k, v in nb.items() if k != 'cells'}}, f, ensure_ascii=True)

    print('Patched notebook successfully at:', NB_PATH)


if __name__ == '__main__':
    main()