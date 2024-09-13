import logging
import shutil
import subprocess

from .build_context import BuildContext
from .book_renderer import BookRenderer


logger = logging.getLogger(__name__)


class JupyterBookRenderer(BookRenderer):

    def jb_build(self, build_ctx: BuildContext, builder_arg: str):
        all_arg = ""
        if build_ctx.rebuild:
            all_arg = "--all "

        cmd = f"jb build {all_arg}{build_ctx.source_dir} --builder {builder_arg}"

        stdoutf = open(build_ctx.build_dir / "jb_logs.txt", 'w', encoding="utf-8")
        
        subprocess.run(cmd, shell=True, check=True,
                       stdout=stdoutf,
                       stderr=stdoutf)

        stdoutf.close()

    def build_html(self, document_name: str, build_ctx: BuildContext):

        self.jb_build(build_ctx, "html")

        source_path = build_ctx.build_dir / "html"
        named_path = build_ctx.build_dir / document_name

        shutil.copytree(source_path, named_path)

        archive_path = build_ctx.build_dir / document_name
        shutil.make_archive(str(archive_path), "zip", str(named_path))
        shutil.rmtree(named_path)

    def build_pdf(self, document_name: str, build_ctx: BuildContext):

        self.jb_build(build_ctx, "pdflatex")

        source_path = build_ctx.build_dir / "latex/book.pdf"
        dst_path = build_ctx.build_dir / f"{document_name}.pdf"
        shutil.move(source_path, dst_path)
