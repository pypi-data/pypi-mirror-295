import logging
from pathlib import Path

from icplot.tex_interface import TexInterface
from icplot.image_utils import svg_to_png, svg_to_pdf

logger = logging.getLogger(__name__)


class MediaConverter:

    def __init__(self):
        self.tex_interface = TexInterface(None, None)

    def run(self, source_dir: Path, output_dir: Path, build_dir: Path | None = None):

        if not source_dir.exists():
            return

        if not build_dir:
            build_dir = output_dir

        logger.info("Start converting media")

        self.tex_interface.build_dir = build_dir
        self.tex_interface.output_dir = output_dir
        self.tex_interface.build(source_dir)

        logger.info("Searching for svg files in %s", source_dir)
        svg_files = list(source_dir.glob("*.svg"))
        logger.info("Found %d files", len(svg_files))
        for svg_file in svg_files:
            png_path = output_dir / f"{svg_file.stem}.png"
            pdf_path = output_dir / f"{svg_file.stem}.pdf"
            svg_to_png(svg_file, png_path)
            svg_to_pdf(svg_file, pdf_path)

        logger.info("Finished converting media")
