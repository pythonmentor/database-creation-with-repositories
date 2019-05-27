class ProductDownloader:
    """Objet responsable de télécharger des produits d'une catégories à partir
    de Openfoodfacts.
    """

    def fetch(self, category, number=20):
        """Récupère un nombre de produits donné depuis l'API.
        
        Args:
            category (str): catégorie des produits à récupérer.
            number (int, optionel): nombre de produits à récupérer. Défaut: 20.
            
        """
        payload = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": number,
            "json": 1,
        }

        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params=payload)
        data = response.json()
        return data['products']