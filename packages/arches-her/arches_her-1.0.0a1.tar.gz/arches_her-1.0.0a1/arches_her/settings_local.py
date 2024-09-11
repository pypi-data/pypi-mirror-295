ELASTICSEARCH_HOSTS = [{"scheme": "http", "host": "localhost", "port": 9200}]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  #<-- Only need to uncomment this for testing without an actual email server
SEARCH_EXPORT_IMMEDIATE_DOWNLOAD_THRESHOLD = 2000
ACCESSIBILITY_MODE = False