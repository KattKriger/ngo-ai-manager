import json
import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase


BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_ENVIRONMENT_VARIABLES = (
    "DJANGO_SECRET_KEY",
    "DJANGO_DEBUG",
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "DJANGO_SECURE_SSL_REDIRECT",
    "DJANGO_SECURE_PROXY_SSL_HEADER",
    "DJANGO_SESSION_COOKIE_SECURE",
    "DJANGO_CSRF_COOKIE_SECURE",
    "DJANGO_SESSION_COOKIE_SAMESITE",
    "DJANGO_CSRF_COOKIE_SAMESITE",
)


class SettingsConfigurationTests(SimpleTestCase):
    def load_settings(self, environment):
        env = os.environ.copy()
        for name in SETTINGS_ENVIRONMENT_VARIABLES:
            env.pop(name, None)
        env.update(environment)
        env.pop("DJANGO_SETTINGS_MODULE", None)
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import json; from config import settings; "
                    "print(json.dumps({'debug': settings.DEBUG, "
                    "'hosts': settings.ALLOWED_HOSTS, "
                    "'csrf_origins': settings.CSRF_TRUSTED_ORIGINS, "
                    "'ssl_redirect': settings.SECURE_SSL_REDIRECT, "
                    "'session_secure': settings.SESSION_COOKIE_SECURE, "
                    "'csrf_secure': settings.CSRF_COOKIE_SECURE}))"
                ),
            ],
            cwd=BASE_DIR,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_production_defaults_are_safe(self):
        settings = self.load_settings({"DJANGO_SECRET_KEY": "test-secret"})

        self.assertFalse(settings["debug"])
        self.assertEqual(settings["hosts"], [])
        self.assertEqual(settings["csrf_origins"], [])
        self.assertTrue(settings["ssl_redirect"])
        self.assertTrue(settings["session_secure"])
        self.assertTrue(settings["csrf_secure"])

    def test_local_environment_can_be_configured(self):
        settings = self.load_settings(
            {
                "DJANGO_SECRET_KEY": "test-secret",
                "DJANGO_DEBUG": "true",
                "DJANGO_ALLOWED_HOSTS": "localhost, 127.0.0.1",
                "DJANGO_CSRF_TRUSTED_ORIGINS": "http://localhost:8000",
            }
        )

        self.assertTrue(settings["debug"])
        self.assertEqual(settings["hosts"], ["localhost", "127.0.0.1"])
        self.assertEqual(settings["csrf_origins"], ["http://localhost:8000"])
        self.assertFalse(settings["ssl_redirect"])
        self.assertFalse(settings["session_secure"])
        self.assertFalse(settings["csrf_secure"])

# Create your tests here.
