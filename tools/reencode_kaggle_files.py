import json, os

PY_NB = r"C:\Users\Diaa\data.analysis.capstone\portfolio\kaggle_kernel_python\kaggle_portfolio_notebook.ipynb"
RMD = r"C:\Users\Diaa\data.analysis.capstone\portfolio\kaggle_kernel_r\kaggle_portfolio_notebook.Rmd"


def reencode_ipynb(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    # Dump ensuring ASCII escape sequences to avoid Windows cp1252 decode issues
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=True)
    print(f"Re-encoded ipynb as ASCII-only: {path}")


def reencode_text_ascii(path: str) -> None:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()
    safe = txt.encode("ascii", "backslashreplace").decode("ascii")
    with open(path, "w", encoding="ascii", errors="replace") as f:
        f.write(safe)
    print(f"Re-encoded text as ASCII-only: {path}")


if __name__ == "__main__":
    reencode_ipynb(PY_NB)
    reencode_text_ascii(RMD)