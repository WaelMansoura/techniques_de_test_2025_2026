# Plan de Tests - Triangulator Service

**Étudiant** : Wael MANSOURA  
**Groupe** : M1 ILSEN classique

## 1. Objectifs du plan de tests

Ce plan définit les tests à mettre en place **avant** l'implémentation du service Triangulator. L'objectif est de :
- Valider la correction de l'algorithme de triangulation
- Garantir la conformité à l'API OpenAPI (triangulator.yml)
- Assurer la robustesse face aux erreurs
- Mesurer les performances
- Atteindre 100% de couverture de code

## 2. Architecture du code à tester

### 2.1 Structure réalisée
```
TP/
├── triangulator/
│   ├── __init__.py
│   ├── app.py                 # API Flask
│   ├── binary_format.py       # Sérialisation/désérialisation binaire
│   ├── triangulation.py       # Algorithme de triangulation
│   └── pointset_client.py     # Client HTTP pour PointSetManager
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_binary_format.py
│   │   ├── test_triangulation.py
│   │   └── test_pointset_client.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── performance/
│       ├── __init__.py
│       └── test_perf.py
├── Makefile
├── pytest.ini
├── PLAN.md
├── requirements.txt
├── dev_requirements.txt
└── pyproject.toml
```

### 2.2 Responsabilités de chaque module

- **binary_format.py** : Conversion Python ↔ binaire pour PointSet et Triangles
- **triangulation.py** : Algorithme qui calcule les triangles à partir des points
- **pointset_client.py** : Requêtes HTTP vers le PointSetManager
- **app.py** : API Flask exposant GET /triangulation/{pointSetId}

## 3. Tests unitaires

### 3.1 Module binary_format.py (18 tests)

#### Sérialisation PointSet (5 tests)
**Fonction** : `serialize_pointset(points: list[tuple[float, float]]) -> bytes`

Tests implémentés :
1. `test_serialize_empty_pointset()` - Liste vide → 4 bytes à zéro
2. `test_serialize_single_point()` - Un point (1.0, 2.0) → vérifier structure
3. `test_serialize_multiple_points()` - Trois points → vérifier longueur et contenu
4. `test_serialize_negative_coordinates()` - Coordonnées négatives
5. `test_serialize_float_precision()` - Vérifier précision des floats

**Pourquoi ?** Le format binaire est critique : toute erreur rend les données illisibles.

#### Désérialisation PointSet (5 tests)
**Fonction** : `deserialize_pointset(data: bytes) -> list[tuple[float, float]]`

Tests implémentés :
1. `test_deserialize_empty_pointset()` - 4 bytes zéro → []
2. `test_deserialize_single_point()` - Bytes valides → [(1.0, 2.0)]
3. `test_roundtrip_pointset()` - deserialize(serialize(points)) == points
4. `test_deserialize_invalid_length()` - Données tronquées → ValueError
5. `test_deserialize_corrupted_data()` - Données corrompues → ValueError

**Pourquoi ?** Valider la réversibilité et la robustesse face à des données invalides.

#### Sérialisation Triangles (4 tests)
**Fonction** : `serialize_triangles(vertices, triangles) -> bytes`

Tests implémentés :
1. `test_serialize_empty_triangles()` - Aucun triangle → structure minimale
2. `test_serialize_single_triangle()` - Un triangle (indices 0,1,2)
3. `test_serialize_multiple_triangles()` - Plusieurs triangles
4. `test_serialize_vertices_and_indices()` - Vérifier les deux parties du format

**Pourquoi ?** Le format Triangles est plus complexe (2 parties), nécessite des tests approfondis.

#### Désérialisation Triangles (4 tests)
**Fonction** : `deserialize_triangles(data: bytes) -> tuple[list, list]`

Tests implémentés :
1. `test_deserialize_empty_triangles()` - Structure minimale → ([], [])
2. `test_deserialize_single_triangle()` - Bytes → (vertices, [(0,1,2)])
3. `test_roundtrip_triangles()` - Vérifier l'idempotence
4. `test_deserialize_invalid_indices()` - Indices hors limites → ValueError

**Pourquoi ?** Assurer que les indices référencent bien les vertices.

### 3.2 Module triangulation.py (9 tests)

#### Algorithme de triangulation
**Fonction** : `triangulate(points: list[tuple[float, float]]) -> list[tuple[int, int, int]]`

Tests implémentés :
1. `test_triangulate_less_than_3_points()` - 0, 1 ou 2 points → []
2. `test_triangulate_triangle()` - 3 points → 1 triangle
3. `test_triangulate_square()` - 4 points → 2 triangles
4. `test_triangulate_pentagon()` - 5 points → 3 triangles
5. `test_triangulate_complex_polygon()` - 10 points → 8 triangles
6. `test_triangulate_validates_indices()` - Tous les indices sont valides
7. `test_triangulate_correct_count()` - Nombre de triangles = n-2 (pour n points)
8. `test_triangulate_collinear_points()` - Points alignés → gestion appropriée
9. `test_triangulate_duplicate_points()` - Points identiques → exception

**Pourquoi ?** L'algorithme est le cœur du service, il doit être correct mathématiquement.

**Comment tester ?**
- Vérifier le nombre de triangles : pour n points → (n-2) triangles
- Vérifier que tous les indices sont dans [0, n-1]
- Vérifier que tous les points sont utilisés
- Gérer les cas dégénérés (points colinéaires, doublons)

### 3.3 Module pointset_client.py (5 tests)

#### Client HTTP
**Classe** : `PointSetManagerClient`

Tests implémentés avec mocks :
1. `test_get_pointset_success()` - Requête réussie (200) → PointSet désérialisé
2. `test_get_pointset_not_found()` - ID inexistant (404) → Exception
3. `test_get_pointset_service_unavailable()` - Service down (503) → Exception
4. `test_get_pointset_timeout()` - Timeout réseau → Exception
5. `test_get_pointset_invalid_binary()` - Données corrompues → ValueError

**Pourquoi ?** Le client doit gérer toutes les erreurs HTTP possibles.

**Comment ?** Utiliser `unittest.mock` pour mocker les requêtes HTTP avec `@patch`.

## 4. Tests d'intégration (8 tests)

### 4.1 API Flask (test_api.py)

#### Endpoint GET /triangulation/{pointSetId}

Tests implémentés :
1. `test_api_triangulate_success()` - Requête complète avec mock → 200 + binaire
2. `test_api_triangulate_empty_pointset()` - 0 points → 200 + résultat vide
3. `test_api_triangulate_pointset_not_found()` - UUID invalide → 404 + JSON
4. `test_api_triangulate_invalid_uuid()` - UUID malformé → 400 + JSON
5. `test_api_triangulate_psm_unavailable()` - Service down → 503 + JSON
6. `test_api_triangulate_internal_error()` - Erreur algorithme → 500 + JSON
7. `test_api_wrong_http_method()` - POST au lieu de GET → 405
8. `test_api_response_content_type()` - Vérifier Content-Type correct

**Pourquoi ?** Valider la conformité à la spec OpenAPI (triangulator.yml).

**Comment ?** 
- Utiliser `flask.test_client()`
- Mocker le PointSetManagerClient
- Vérifier les status codes et les formats de réponse

## 5. Tests de performance (5 tests)

### 5.1 Benchmarks (test_perf.py)

Tests implémentés (marqués `@pytest.mark.perf`) :
1. `test_perf_triangulate_100_points()` - Temps < 100ms
2. `test_perf_triangulate_1000_points()` - Temps < 2s
3. `test_perf_triangulate_10000_points()` - Temps < 60s
4. `test_perf_serialize_large_pointset()` - 10000 points
5. `test_perf_deserialize_large_pointset()` - 10000 points

**Pourquoi ?** Identifier les régressions de performance.

**Comment ?** Utiliser `time.perf_counter()` et définir des seuils acceptables.

## 6. Configuration

### 6.1 pytest.ini
```ini
[pytest]
markers =
    unit: Tests unitaires rapides
    integration: Tests d'intégration
    perf: Tests de performance (lents)
testpaths = tests
```

### 6.2 Makefile
```makefile
.PHONY: test unit_test perf_test coverage lint doc

test:
	pytest tests/

unit_test:
	pytest -m "not perf" tests/

perf_test:
	pytest -m perf tests/performance/

coverage:
	coverage run -m pytest -m "not perf" tests/
	coverage report
	coverage html

lint:
	ruff check .

doc:
	pdoc3 --html --output-dir docs --force triangulator
```

## 7. Stratégie de développement

### Phase 1 : Implémentation des tests (séances 2-4) ✅
1. ✅ Créer tous les fichiers de tests
2. ✅ Écrire tous les tests (43 tests au total)
3. ✅ Mettre en place les fixtures et mocks
4. ✅ Configurer pytest, Makefile, et tous les outils
5. **Rendu 2** : Tous les tests en place et exécutables

**État actuel (fin séance 4)** :
- 43 tests créés et exécutables
- 2 tests passent (ceux avec des assertions complètes)
- 41 tests échouent avec `NotImplementedError` ou `assert False` (comportement attendu)
- Tous les outils configurés et fonctionnels (pytest, coverage, ruff, pdoc3)

### Phase 2 : Implémentation du code 
1. Implémenter binary_format.py pour faire passer les tests
2. Implémenter triangulation.py (algorithme : Ear Clipping)
3. Implémenter pointset_client.py
4. Implémenter app.py (Flask)
5. Ajuster les tests si nécessaire
6. **Rendu 3** : Tous les tests passent, 100% couverture

## 8. Critères de réussite

### Pour le rendu 2 (fin séance 4) ✅
- ✅ Tous les fichiers de tests créés (6 fichiers de tests)
- ✅ Tests exécutables : 43 tests détectés par pytest
- ✅ Fixtures et mocks en place (unittest.mock configuré)
- ✅ Makefile fonctionnel (toutes les commandes testées)
- ✅ pytest.ini et pyproject.toml configurés
- ✅ Structure complète du projet en place

### Pour le rendu 3 (dernière séance)
- ⏳ Tous les tests passent
- ⏳ Couverture ≥ 100%
- ⏳ `ruff check` sans erreur
- ⏳ Documentation générée

## 9. Choix techniques justifiés

### Algorithme de triangulation
**Choix** : Ear Clipping Algorithm

**Pourquoi ?**
- Simple à implémenter
- Facile à tester (résultats prévisibles)
- Complexité O(n²) acceptable pour des datasets < 10000 points

### Format binaire
**Choix** : Little-endian, struct Python

**Pourquoi ?**
- Standard sur la plupart des architectures
- Module `struct` natif Python
- Facile à déboguer avec des valeurs connues

### Mocking HTTP
**Choix** : unittest.mock avec @patch

**Pourquoi ?**
- Inclus dans Python standard
- Permet de simuler tous les cas d'erreur
- Pas de dépendance externe
- Compatible avec pytest

### Framework de tests
**Choix** : pytest

**Pourquoi ?**
- Syntaxe simple et claire
- Système de marqueurs pour catégoriser les tests
- Fixtures puissantes
- Excellente intégration avec coverage

## 10. Statistiques des tests

### Répartition par catégorie
- Tests unitaires binary_format : 18 tests
- Tests unitaires triangulation : 9 tests
- Tests unitaires pointset_client : 5 tests
- Tests d'intégration API : 8 tests
- Tests de performance : 5 tests
- **Total : 45 tests**

### Commandes de lancement
- `make test` : Lance tous les 45 tests
- `make unit_test` : Lance 40 tests (exclut les 5 tests perf)
- `make perf_test` : Lance uniquement les 5 tests de performance
- `make coverage` : Génère rapport de couverture (tests hors perf)
- `make lint` : Vérifie la qualité du code avec ruff
- `make doc` : Génère la documentation HTML

## 11. Risques identifiés et mitigations

| Risque | Mitigation | État |
|--------|-----------|------|
| Algorithme complexe | Commencer simple (Ear Clipping), améliorer si temps | ✅ Planifié |
| Bugs format binaire | Tests exhaustifs avec valeurs calculées manuellement | ✅ Tests en place |
| Tests trop lents | Marqueur `@pytest.mark.perf` pour exclusion | ✅ Implémenté |
| Précision des floats | Utiliser `math.isclose()` pour les comparaisons | ⏳ À implémenter |
| Mocks complexes | Documentation claire des fixtures | ✅ Fait |

## 12. Notes d'implémentation pour les prochaines séances

### Ordre d'implémentation 
1. **binary_format.py** 
   - Commencer par serialize/deserialize PointSet
   - Puis Triangles (plus complexe)
   - Vérifier les 18 tests unitaires

2. **triangulation.py** 
   - Implémenter Ear Clipping Algorithm
   - Gérer les cas limites
   - Vérifier les 9 tests unitaires

3. **pointset_client.py** 
   - Implémenter les requêtes HTTP avec requests
   - Gérer tous les codes d'erreur
   - Vérifier les 5 tests unitaires

4. **app.py** 
   - Connecter tous les modules
   - Implémenter la gestion d'erreurs
   - Vérifier les 8 tests d'intégration

5. **Optimisation** 
   - Lancer les tests de performance
   - Optimiser si nécessaire
   - Finaliser la documentation

### Ressources techniques
- Documentation struct : https://docs.python.org/3/library/struct.html
- Ear Clipping : algorithme simple de triangulation pour polygones convexes
- Flask testing : https://flask.palletsprojects.com/en/latest/testing/
- unittest.mock : https://docs.python.org/3/library/unittest.mock.html

---

**Document révisé le** : Fin de séance 4  
**Prochaine étape** : Implémentation du code