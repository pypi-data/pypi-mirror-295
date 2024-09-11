import sys
import json
import logging
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path

import yaml
from jinja2 import Environment, PackageLoader

import app.reports.convert as convert
import app.reports.report_lib as rlib
from app.reports.report import Report

_basedir = "/tmp"
logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("uvicorn")


class Reporter(ABC):
    def __init__(self, spec: dict):
        self.spec = spec
        self.context = {}
        # init_logger()

    @abstractmethod
    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list: ...

    @abstractmethod
    def processor(
        self,
        data: list,
        args: dict[str, str | float | int | bool | list],
    ) -> dict: ...

    def collect_and_process(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> None:

        # Get the data
        data = self.collector(
            args=args,
            org_uid=org_uid,
            api_key=api_key,
            api_url=api_url,
        )

        # Process the data to a lowest common denominator context
        # dict that can be used to render the report in multiple formats
        self.context = self.processor(data, args)

    def renderer(
        self,
        format: str,
        rid: str,
    ) -> Path:
        return self.render(self.context, format, rid)

    def generate_reports(
        self, r: Report, api_key: str, api_url: str
    ) -> dict[rlib.FORMATS, Path]:
        rv = dict()

        logger.info(
            f"Generating {r.input.report_id} report for {r.input.org_uid} ({r.id})"
        )
        t1 = time.time()

        # Collect and process the data
        self.collect_and_process(
            args=r.input.report_args,
            org_uid=r.input.org_uid,
            api_key=api_key,
            api_url=api_url,
        )

        t2 = time.time()
        logger.info(
            f"Collection and processing done for {r.input.report_id} "
            f"report for {r.input.org_uid} ({r.id}) - took {t2-t1} seconds"
        )

        # Render the report in all supported formats
        for fmt in self.spec["supported_formats"]:
            rv[fmt] = self.renderer(fmt, r.id)  # type: ignore

        t3 = time.time()
        logger.info(
            f"Rendering done for {r.input.report_id} report for {r.input.org_uid} ({r.id}) - took {t3-t2} seconds"
        )

        return rv

    def render(self, context: dict, format: str, rid: str) -> Path:

        if format == "json":
            with open(f"{_basedir}/{rid}.json", "w") as f:
                json.dump(context, f)
            return Path(f"{_basedir}/{rid}.json")

        if format == "yaml":
            # Yaml default dict output is adding in python info about
            # the default dict type and function, so we need to convert
            # the default dict to a normal dict before writing to yaml
            for k, v in context.items():
                if isinstance(v, defaultdict):
                    context[k] = defaultdict_to_dict(v)
            with open(f"{_basedir}/{rid}.yaml", "w") as f:
                yaml.dump(context, f)
            return Path(f"{_basedir}/{rid}.yaml")

        if format == "md":
            with open(f"{_basedir}/{rid}.md", "w") as f:
                f.write(self.render_with_template(format, context))
            return Path(f"{_basedir}/{rid}.md")

        if format == "mdx":
            with open(f"{_basedir}/{rid}.mdx", "w") as f:
                f.write(self.render_with_template(format, context))
            return Path(f"{_basedir}/{rid}.mdx")

        if format == "pdf":
            if not Path(f"{_basedir}/{rid}.md").exists():
                self.render(context, "md", rid)
            if not Path(f"{_basedir}/{rid}.md").exists():
                raise ValueError(
                    "Markdown file could not be generated for PDF"
                )
            convert.md_to_pdf(f"{_basedir}/{rid}.md", f"{_basedir}/{rid}.pdf")
            return Path(f"{_basedir}/{rid}.pdf")

        if format == "html":
            if Path(f"{_basedir}/{rid}.mdx").exists():
                convert.mdx_to_html(
                    f"{_basedir}/{rid}.mdx", f"{_basedir}/{rid}.html"
                )
                return Path(f"{_basedir}/{rid}.html")

            if not Path(f"{_basedir}/{rid}.md").exists():
                self.render(context, "md", rid)
            if not Path(f"{_basedir}/{rid}.md").exists():
                raise ValueError(
                    "Markdown file could not be generated for HTML"
                )
            convert.md_to_html(
                f"{_basedir}/{rid}.md", f"{_basedir}/{rid}.html"
            )
            return Path(f"{_basedir}/{rid}.html")

        raise ValueError(f"Unsupported format: {format}")

    def render_with_template(self, format, context):
        environment = Environment(
            loader=PackageLoader("app.reports.portfolio", "templates")
        )
        template_spec = self.spec["templates"][format]
        template = environment.get_template(template_spec)
        return template.render(context)


def defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: defaultdict_to_dict(v) for k, v in d.items()}
    return d
