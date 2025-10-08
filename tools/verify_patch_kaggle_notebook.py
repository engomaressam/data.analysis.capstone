import json
import os

NB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'portfolio', 'kaggle_kernel_python', 'kaggle_portfolio_notebook.ipynb'))

IMPORT_MARKER = '# Load required libraries\n'
DATA_LOAD_MARKER = '# Load Cyclistic Bike Share Data\n'
PLOT_PATCH_MARKER = 'Member Distribution plot using provided dataset metrics when available'


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb.get('cells', [])

    # Locate import and data load cells
    import_idx = None
    load_idx = None
    plot_cell_idx = None
    for idx, cell in enumerate(cells):
        if cell.get('cell_type') == 'code':
            src_list = cell.get('source', [])
            src0 = src_list[0] if src_list else ''
            if src0 == IMPORT_MARKER:
                import_idx = idx
            if src0 == DATA_LOAD_MARKER:
                load_idx = idx
            if any(PLOT_PATCH_MARKER in s for s in src_list):
                plot_cell_idx = idx

    # Checks
    has_os_import = False
    if import_idx is not None:
        has_os_import = any(line.strip() == 'import os' for line in cells[import_idx].get('source', []))

    has_dataset_base = False
    if load_idx is not None:
        has_dataset_base = any('dataset_base' in line for line in cells[load_idx].get('source', []))

    # Find variables cell(s)
    member_var_idx = None
    daily_var_idx = None
    monthly_var_idx = None
    for idx, cell in enumerate(cells):
        if cell.get('cell_type') != 'code':
            continue
        src = ''.join(cell.get('source', []))
        if member_var_idx is None and 'member_distribution =' in src:
            member_var_idx = idx
        if daily_var_idx is None and 'daily_usage =' in src:
            daily_var_idx = idx
        if monthly_var_idx is None and 'monthly_usage =' in src:
            monthly_var_idx = idx

    # Determine if variables cell was inserted after the data load cell
    inserted_after_load = False
    if load_idx is not None and member_var_idx is not None:
        inserted_after_load = member_var_idx > load_idx

    print('Import cell has os import:', has_os_import)
    print('Data load cell has dataset_base:', has_dataset_base)
    print('Variables cell inserted after data load:', inserted_after_load)
    print('member_distribution defined somewhere:', member_var_idx is not None)
    print('daily_usage defined somewhere:', daily_var_idx is not None)
    print('monthly_usage defined somewhere:', monthly_var_idx is not None)
    print('Member Distribution plotting cell patched:', plot_cell_idx is not None)


if __name__ == '__main__':
    main()