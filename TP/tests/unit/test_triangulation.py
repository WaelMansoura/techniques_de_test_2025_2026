"""Tests unitaires pour le module triangulation."""

import pytest
from triangulator.triangulation import triangulate


def test_triangulate_less_than_3_points():
    """Test avec moins de 3 points, impossible de faire un triangle."""
    # Avec 0 points
    result = triangulate([])
    assert result == [], "0 points devrait retourner une liste vide"
    
    # Avec 1 point
    result = triangulate([(0.0, 0.0)])
    assert result == [], "1 point ne peut pas former de triangle"
    
    # Avec 2 points
    result = triangulate([(0.0, 0.0), (1.0, 0.0)])
    assert result == [], "2 points ne peuvent pas former de triangle"


def test_triangulate_triangle():
    """Test avec exactement 3 points, devrait donner 1 triangle."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    result = triangulate(points)
    # Devrait retourner 1 triangle avec les indices 0, 1, 2
    assert len(result) == 1, "3 points = 1 triangle"
    assert result[0] in [(0, 1, 2), (1, 2, 0), (2, 0, 1), 
                          (0, 2, 1), (2, 1, 0), (1, 0, 2)], "Le triangle doit utiliser les 3 points"


def test_triangulate_square():
    """Test avec 4 points formant un carré, devrait donner 2 triangles."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    result = triangulate(points)
    assert len(result) == 2, "4 points = 2 triangles (formule n-2)"
    # TODO: vérifier que tous les points sont utilisés


def test_triangulate_pentagon():
    """Test avec 5 points formant un pentagone."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.5, 1.0), (0.5, 1.5), (-0.5, 1.0)]
    result = triangulate(points)
    assert len(result) == 3, "5 points = 3 triangles (formule n-2)"


def test_triangulate_complex_polygon():
    """Test avec 10 points."""
    # Créer 10 points en cercle
    import math
    points = []
    for i in range(10):
        angle = 2 * math.pi * i / 10
        x = math.cos(angle)
        y = math.sin(angle)
        points.append((x, y))
    
    result = triangulate(points)
    assert len(result) == 8, "10 points = 8 triangles (formule n-2)"


def test_triangulate_validates_indices():
    """Vérifie que tous les indices sont valides."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    result = triangulate(points)
    
    # Tous les indices doivent être dans [0, 3]
    for triangle in result:
        for idx in triangle:
            assert 0 <= idx < len(points), f"Indice {idx} hors limites"


def test_triangulate_correct_count():
    """Vérifie la formule nombre de triangles = n - 2."""
    for n in [3, 4, 5, 6, 7, 8]:
        points = [(float(i), float(i)) for i in range(n)]
        result = triangulate(points)
        assert len(result) == n - 2, f"Pour {n} points, attendu {n-2} triangles"


def test_triangulate_collinear_points():
    """Test avec des points alignés, cas dégénéré."""
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]
    # Comportement à définir : exception ou résultat vide ?
    # Pour l'instant on teste juste que ça ne crash pas
    try:
        result = triangulate(points)
        # Si ça retourne quelque chose, vérifier que c'est cohérent
        assert isinstance(result, list)
    except ValueError:
        # Acceptable de lever une exception pour des points colinéaires
        pass


def test_triangulate_duplicate_points():
    """Test avec des points identiques."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 0.0)]  # Premier et dernier identiques
    # Comportement à définir
    with pytest.raises((ValueError, Exception)):
        triangulate(points)