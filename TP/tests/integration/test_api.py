"""Tests d'intégration pour l'API Flask."""

import pytest
from unittest.mock import Mock, patch
from triangulator.app import app


@pytest.fixture
def client():
    """Fixture qui crée un client de test Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch('triangulator.app.PointSetManagerClient')
def test_api_triangulate_success(mock_client_class, client):
    """Test complet du endpoint avec un cas nominal."""
    # On mock le client HTTP pour éviter de vraies requêtes
    mock_client = Mock()
    mock_client.get_pointset.return_value = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    mock_client_class.return_value = mock_client
    
    response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
    
    # Devrait retourner 200 avec du binaire
    assert response.status_code == 200
    assert response.content_type == 'application/octet-stream'
    # TODO: vérifier le contenu binaire
    assert False, "Test non implémenté"


def test_api_triangulate_empty_pointset(client):
    """Test avec un PointSet vide."""
    # TODO: mocker pour retourner une liste vide
    assert False, "Test non implémenté"


@patch('triangulator.app.PointSetManagerClient')
def test_api_triangulate_pointset_not_found(mock_client_class, client):
    """Test avec un UUID qui n'existe pas."""
    mock_client = Mock()
    # On simule que le PointSetManager retourne 404
    mock_client.get_pointset.side_effect = Exception("Not found")
    mock_client_class.return_value = mock_client
    
    response = client.get('/triangulation/unknown-uuid')
    
    # Devrait retourner 404 avec un JSON d'erreur
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert 'code' in data
    assert 'message' in data


def test_api_triangulate_invalid_uuid(client):
    """Test avec un UUID malformé."""
    response = client.get('/triangulation/pas-un-uuid')
    
    # Devrait retourner 400
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert 'code' in data
    assert 'message' in data


@patch('triangulator.app.PointSetManagerClient')
def test_api_triangulate_psm_unavailable(mock_client_class, client):
    """Test quand le PointSetManager est indisponible."""
    mock_client = Mock()
    # Simuler que le service est down
    mock_client.get_pointset.side_effect = ConnectionError("Service unavailable")
    mock_client_class.return_value = mock_client
    
    response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
    
    # Devrait retourner 503
    assert response.status_code == 503
    assert response.content_type == 'application/json'


@patch('triangulator.app.triangulate')
def test_api_triangulate_internal_error(mock_triangulate, client):
    """Test quand l'algorithme de triangulation échoue."""
    # Simuler une erreur dans l'algo
    mock_triangulate.side_effect = RuntimeError("Triangulation failed")
    
    response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
    
    # Devrait retourner 500
    assert response.status_code == 500
    assert response.content_type == 'application/json'


def test_api_wrong_http_method(client):
    """Test avec un mauvais verbe HTTP."""
    # On essaie POST au lieu de GET
    response = client.post('/triangulation/123e4567-e89b-12d3-a456-426614174000')
    
    # Devrait retourner 405 (Method Not Allowed)
    assert response.status_code == 405


def test_api_response_content_type(client):
    """Vérifie que le Content-Type est correct dans différents cas."""
    # Succès : devrait être application/octet-stream
    # Erreur : devrait être application/json
    # TODO: tester les deux cas
    assert False, "Test non implémenté"