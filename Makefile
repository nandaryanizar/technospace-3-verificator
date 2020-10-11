serve-development:
	uvicorn server:app --reload

serve-production:
	gunicorn -k uvicorn.workers.UvicornWorker server:app