from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article

app = Flask(__name__)

# REQUIRED for sessions
app.secret_key = "super-secret-key"

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    # initialize page views if not present
    session['page_views'] = session['page_views'] if 'page_views' in session else 0

    # increment page views
    session['page_views'] += 1

    # enforce paywall
    if session['page_views'] > 3:
        return jsonify({
            'message': 'Maximum pageview limit reached'
        }), 401

    # fetch article
    article = Article.query.get(id)

    if not article:
        return jsonify({'error': 'Article not found'}), 404

    return jsonify(article.to_dict()), 200


@app.route('/clear', methods=['DELETE'])
def clear_session():
    session.clear()
    return {}, 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)
