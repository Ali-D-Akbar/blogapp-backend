help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  help                       display this help message"
	@echo "  migrate                    apply database migrations"
	@echo "  prod_requirements          install production requirements for django-rest-blog-app-backend python3 environment"
	@echo "  quality                    check code quality for django-rest-blog-app-backend"
	@echo "  requirements               install local requirements for django-rest-blog-app-backend python3 environment"
	@echo "  serve                      serve django-rest-blog-app-backend at 0.0.0.0:8000"
	@echo "  static                     build and compress static assets"
	@echo "  test                       run tests"
	@echo ""

quality:
	isort --check-only --diff --recursive .

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

test:
	py.test -vv --nomigrations --cov=. --cov-report=html --cov-config=.coveragerc
