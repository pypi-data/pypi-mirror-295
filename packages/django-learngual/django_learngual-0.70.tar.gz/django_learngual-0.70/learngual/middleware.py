import zoneinfo
from logging import getLogger

import pytz
from django.utils import timezone, translation

from .utils import get_language_code

logger = getLogger(__file__)


class TimeZoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz_header = request.headers.get("TZ")

        if tz_header:
            try:
                timezone.activate(tz_header)
            except (pytz.UnknownTimeZoneError, zoneinfo.ZoneInfoNotFoundError):
                logger.error("Invalid timezone %s", tz_header)
                pass  # Handle unknown timezone error here
        else:
            # Set default timezone if TZ header is not provided
            timezone.activate("UTC")

        response = self.get_response(request)
        timezone.deactivate()
        return response


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract language from _lang query parameter
        lang = request.GET.get("_lang")
        logger.info(
            f"language middleware start: {translation.get_language()}\n{lang = }"
        )

        if lang:
            lang = get_language_code(lang).upper()
        if lang:
            # Activate the new language if it's valid
            translation.activate(lang)
        else:
            # Fallback to default language if not valid
            translation.activate("EN")

        logger.info(f"language middleware get response: {translation.get_language()}")
        response = self.get_response(request)
        logger.info(
            f"language middleware after get response: {translation.get_language()}"
        )
        # Restore the original language
        translation.activate("EN")
        logger.info(f"language middleware ends: {translation.get_language()}")
        return response
