"""Module de sérialisation/désérialisation du format binaire."""


def serialize_pointset(points):
    """
    Sérialise un PointSet en format binaire.
    
    Args:
        points: Liste de tuples (x, y) représentant les points
        
    Returns:
        bytes: Représentation binaire du PointSet
    """
    raise NotImplementedError("serialize_pointset pas encore implémenté")


def deserialize_pointset(data):
    """
    Désérialise un PointSet depuis le format binaire.
    
    Args:
        data: bytes représentant le PointSet
        
    Returns:
        list: Liste de tuples (x, y)
    """
    raise NotImplementedError("deserialize_pointset pas encore implémenté")


def serialize_triangles(vertices, triangles):
    """
    Sérialise des triangles en format binaire.
    
    Args:
        vertices: Liste de tuples (x, y) pour les sommets
        triangles: Liste de tuples (i, j, k) pour les indices
        
    Returns:
        bytes: Représentation binaire des Triangles
    """
    raise NotImplementedError("serialize_triangles pas encore implémenté")


def deserialize_triangles(data):
    """
    Désérialise des triangles depuis le format binaire.
    
    Args:
        data: bytes représentant les Triangles
        
    Returns:
        tuple: (vertices, triangles)
    """
    raise NotImplementedError("deserialize_triangles pas encore implémenté")