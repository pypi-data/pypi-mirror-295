publish-roboces:
	uv build
	uvx twine upload dist/* -u $(ROBOCES_REGISTRY_USERNAME) -p $(ROBOCES_REGISTRY_PASSWORD) --repository-url https://git.roboces.dev/api/packages/catalin/pypi

publish-pypi:
	uv build
	uvx twine upload dist/* -u $(PYPI_USERNAME) -p $(PYPI_PASSWORD)

publish:
	make publish-pypi
	make publish-roboces