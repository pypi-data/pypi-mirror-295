"""matplatex: export matplotlib figures as pdf and text separately for
use in LaTeX.

Copyright (C) 2023 Johannes Sørby Heines

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from beartype import beartype
import matplotlib.pyplot as plt

from .tools import write_tex, make_all_transparent, restore_colors
from .latex_input import LaTeXinput

@beartype
def save(
        figure: plt.Figure,
        filename: str,
        *,
        widthcommand: str = r"\figurewidth",
        draw_anchors: bool = False,
        verbose: bool = True
        ):
    """Save matplotlib Figure with text in a separate tex file.

    Arguments:
    figure      The matplotlib Figure to save
    filename    The name to use for the files, without extention

    Optional keyword arguments:
    widthcommand    The LaTeX length command which will be used to
                    define the width of the figure.
    draw_anchors    If True, mark the text anchors on the figure.
                    Useful for debugging.
    verbose: bool   Print save message.
    """
    figure.draw_without_rendering() # Must draw text before it can be extracted.
    output = LaTeXinput(widthcommand=widthcommand)
    write_tex(output, figure, graphics=filename, add_anchors=draw_anchors)
    output.write(f"{filename}.pdf_tex")
    color_backup = make_all_transparent(figure)
    figure.savefig(f"{filename}.pdf", format='pdf')
    restore_colors(figure, color_backup)
    if verbose:
        print(f"Figure written to files {filename}.pdf_tex and {filename}.pdf")
