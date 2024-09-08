docs:
	$(shell command -v python3 || command -v python) -m venv env
	. env/bin/activate && pip install --upgrade cmw
	. env/bin/activate && cmw docs-src docs
	echo authbase.org > docs/CNAME
release:
	rm -rf dist
	$(shell command -v python3 || command -v python) -m build
	$(shell command -v python3 || command -v python) -m twine upload dist/*
