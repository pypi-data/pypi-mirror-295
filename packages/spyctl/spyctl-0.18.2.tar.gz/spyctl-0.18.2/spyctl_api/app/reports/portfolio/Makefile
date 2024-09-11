.PHONY: samples tests clean

clean:
	@echo "Cleaning up..."
	rm -f samples/sample*

samples:
	@echo "Generating samples..."
	for spec in samples/spec-*; do \
			echo "Generating sample for $$spec"; \
			PYTHONPATH=../../.. python -m app.reports.portfolio.make --spec $$spec --org KNUJF8M43WcT2o1qgEts --api_key $$API_KEY --api_url $$API_URL --output samples/sample --formats md,mdx ;  \
		done

