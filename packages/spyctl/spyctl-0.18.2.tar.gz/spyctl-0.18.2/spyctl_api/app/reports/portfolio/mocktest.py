from app.reports.reporter import Reporter


class MockReporter(Reporter):
    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list:

        return []

    def processor(
        self,
        data: list,
        args: dict[str, str | float | int | bool],
        mock: dict = {},
        format: str = "md",
    ) -> dict:
        return {"args": args}
