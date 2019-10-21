help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  clean                      delete generated byte code and coverage reports"
	@echo "  help                       display this help message"
	@echo "  migrate                    apply database migrations"
	@echo "  prod_requirements          install production requirements for django-rest-blog-app-backend python3 environment"
	@echo "  quality                    check code quality for django-rest-blog-app-backend"
	@echo "  requirements               install local requirements for django-rest-blog-app-backend python3 environment"
	@echo "  serve                      serve django-rest-blog-app-backend at 0.0.0.0:8000"
	@echo "  static                     build and compress static assets"
	@echo "  test                       run tests"
	@echo "  html_coverage              open code coverage in browser as HTML document"
	@echo ""

clean:
	find . -name '*.pyc' -delete
	coverage erase

quality:
	isort --skip venv --check-only --diff --recursive .
	pycodestyle --exclude='venv','migrations' --config=.pep8 .

requirements:
	pip install -qr requirements/local.txt --exists-action w

prod_requirements:
	pip install -qr requirements/production.txt --exists-action w

static:
	python manage.py collectstatic --noinput

serve:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate --noinput

html_coverage:
	coverage html && open htmlcov/index.html

test: clean
	py.test -vv --nomigrations --cov=webblog --cov-report term --cov-config=.coveragerc

validate: quality test
