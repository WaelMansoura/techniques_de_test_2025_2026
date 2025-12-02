"""Tests unitaires pour le module binary_format."""

import pytest
from triangulator.binary_format import (
    serialize_pointset,
    deserialize_pointset,
    serialize_triangles,
    deserialize_triangles,
)


# Tests de sérialisation PointSet
def test_serialize_empty_pointset():
    """Test avec une liste vide."""
    result = serialize_pointset([])
    # TODO: vérifier que result fait 4 bytes à zéro
    assert False, "Test non implémenté"


def test_serialize_single_point():
    """Test avec un seul point."""
    result = serialize_pointset([(1.0, 2.0)])
    # TODO: vérifier la structure binaire
    assert False, "Test non implémenté"


def test_serialize_multiple_points():
    """Test avec plusieurs points."""
    result = serialize_pointset([(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)])
    # TODO: vérifier longueur et contenu
    assert False, "Test non implémenté"


def test_serialize_negative_coordinates():
    """Test avec des coordonnées négatives."""
    result = serialize_pointset([(-1.5, -2.5)])
    # TODO: vérifier que les négatifs sont bien gérés
    assert False, "Test non implémenté"


def test_serialize_float_precision():
    """Test de précision des floats."""
    result = serialize_pointset([(1.123456, 2.789012)])
    # TODO: vérifier la précision
    assert False, "Test non implémenté"


# Tests de désérialisation PointSet
def test_deserialize_empty_pointset():
    """Test désérialisation liste vide."""
    # TODO: créer 4 bytes à zéro
    data = b'\x00\x00\x00\x00'
    result = deserialize_pointset(data)
    assert result == [], "Devrait retourner une liste vide"


def test_deserialize_single_point():
    """Test désérialisation d'un point."""
    # TODO: construire les bytes pour un point
    assert False, "Test non implémenté"


def test_roundtrip_pointset():
    """Test que serialize puis deserialize retourne l'original."""
    original = [(1.0, 2.0), (3.0, 4.0)]
    serialized = serialize_pointset(original)
    result = deserialize_pointset(serialized)
    assert result == original, "Le roundtrip devrait être identique"


def test_deserialize_invalid_length():
    """Test avec des données tronquées."""
    invalid_data = b'\x01\x00\x00\x00\xff'  # Dit 1 point mais pas assez de bytes
    with pytest.raises(ValueError):
        deserialize_pointset(invalid_data)


def test_deserialize_corrupted_data():
    """Test avec des données corrompues."""
    corrupted = b'\xff\xff\xff\xff'
    # TODO: déterminer le comportement attendu
    assert False, "Test non implémenté"


# Tests de sérialisation Triangles
def test_serialize_empty_triangles():
    """Test triangles vides."""
    result = serialize_triangles([], [])
    # TODO: vérifier la structure minimale
    assert False, "Test non implémenté"


def test_serialize_single_triangle():
    """Test un seul triangle."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = [(0, 1, 2)]
    result = serialize_triangles(vertices, triangles)
    # TODO: vérifier la structure
    assert False, "Test non implémenté"


def test_serialize_multiple_triangles():
    """Test plusieurs triangles."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = [(0, 1, 2), (0, 2, 3)]
    result = serialize_triangles(vertices, triangles)
    # TODO: vérifier
    assert False, "Test non implémenté"


def test_serialize_vertices_and_indices():
    """Test que les deux parties sont correctes."""
    vertices = [(1.0, 2.0)]
    triangles = [(0, 0, 0)]
    result = serialize_triangles(vertices, triangles)
    # TODO: vérifier les deux parties séparément
    assert False, "Test non implémenté"


# Tests de désérialisation Triangles
def test_deserialize_empty_triangles():
    """Test désérialisation triangles vides."""
    # TODO: construire les bytes pour 0 vertices et 0 triangles
    assert False, "Test non implémenté"


def test_deserialize_single_triangle():
    """Test désérialisation d'un triangle."""
    assert False, "Test non implémenté"


def test_roundtrip_triangles():
    """Test roundtrip complet."""
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    triangles = [(0, 1, 2)]
    serialized = serialize_triangles(vertices, triangles)
    result_vertices, result_triangles = deserialize_triangles(serialized)
    assert result_vertices == vertices
    assert result_triangles == triangles


def test_deserialize_invalid_indices():
    """Test avec des indices hors limites."""
    # TODO: construire des données avec indices invalides
    assert False, "Test non implémenté"