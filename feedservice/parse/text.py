import re
from html.entities import entitydefs


class StripHtmlTags(object):

    def process(self, html):
        """
        Remove HTML tags from a string and replace numeric and
        named entities with the corresponding character, so the
        HTML text can be displayed in a simple text view.
        """
        if html is None:
            return None

        # If we would want more speed, we could make these global
        re_strip_tags = re.compile('<[^>]*>')
        re_unicode_entities = re.compile('&#(\d{2,4});')
        re_html_entities = re.compile('&(.{2,8});')
        re_newline_tags = re.compile('(<br[^>]*>|<[/]?ul[^>]*>|</li>)', re.I)
        re_listing_tags = re.compile('<li[^>]*>', re.I)

        result = html

        # Convert common HTML elements to their text equivalent
        result = re_newline_tags.sub('\n', result)
        result = re_listing_tags.sub('\n * ', result)
        result = re.sub('<[Pp]>', '\n\n', result)

        # Remove all HTML/XML tags from the string
        result = re_strip_tags.sub('', result)
        # Convert numeric XML entities to their unicode character
        result = re_unicode_entities.sub(
            lambda x: chr(int(x.group(1))),
            result)

        # Convert named HTML entities to their unicode character
        result = re_html_entities.sub(
            lambda x: str(entitydefs.get(x.group(1), ''), 'iso-8859-1'),
            result)

        # Convert more than two newlines to two newlines
        result = re.sub('([\r\n]{2})([\r\n])+', '\\1', result)

        return result.strip()


class ConvertMarkdown(object):

    def process(self, html_str):
        import html2text

        try:
            text = html2text.html2text(html_str)
            return text.strip()

        except Exception:
            return ''
