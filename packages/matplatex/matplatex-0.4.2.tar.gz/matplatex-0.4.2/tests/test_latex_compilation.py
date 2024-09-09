from pathlib import Path
from subprocess import run

import matplotlib.pyplot as plt
import pytest

from matplatex import save

LATEX_TYPICAL = r"""
\documentclass{article}

\usepackage{graphicx}
\usepackage{tikz}

\begin{document}

\newlength{\figurewidth}
\setlength{\figurewidth}{\linewidth}
\input{figure.pdf_tex}

\end{document}
"""

@pytest.fixture
def figure():
    plt.rc('text', usetex=True)
    fig, [ax1, ax2] = plt.subplots(1, 2)
    x1 = [-1, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 1]
    y11 = [x**3 for x in x1]  # no numpy to avoid superfluous dependencies
    y12 = [x**2 for x in x1]
    ax1.plot(x1, y11, 'o-', label='$x^3$')
    ax1.plot(x1, y12, 'd-', label='$x^2$')
    ax1.legend()
    ax1.set_xlabel('x', usetex=False)
    ax1.set_ylabel('y')
    ax2.axhline(20)
    ax2.axhspan(0, 17)
    ax2.plot([0, 3, 4, 7], [15, 11, 7, 3], '--')
    return fig

def test_compilation(figure, tmp_path):
    latex_path = tmp_path / 'document.tex'
    figure_path = tmp_path / 'figure'
    # Regenerate the files each time so changes are applied.
    latex_path.write_text(LATEX_TYPICAL, encoding='utf-8')
    save(figure, str(figure_path))
    # compile with pdflatex
    compilation = run(
        ['pdflatex', latex_path.name],
        cwd=tmp_path
        )
    assert compilation.returncode == 0
