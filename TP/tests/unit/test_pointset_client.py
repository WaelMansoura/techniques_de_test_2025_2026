"""Tests unitaires pour le client PointSetManager."""

import pytest
from unittest.mock import Mock, patch
from triangulator.pointset_client import PointSetManagerClient


@pytest.fixture
def client():
    """Fixture qui crée un client pour les tests."""
    return PointSetManagerClient("http://localhost:5000")


@patch('triangulator.pointset_client.requests.get')
def test_get_pointset_success(mock_get, client):
    """Test d'une requête réussie."""
    # On simule une réponse HTTP 200 avec des données binaires valides
    mock_response = Mock()
    mock_response.status_code = 200
    # Données binaires pour 1 point (1.0, 2.0)
    mock_response.content = b'\x01\x00\x00\x00\x00\x00\x80?\x00\x00\x00@'
    mock_get.return_value = mock_response
    
    result = client.get_pointset("123e4567-e89b-12d3-a456-426614174000")
    
    # Vérifier que la requête a été faite
    mock_get.assert_called_once()
    # TODO: vérifier que result contient les bons points désérialisés
    assert False, "Test non implémenté"


@patch('triangulator.pointset_client.requests.get')
def test_get_pointset_not_found(mock_get, client):
    """Test quand le PointSet n'existe pas (404)."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "code": "NOT_FOUND",
        "message": "PointSet not found"
    }
    mock_get.return_value = mock_response
    
    # Devrait lever une exception appropriée
    with pytest.raises(Exception):  # À raffiner avec une exception custom
        client.get_pointset("unknown-id")


@patch('triangulator.pointset_client.requests.get')
def test_get_pointset_service_unavailable(mock_get, client):
    """Test quand le service est down (503)."""
    mock_response = Mock()
    mock_response.status_code = 503
    mock_response.json.return_value = {
        "code": "SERVICE_UNAVAILABLE",
        "message": "Database is unavailable"
    }
    mock_get.return_value = mock_response
    
    with pytest.raises(Exception):
        client.get_pointset("some-id")


@patch('triangulator.pointset_client.requests.get')
def test_get_pointset_timeout(mock_get, client):
    """Test timeout réseau."""
    # On simule un timeout
    import requests
    mock_get.side_effect = requests.Timeout("Connection timeout")
    
    with pytest.raises(requests.Timeout):
        client.get_pointset("some-id")


@patch('triangulator.pointset_client.requests.get')
def test_get_pointset_invalid_binary(mock_get, client):
    """Test avec des données binaires corrompues."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'\xff\xff\xff'  # Données invalides
    mock_get.return_value = mock_response
    
    # Devrait lever ValueError lors de la désérialisation
    with pytest.raises(ValueError):
        client.get_pointset("some-id")