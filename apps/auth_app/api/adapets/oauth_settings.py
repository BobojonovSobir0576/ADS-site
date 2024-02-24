import os


REDIRECT_URL = os.environ.get("SOCIAL_MEDIA_REDIRECT_URL", "https://example.com")

GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID", '409261742060-ia3molca8tcmm7c7dci610233u02eqbd.apps.googleusercontent.com'
)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", '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')