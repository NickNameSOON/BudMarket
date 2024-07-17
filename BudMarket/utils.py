from django.urls import get_resolver


def get_all_urls():
    url_patterns = get_resolver().url_patterns
    urls = []

    def collect_urls(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                collect_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
            else:
                full_url = prefix + pattern.pattern.regex.pattern
                full_url = full_url.replace('^', '').replace('$', '')
                urls.append(full_url)

    collect_urls(url_patterns)
    return urls
