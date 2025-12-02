"""API Flask du service Triangulator."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/triangulation/<pointset_id>', methods=['GET'])
def get_triangulation(pointset_id):
    """
    Endpoint principal de triangulation.
    
    Args:
        pointset_id: UUID du PointSet à trianguler
        
    Returns:
        Response Flask avec les triangles en binaire ou erreur JSON
    """
    return jsonify({"error": "Not implemented"}), 501