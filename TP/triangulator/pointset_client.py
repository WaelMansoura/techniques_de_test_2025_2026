"""Client HTTP pour communiquer avec le PointSetManager."""


class PointSetManagerClient:
    """Client pour interroger le service PointSetManager."""
    
    def __init__(self, base_url):
        """
        Initialise le client.
        
        Args:
            base_url: URL de base du service PointSetManager
        """
        self.base_url = base_url
    
    def get_pointset(self, pointset_id):
        """
        Récupère un PointSet depuis le PointSetManager.
        
        Args:
            pointset_id: UUID du PointSet
            
        Returns:
            list: Liste de tuples (x, y)
        """
        raise NotImplementedError("get_pointset pas encore implémenté")