import logging
import re
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.six.moves.urllib.parse import urlparse
import requests
import json

logger = logging.getLogger('django')

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
# The repository to add this issue to
REPO_OWNER = 'tarunbehal'
REPO_NAME = 'cores'
ACCESS_TOKEN = '019b58c5ac71c8779f46f16e2311d67443488c0b'


def git_managers(subject, message, fail_silently=True):
    labels = getattr(settings, 'GBT_ISSUE_LABEL', None)
    issue = {
        'title': subject,
        'body': message,
        'labels': labels
    }
    url = 'https://api.github.com/repos/%s/%s/issues' % (settings.GBT_REPO_OWNER, settings.GBT_REPO_NAME)
    r = requests.post(
            url,
            json.dumps(issue),
            headers={'Authorization': 'token {}'.format(settings.GBT_ACCESS_TOKEN)}
    )
    if r.status_code == 201:
        msg = 'Successfully created Issue "%s"' % subject
        logger.info(msg)
        return True, msg
    else:
        msg = 'Could not create Issue "%s" \n Response "s"' % subject, r.content
        if not fail_silently:
            logger.error(msg)
            raise msg
        return False, msg


class GitIssueTrackMiddleware(object):

    def test_git_config(self):
        if all([
            getattr(settings, 'GBT_REPO_OWNER', None),
            getattr(settings, 'GBT_REPO_NAME', None),
            getattr(settings, 'GBT_ACCESS_TOKEN', None),
        ]):
            return True
        logger.warning('Missing configuration related to REPO_OWNER, REPO_NAME and ACCESS_TOKEN')
        return False

    def process_response(self, request, response):
        """
        Create git issues for relevant 404 NOT FOUND responses.
        """
        GBT_ENABLED = getattr(settings, 'GBT_ENABLED', False)
        if response.status_code == 404 and self.test_git_config() and GBT_ENABLED:
            domain = request.get_host()
            path = request.get_full_path()
            referer = force_text(request.META.get('HTTP_REFERER', ''), errors='replace')

            if not self.is_ignorable_request(request, path, domain, referer):
                ua = force_text(request.META.get('HTTP_USER_AGENT', '<none>'), errors='replace')
                ip = request.META.get('REMOTE_ADDR', '<none>')
                git_managers(
                    "Broken %slink on [%s] url path [%s]" % (
                        ('INTERNAL ' if self.is_internal_request(domain, referer) else ''),
                        domain,
                        path
                    ),
                    "Referrer: %s\nRequested URL: %s\nUser agent: %s\n"
                    "IP address: %s\n" % (referer, path, ua, ip),
                    fail_silently=True
                )
        return response

    def is_internal_request(self, domain, referer):
        """
        Returns True if the referring URL is the same domain as the current request.
        """
        # Different subdomains are treated as different domains.
        return bool(re.match("^https?://%s/" % re.escape(domain), referer))

    def is_ignorable_request(self, request, uri, domain, referer):
        """
        Return True if the given request *shouldn't* notify the site managers
        according to project settings or in three specific situations:
         - If the referer is empty.
         - If a '?' in referer is identified as a search engine source.
         - If the referer is equal to the current URL, ignoring the scheme
           (assumed to be a poorly implemented bot).
        """
        GBT_DEBUG_MODE = getattr(settings, 'GBT_DEBUG_MODE', False)
        
        if GBT_DEBUG_MODE:
            return True
        if not referer:
            return True

        if not self.is_internal_request(domain, referer) and '?' in referer:
            return True

        parsed_referer = urlparse(referer)
        if parsed_referer.netloc in ['', domain] and parsed_referer.path == uri:
            return True

        return any(pattern.search(uri) for pattern in settings.IGNORABLE_404_URLS)
