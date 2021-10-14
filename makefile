# Make File

VIRTUALENV = $(shell which virtualenv)

clean: shutdown
	rm -fr venv

venv:
	$(VIRTUALENV) venv

install: clean venv
	. venv/bin/activate; pip install -r requirements.txt

launch: venv shutdown
	. venv/bin/activate; python  discount_generator.py &
	. venv/bin/activate; python  discount_provider.py &

shutdown:
	ps -ef | grep "discount_provider.py" | grep -v grep | awk '{print $$2}' | xargs kill  
	ps -ef | grep "discount_generator.py" | grep -v grep | awk '{print $$2}' | xargs kill

