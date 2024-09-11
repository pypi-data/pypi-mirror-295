import argparse
import asyncio
import json
import logging
import os
import sys
from app.reports.report import Report
from app.reports.report_engine import ReportEngine
from app.reports.report_lib import ReportInput


async def make_report(rep: Report, api_key: str, api_url: str, engine: ReportEngine):
    logging.basicConfig(
        stream=sys.stdout, format=" %(asctime)s:%(levelname)-8s:%(message)s"
    )
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.INFO)
    logger.info(
        f"Starting report generation job for {rep.id} with input {rep.input}"
    )


    # reports = await engine.make_reports(rep, api_key, api_url)
    reports = await engine.generate_report(rep, api_key, api_url)

    for fmt, path in reports.items():
        if args.output_name:
            if "sample" in args.output_name:
                path = path.rename(f"{args.output_name}-{rep.input.report_id}.{fmt}")
            else:
                path = path.rename(f"{args.output_name}.{fmt}")
        logger.info(f"Generated {fmt} report: {path}, size: {path.stat().st_size}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate reports.")
    parser.add_argument("--json", type=str, help="JSON input for the report")

    parser.add_argument(
        "--spec", type=str, help="Path to the report specification JSON file"
    )
    parser.add_argument(
        "--api_key",
        type=str,
        help="API key",
        default=os.getenv("PROD_API_KEY"),
    )
    parser.add_argument(
        "--api_url",
        type=str,
        help="API URL",
        default="https://api.spyderbat.com",
    )
    parser.add_argument("--org", type=str, help="Organization")
    parser.add_argument(
        "-o", "--output_name", type=str, default="sample", help="Output name"
    )
    parser.add_argument(
        "--formats",
        type=str,
        help="Comma separated list of formats to generate (default: json,yaml,md, mdx,html,pdf)",
        default="json,yaml,md,mdx,html,pdf",
    )
    parser.add_argument(
        "--backend_config",
        type=str,
        help="Backend config to use for storing the report",
        default='{"kind": "simple_file", "dir": "/tmp/reports"}',
    )

    args = parser.parse_args()

    if args.json:
        rep = Report.from_dict(json.loads(args.json))
    else:
        with open(args.spec, "r") as f:
            report_input = json.load(f)
        report_input["org_uid"] = args.org

        ri = ReportInput.model_validate(report_input)
        rep = Report(input=ri, formats=["json", "yaml", "mdx", "html", "pdf"])

    engine = ReportEngine({"backend": json.loads(args.backend_config)})
    asyncio.run(make_report(rep, args.api_key, args.api_url, engine))
