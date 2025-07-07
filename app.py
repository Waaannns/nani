from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import requests, base64
import json
import os
from datetime import datetime
from config import config

app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)

class AnimeAPI:
    def __init__(self):
        self.base_url = app.config.get('ANIMEKITA_API_BASE')
    
    def get_latest_anime(self):
        """Get latest anime releases"""
        try:
            response = requests.get(f"{self.base_url}/terbaru.php")
            if response.status_code == 200:
                return response.json()
            return {"error": "Failed to fetch latest anime"}
        except Exception as e:
            return {"error": str(e)}
    
    def search_anime(self, keyword):
        """Search anime by keyword"""
        try:
            response = requests.get(f"{self.base_url}/search.php", params={"keyword": keyword})
            if response.status_code == 200:
                return response.json()
            return {"error": "Failed to search anime"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_anime_detail(self, url):
        """Get anime detail"""
        try:
            response = requests.get(f"{self.base_url}/series.php", params={"url": url})
            if response.status_code == 200:
                return response.json()
            return {"error": "Failed to fetch anime detail"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_anime_stream(self, url, reso="720p"):
        """Get anime streaming links"""
        try:
            response = requests.get(f"{self.base_url}/chapter.php", params={"url": url, "reso": reso})
            if response.status_code == 200:
                return response.json()
            return {"error": "Failed to fetch streaming links"}
        except Exception as e:
            return {"error": str(e)}

# Initialize API
anime_api = AnimeAPI()

@app.route('/')
def index():
    """Home page with latest anime"""
    latest_anime = anime_api.get_latest_anime()
    return render_template('index.html', latest_anime=latest_anime)

@app.route('/search')
def search():
    """Search page"""
    keyword = request.args.get('name', '')
    results = None
    
    if keyword:
        results = anime_api.search_anime(keyword)
    
    return render_template('search.html', results=results, keyword=keyword)

@app.route('/detail/<path:anime_url>')
def anime_detail(anime_url):
    """Anime detail page"""
    detail = anime_api.get_anime_detail(anime_url)
    return render_template('detail.html', anime=detail, anime_url=anime_url)

@app.route('/watch/<path:episode_url>')
def watch_anime(episode_url):
    """Watch anime episode"""
    selected_reso = request.args.get('reso', '720p')
    stream_data = anime_api.get_anime_stream(episode_url, selected_reso)
    
    return render_template('watch.html', stream_data=stream_data, episode_url=episode_url, selected_reso=selected_reso)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=error), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=error), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error=error), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
