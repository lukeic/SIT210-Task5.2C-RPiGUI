.PHONY: app

app:
	python3 LightToggler.py

ui:
	pyuic5 LightToggler.ui -o UI.py

