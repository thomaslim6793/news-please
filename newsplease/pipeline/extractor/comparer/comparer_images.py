import re

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# to improve performance, regex statements are compiled only once per module
re_http = re.compile('http://*')

class ComparerImages:
    """This class compares the images of the list of ArticleCandidates and sends the result back to the Comparer."""

    def extract(self, item, list_article_candidate):
        """Compares the extracted images.

        :param item: The corresponding NewscrawlerItem
        :param list_article_candidate: A list of ArticleCandidate objects which have been extracted
        :return: A list of strings (URLs) containing all relevant image URLs
        """
        list_images = []

        for article_candidate in list_article_candidate:
            if article_candidate.images is not None:
                # Resolve relative URLs into absolute ones
                resolved_images = [self.image_absolute_path(item['url'], img) for img in article_candidate.images]
                list_images.append((resolved_images, article_candidate.extractor))

        # If there is no value in the list, return None.
        if len(list_images) == 0:
            return None

        # If there are more options than one, return the result from newspaper.
        list_newspaper = [x for x in list_images if x[1] == "newspaper"]
        if len(list_newspaper) == 0:

            # If there is no topimage extracted by newspaper, return the first result of list_topimage.
            return list_images[0][0]
        else:
            return list_newspaper[0][0]

    def image_absolute_path(self, base_url, image_url):
        """Resolves relative image URLs to absolute URLs using the base URL.

        :param base_url: The base URL of the article
        :param image_url: The URL of the image (relative or absolute)
        :return: The absolute URL of the image
        """
        if not re.match(re_http, image_url):
            return urljoin(base_url, image_url)
        return image_url