from demo.models import Product, Store
from demo.openfoodfacts import ProductDownloader

articles = [
    {
        "article_title": "Mon super article au sujet de A",
        "tags": ["a", "aa", "aaa"],
        "category": "cat-a"
    },
    {
        "article_title": "Mon second super article au sujet de A",
        "tags": ["a", "aa", "aaa"],
        "category": "cat-a"
    },
    {
        "article_title": "Mon super article au sujet de B",
        "tags": ["b", "bb", "bbb"],
        "category": "cat-b"
    },
    {
        "article_title": "Mon second super article au sujet de B",
        "tags": ["b", "bb", "bbb"],
        "category": "cat-b"
    },
    {
        "article_title": "Mon article général au sujet de A et B",
        "tags": ["a", "b", "c"],
        "category": "cat-c"
    },
]

def main():
    for article in articles:
        article = Article.create_from_openfoodfacts(**article)


if __name__ == "__main__":
    main()
