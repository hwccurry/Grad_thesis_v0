#!/usr/bin/env python3
import json
import re
from pathlib import Path

NB_DIR = Path('/Users/mac/Desktop/Grad_thesis/参考文献/1/20240618102625WU_FILE_1/程序/程序-python')
TARGET_FOLDER = "参考文献/1/20240618102625WU_FILE_1"

PATH_CELL = """TARGET_FOLDER = '参考文献/1/20240618102625WU_FILE_1'\n
def locate_project_root(target_folder=TARGET_FOLDER):\n    current = Path.cwd().resolve()\n    for candidate in [current, *current.parents]:\n        if (candidate / target_folder).exists():\n            return candidate\n    raise FileNotFoundError(f'未能在 {current} 及其父目录中定位 {target_folder}')\n
PROJECT_ROOT = locate_project_root()\nDATA_DIR = PROJECT_ROOT / TARGET_FOLDER / '数据' / '数据-python'\nOUTPUT_DIR = PROJECT_ROOT / 'output'\nTABLE_DIR = OUTPUT_DIR / 'tables'\nFIG_DIR = OUTPUT_DIR / 'figures'\nML_DIR = OUTPUT_DIR / 'ml'\nfor path in (TABLE_DIR, FIG_DIR, ML_DIR):\n    path.mkdir(parents=True, exist_ok=True)\nprint(f'PROJECT_ROOT: {PROJECT_ROOT}')\n"""

# read_csv absolute path -> DATA_DIR
READ_CSV_RE = re.compile(
    r"pd\.read_csv\(\s*r?['\"]/Users/mac/Desktop/(?:Grad_thesis|毕业论文)/参考文献/1/20240618102625WU_FILE_1/数据/数据-python/([^'\"/]+)['\"]\s*,\s*header\s*=\s*0\s*\)",
    re.MULTILINE,
)

# open absolute output/tables -> TABLE_DIR
OPEN_TABLE_RE = re.compile(
    r"open\(\s*r?['\"]/Users/mac/Desktop/(?:Grad_thesis|毕业论文)/output/tables/([^'\"/]+)['\"]\s*,\s*'w'\s*\)",
    re.MULTILINE,
)

# plt.savefig absolute output/ml -> ML_DIR
SAVEFIG_ML_RE = re.compile(
    r"plt\.savefig\(\s*r?['\"]/Users/mac/Desktop/(?:Grad_thesis|毕业论文)/output/ml/([^'\"]+)['\"](?:\.format\(names\[i\]\))?\s*,\s*dpi\s*=\s*([0-9]+)\s*\)",
    re.MULTILINE,
)

# fallback absolute path removal for csv inside quotes
CSV_FALLBACK_RE = re.compile(
    r"['\"]/Users/mac/Desktop/(?:Grad_thesis|毕业论文)/参考文献/1/20240618102625WU_FILE_1/数据/数据-python/([^'\"/]+)['\"]",
    re.MULTILINE,
)


def split_source(text: str):
    parts = text.splitlines(keepends=True)
    return parts if parts else [""]


def transform_code(text: str):
    original = text
    text = READ_CSV_RE.sub(lambda m: f"pd.read_csv(DATA_DIR / '{m.group(1)}', header=0)", text)
    text = OPEN_TABLE_RE.sub(lambda m: f"open(TABLE_DIR / '{m.group(1)}','w')", text)
    text = SAVEFIG_ML_RE.sub(lambda m: f"plt.savefig(ML_DIR / '{m.group(1)}', dpi={m.group(2)})", text)
    text = CSV_FALLBACK_RE.sub(lambda m: f"str(DATA_DIR / '{m.group(1)}')", text)
    # Fix one malformed legacy savefig line with broken quotes.
    text = text.replace(
        "plt.savefig(r'/Users/mac/Desktop/Grad_thesis/output/ml/'分析师跟踪人数1.png'.format(names[i]), dpi=200)",
        "plt.savefig(ML_DIR / '分析师跟踪人数1.png', dpi=200)",
    )
    return text, text != original


def ensure_path_cell(nb):
    code_indices = [i for i, c in enumerate(nb.get('cells', [])) if c.get('cell_type') == 'code']
    if not code_indices:
        return False

    full_code = "\n".join("".join(c.get('source', [])) for c in nb['cells'] if c.get('cell_type') == 'code')
    if "TARGET_FOLDER = '参考文献/1/20240618102625WU_FILE_1'" in full_code and "DATA_DIR = PROJECT_ROOT" in full_code:
        # already present; still ensure Path import in first code cell
        first_idx = code_indices[0]
        src = "".join(nb['cells'][first_idx].get('source', []))
        if "from pathlib import Path" not in src:
            lines = src.splitlines(keepends=True)
            insert_at = 0
            for j, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_at = j + 1
            lines.insert(insert_at, "from pathlib import Path\n")
            nb['cells'][first_idx]['source'] = lines
            return True
        return False

    first_idx = code_indices[0]
    src = "".join(nb['cells'][first_idx].get('source', []))
    if "from pathlib import Path" not in src:
        lines = src.splitlines(keepends=True)
        insert_at = 0
        for j, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                insert_at = j + 1
        lines.insert(insert_at, "from pathlib import Path\n")
        nb['cells'][first_idx]['source'] = lines

    path_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": split_source(PATH_CELL),
    }
    nb['cells'].insert(first_idx + 1, path_cell)
    return True


def main():
    changed_files = []
    for nb_path in sorted(NB_DIR.glob('*.ipynb')):
        nb = json.loads(nb_path.read_text(encoding='utf-8'))
        changed = False

        for cell in nb.get('cells', []):
            if cell.get('cell_type') != 'code':
                continue
            source_text = "".join(cell.get('source', []))
            new_text, cell_changed = transform_code(source_text)
            if cell_changed:
                cell['source'] = split_source(new_text)
                changed = True

        if ensure_path_cell(nb):
            changed = True

        if changed:
            nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding='utf-8')
            changed_files.append(str(nb_path))

    print(f"changed_notebooks={len(changed_files)}")
    for p in changed_files:
        print(p)


if __name__ == '__main__':
    main()
