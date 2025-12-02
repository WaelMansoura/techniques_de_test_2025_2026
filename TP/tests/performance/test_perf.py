"""Tests de performance pour les opérations critiques."""

import pytest
import time


@pytest.mark.perf
def test_perf_triangulate_100_points():
    """Triangulation de 100 points devrait prendre moins de 100ms."""
    from triangulator.triangulation import triangulate
    
    # Générer 100 points
    points = [(float(i), float(i * 2)) for i in range(100)]
    
    start = time.perf_counter()
    result = triangulate(points)
    elapsed = time.perf_counter() - start
    
    assert elapsed < 0.1, f"Trop lent : {elapsed:.3f}s pour 100 points"
    assert len(result) == 98, "Devrait avoir 98 triangles"


@pytest.mark.perf
def test_perf_triangulate_1000_points():
    """Triangulation de 1000 points devrait prendre moins de 2s."""
    from triangulator.triangulation import triangulate
    
    points = [(float(i), float(i * 2)) for i in range(1000)]
    
    start = time.perf_counter()
    result = triangulate(points)
    elapsed = time.perf_counter() - start
    
    assert elapsed < 2.0, f"Trop lent : {elapsed:.3f}s pour 1000 points"
    assert len(result) == 998


@pytest.mark.perf
def test_perf_triangulate_10000_points():
    """Triangulation de 10000 points devrait prendre moins de 60s."""
    from triangulator.triangulation import triangulate
    
    points = [(float(i), float(i * 2)) for i in range(10000)]
    
    start = time.perf_counter()
    result = triangulate(points)
    elapsed = time.perf_counter() - start
    
    assert elapsed < 60.0, f"Trop lent : {elapsed:.3f}s pour 10000 points"
    assert len(result) == 9998


@pytest.mark.perf
def test_perf_serialize_large_pointset():
    """Sérialisation d'un gros PointSet."""
    from triangulator.binary_format import serialize_pointset
    
    points = [(float(i), float(i * 2)) for i in range(10000)]
    
    start = time.perf_counter()
    result = serialize_pointset(points)
    elapsed = time.perf_counter() - start
    
    # La sérialisation devrait être rapide (moins d'1 seconde)
    assert elapsed < 1.0, f"Sérialisation trop lente : {elapsed:.3f}s"
    # Vérifier la taille attendue : 4 + (10000 * 8) bytes
    expected_size = 4 + (10000 * 8)
    assert len(result) == expected_size


@pytest.mark.perf
def test_perf_deserialize_large_pointset():
    """Désérialisation d'un gros PointSet."""
    from triangulator.binary_format import serialize_pointset, deserialize_pointset
    
    points = [(float(i), float(i * 2)) for i in range(10000)]
    data = serialize_pointset(points)
    
    start = time.perf_counter()
    result = deserialize_pointset(data)
    elapsed = time.perf_counter() - start
    
    assert elapsed < 1.0, f"Désérialisation trop lente : {elapsed:.3f}s"
    assert len(result) == 10000