from flask import Flask, render_template, request
import requests, re
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "awan12345"

class OtakudesuApi:
    def __init__(self):
        self.header = {'User-Agent': 'user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}
        self.base_url = 'https://otakudesu.cloud/'
        self.api = requests.Session()

    def fetch_ongoing_anime(self, page):
        if page == "1":
            url = f"{self.base_url}ongoing-anime/"
        else:
            url = f"{self.base_url}ongoing-anime/page/{page}/"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            anime_list = []
            detpost_divs = soup.find_all('div', class_='detpost')
            
            for detpost in detpost_divs:
                try:
                    episode = detpost.find('div', class_='epz').text.strip()
                    hari = detpost.find('div', class_='epztipe').text.strip()
                    tanggal = detpost.find('div', class_='newnime').text.strip()
                    judul = detpost.find('h2', class_='jdlflm').text.strip()
                    img_element = detpost.find('img')
                    img_url = img_element['src'] if img_element else None
                    link_element = detpost.find('a')
                    link_url = link_element['href'] if link_element else None
                    if link_url:
                        link_url = link_url.rstrip('/').split('/')[-1] + '/'
                    
                    anime_data = {
                        'episode': episode,
                        'hari': hari,
                        'tanggal': tanggal,
                        'judul': judul,
                        'img_url': img_url,
                        'link_url': link_url
                    }
                    
                    anime_list.append(anime_data)
                    
                except Exception as e:
                    print(f"Error parsing anime item: {e}")
                    continue
            
            pagination_info = {}
            pagination_div = soup.find('div', class_='pagination')
            if pagination_div:
                pagenavix = pagination_div.find('div', class_='pagenavix')
                if pagenavix:
                    current_page = pagenavix.find('span', class_='current')
                    pagination_info['current_page'] = int(current_page.text.strip()) if current_page else 1
                        
                    page_links = []
                    page_numbers = pagenavix.find_all('a', class_='page-numbers')
                    for link in page_numbers:
                        if 'next' not in link.get('class', []):
                            page_links.append({
                            'page': link.text.strip(),
                            'url': link['href'].rstrip('/').split('/')[-1] + '/'
                            })
                        
                    pagination_info['page_links'] = page_links
                        
                    next_link = pagenavix.find('a', class_='next')
                    pagination_info['next_page'] = next_link['href'].rstrip('/').split('/')[-1] + '/' if next_link else None
                    
            return {
                'anime_list': anime_list,
                'pagination': pagination_info
            }
            
        except Exception as e:
            print(f"Error fetching ongoing anime: {e}")
            return []
        
    def fetch_complete_anime(self, page):
        if page == "1":
            url = f"{self.base_url}complete-anime/"
        else:
            url = f"{self.base_url}complete-anime/page/{page}/"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            anime_list = []
            detpost_divs = soup.find_all('div', class_='detpost')
            
            for detpost in detpost_divs:
                try:
                    episode = detpost.find('div', class_='epz').text.strip()
                    hari = detpost.find('div', class_='epztipe').text.strip()
                    tanggal = detpost.find('div', class_='newnime').text.strip()
                    judul = detpost.find('h2', class_='jdlflm').text.strip()
                    img_element = detpost.find('img')
                    img_url = img_element['src'] if img_element else None
                    link_element = detpost.find('a')
                    link_url = link_element['href'] if link_element else None
                    if link_url:
                        link_url = link_url.rstrip('/').split('/')[-1] + '/'
                        
                    anime_data = {
                        'episode': episode,
                        'hari': hari,
                        'tanggal': tanggal,
                        'judul': judul,
                        'img_url': img_url,
                        'link_url': link_url
                    }
                        
                    anime_list.append(anime_data)
                    
                except Exception as e:
                    print(f"Error parsing anime item: {e}")
                    continue
                
            pagination_info = {}
            pagination_div = soup.find('div', class_='pagination')
            if pagination_div:
                pagenavix = pagination_div.find('div', class_='pagenavix')
                if pagenavix:
                    current_page = pagenavix.find('span', class_='current')
                    pagination_info['current_page'] = int(current_page.text.strip()) if current_page else 1
                        
                    page_links = []
                    page_numbers = pagenavix.find_all('a', class_='page-numbers')
                    for link in page_numbers:
                        if 'next' not in link.get('class', []):
                            page_links.append({
                            'page': link.text.strip(),
                            'url': link['href'].rstrip('/').split('/')[-1] + '/'
                            })
                        
                    pagination_info['page_links'] = page_links
                        
                    next_link = pagenavix.find('a', class_='next')
                    pagination_info['next_page'] = next_link['href'].rstrip('/').split('/')[-1] if next_link else None
                    
            return {
                'anime_list': anime_list,
                'pagination': pagination_info
            }
            
        except Exception as e:
            print(f"Error fetching complete anime: {e}")
            return {'anime_list': [], 'pagination': {}}
        
    def fetch_anime_release_schedule(self):
        url = f"{self.base_url}jadwal-rilis/"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            schedule = {}
            kglist_divs = soup.find_all('div', class_='kglist321')
            
            for div in kglist_divs:
                try:
                    day = div.find('h2').text.strip()
                    
                    anime_list = []
                    ul_element = div.find('ul')
                    if ul_element:
                        li_elements = ul_element.find_all('li')
                        for li in li_elements:
                            a_element = li.find('a')
                            if a_element:
                                anime_data = {
                                    'title': a_element.text.strip(),
                                    'url': a_element['href'].rstrip('/').split('/')[-1] + '/'
                                }
                                anime_list.append(anime_data)
                    
                    schedule[day] = anime_list
                    
                except Exception as e:
                    print(f"Error parsing schedule item: {e}")
                    continue
            
            return schedule
            
        except Exception as e:
            print(f"Error fetching anime schedule: {e}")
            return {}
        
    def fetch_anime_genres(self):
        url = f"{self.base_url}genre-list/"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            genres = []
            genres_ul = soup.find('ul', class_='genres')
            
            if genres_ul:
                li_elements = genres_ul.find_all('li')
                for li in li_elements:
                    a_elements = li.find_all('a')
                    for a in a_elements:
                        try:
                            genre_name = a.text.strip()
                            genre_url = a['href']
                            
                            genres.append({
                                'name': genre_name,
                                'url': genre_url
                            })
                            
                        except Exception as e:
                            print(f"Error parsing genre item: {e}")
                            continue
            
            return genres
            
        except Exception as e:
            print(f"Error fetching anime genres: {e}")
            return []
        
    def fetch_anime_detail(self, url):
        url = f"{self.base_url}anime/{url}"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            anime_detail = {}

            fotoanime_div = soup.find('div', class_='fotoanime')
            if fotoanime_div:
                img_element = fotoanime_div.find('img')
                if img_element:
                    anime_detail['cover_image'] = img_element.get('src')

            infozin_div = soup.find('div', class_='infozin')
            if infozin_div:
                infozingle_div = infozin_div.find('div', class_='infozingle')
                if infozingle_div:
                    paragraphs = infozingle_div.find_all('p')
                    for p in paragraphs:
                        try:
                            text = p.text.strip()
                            if ':' in text:
                                key, value = text.split(':', 1)
                                key = key.strip().replace('**', '').replace('*', '')
                                value = value.strip()
                                
                                if key == 'Genre':
                                    genres = []
                                    genre_links = p.find_all('a')
                                    for link in genre_links:
                                        genres.append({
                                            'name': link.text.strip(),
                                            'url': link['href']
                                        })
                                    anime_detail['genres'] = genres
                                else:
                                    anime_detail[key.lower()] = value
                        except Exception as e:
                            print(f"Error parsing info item: {e}")
                            continue
            
            sinopc_div = soup.find('div', class_='sinopc')
            if sinopc_div:
                synopsis_paragraphs = sinopc_div.find_all('p')
                synopsis = '\n'.join([p.text.strip() for p in synopsis_paragraphs if p.text.strip()])
                anime_detail['synopsis'] = synopsis
            
            episodes = []
            episodelist_div = soup.find_all('div', class_='episodelist')

            for episodelist_div in episodelist_div:
                ul_element = episodelist_div.find('ul')
                
                if ul_element and ul_element.find_all('li'):
                    li_elements = ul_element.find_all('li')
                    for li in li_elements:
                        try:
                            a_element = li.find('a')
                            date_span = li.find('span', class_='zeebr')

                            if a_element:
                                link_url = a_element['href'].rstrip('/').split('/')[-1] + '/'
                                episode_data = {
                                    'title': a_element.text.strip(),
                                    'url': link_url,
                                    'date': date_span.text.strip() if date_span else None
                                }
                                episodes.append(episode_data)
                        except Exception as e:
                            print(f"Error parsing episode item: {e}")
            
            anime_detail['episodes'] = episodes
            
            return anime_detail
            
        except Exception as e:
            print(f"Error fetching anime detail: {e}")
            return {}
        
    def fetch_watch_anime(self, url):   
        head = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "x-browser-channel": "stable",
            "x-browser-copyright": "Copyright 2025 Google LLC. All rights reserved.",
            "x-browser-validation": "6h3XF8YcD8syi2FF2BbuE2KllQo=",
            "x-browser-year": "2025"
        }
        url = f"{self.base_url}episode/{url}"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = None
            release_time = None
            title_tag = soup.find('h1', class_='posttl')
            if title_tag:
                title = title_tag.text.strip()

            kategoz_spans = soup.select('.kategoz span')
            for span in kategoz_spans:
                if 'Release on' in span.text:
                    release_time = span.text.replace('Release on', '').strip()
                    break

            episode_list = []
            select_tag = soup.find('select', id='selectcog')
            if select_tag:
                options = select_tag.find_all('option')
                for option in options:
                    ep_value = option.get('value', '')
                    ep_text = option.text.strip()

                    if ep_value == '0':
                        continue

                    ep_slug = ep_value.rstrip('/').split('/')[-1] + '/'
                    episode_list.append({
                        'title': ep_text,
                        'slug': ep_slug,
                        'url': ep_value
                    })

            file_url = None
            embed_holder = soup.find('div', id='embed_holder')
            if embed_holder:
                iframe = embed_holder.find('iframe')
                if iframe and iframe.has_attr('src'):
                    embed_url = iframe['src']

                    try:
                        data = self.api.get(embed_url, headers=head)
                        data.raise_for_status()
                        embed_soup = BeautifulSoup(data.text, 'html.parser')
                        script_tags = embed_soup.find_all('script')

                        for script in script_tags:
                            if script.string and 'var vs' in script.string:
                                match = re.search(r'file\s*:\s*"([^"]+)"', script.string)
                                if match:
                                    file_url = match.group(1)
                                    break
                    except Exception as e:
                        print(f"Error fetching embed video: {e}")
                        file_url = None

            download_links = []
            download_div = soup.find('div', class_='download')
            if download_div:
                li_elements = download_div.find_all('li')
                for li in li_elements:
                    try:
                        strong_tag = li.find('strong')
                        if strong_tag:
                            resolution_text = strong_tag.text.strip()

                            if 'Mp4' not in resolution_text:
                                continue

                            reso_match = re.search(r'(\d{3,4}p)', resolution_text)
                            reso = reso_match.group(1) if reso_match else None

                            links = li.find_all('a')
                            pixeldrain_url = None
                            gofile_url = None

                            for link in links:
                                href = link.get('href', '')

                                if 'pixeldrain.com' in href:
                                    match = re.search(r'/([a-zA-Z0-9]+)$', href)
                                    if match:
                                        file_id = match.group(1)
                                        pixeldrain_url = f'https://pixeldrain.com/api/file/{file_id}'

                                elif 'gofile.io' in href:
                                    gofile_url = href

                            if reso and (pixeldrain_url or gofile_url):
                                download_links.append({
                                    'file_url': file_url,
                                    'reso': reso,
                                    'pixeldrain': pixeldrain_url,
                                    'gofile': gofile_url
                                })
                    except Exception as e:
                        print(f"Error parsing download link: {e}")
                        continue

            if not download_links:
                download_links.append({
                    'file_url': file_url,
                    'reso': 'Unknown',
                    'pixeldrain': 'Unknown',
                    'gofile': 'Unknown'
                })

            info_data = {}
            info_div = soup.find('div', class_='infozin')
            if info_div:
                p_tags = info_div.find_all('p')
                for p in p_tags:
                    span = p.find('span')
                    if span and span.find('b'):
                        label = span.find('b').text.strip(':').lower()
                        value = span.text.split(':', 1)[-1].strip()
                        info_data[label] = value


            return {
                'title': title,
                'release_time': release_time,
                'download_links': download_links,
                'episodes': episode_list,
                'info': info_data
            }

        except Exception as e:
            print(f"Error fetching watch anime: {e}")
            return {}
        
    def fetch_search_anime(self, query):
        url = f"{self.base_url}?s={query}&post_type=anime"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            search_results = []
            chivsrc_ul = soup.find('ul', class_='chivsrc')
            
            if chivsrc_ul:
                li_elements = chivsrc_ul.find_all('li')
                for li in li_elements:
                    try:
                        img_element = li.find('img')
                        cover_url = img_element['src'] if img_element else None
                        
                        h2_element = li.find('h2')
                        title = None
                        anime_url = None
                        if h2_element:
                            a_element = h2_element.find('a')
                            if a_element:
                                title = a_element.text.strip()
                                anime_url = a_element['href'].rstrip('/').split('/')[-1] + '/'
                        
                        genres = []
                        set_divs = li.find_all('div', class_='set')
                        for div in set_divs:
                            if div.find('b') and div.find('b').text.strip() == 'Genres':
                                genre_links = div.find_all('a')
                                for link in genre_links:
                                    genres.append({
                                        'name': link.text.strip(),
                                        'url': link['href'].rstrip('/').split('/')[-1] + '/'
                                    })
                        
                        status = None
                        for div in set_divs:
                            if div.find('b') and div.find('b').text.strip() == 'Status':
                                status = div.text.replace('Status', '').replace(':', '').strip()
                        
                        rating = None
                        for div in set_divs:
                            if div.find('b') and div.find('b').text.strip() == 'Rating':
                                rating = div.text.replace('Rating', '').replace(':', '').strip()
                        
                        if title:
                            anime_data = {
                                'title': title,
                                'url': anime_url,
                                'cover_url': cover_url,
                                'genres': genres,
                                'status': status,
                                'rating': rating
                            }
                            search_results.append(anime_data)
                            
                    except Exception as e:
                        print(f"Error parsing search result item: {e}")
                        continue
            
            return search_results
            
        except Exception as e:
            print(f"Error fetching search results: {e}")
            return []

    def fetch_genre_detail(self, genre_url, page):
        if page == "1":
            url = f"{self.base_url}{genre_url}"
        else:
            url = f"{self.base_url}{genre_url}page{page}"
        try:
            response = self.api.get(url, headers=self.header)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            anime_list = []

            anime_divs = soup.find_all('div', class_='col-anime-con')
            for anime in anime_divs:
                try:
                    title_tag = anime.find('div', class_='col-anime-title').find('a')
                    title = title_tag.text.strip()
                    link = title_tag['href']
                    slug = link.rstrip('/').split('/')[-1] + '/'

                    studio = anime.find('div', class_='col-anime-studio').text.strip()

                    episode = anime.find('div', class_='col-anime-eps').text.strip()

                    rating_div = anime.find('div', class_='col-anime-rating')
                    rating = rating_div.text.strip() if rating_div else None

                    genre_links = anime.find('div', class_='col-anime-genre').find_all('a')
                    genres = [g.text.strip() for g in genre_links]

                    img_tag = anime.find('div', class_='col-anime-cover').find('img')
                    img_url = img_tag['src'] if img_tag else None

                    synopsis_div = anime.find('div', class_='col-synopsis')
                    sinopsis = synopsis_div.get_text(separator="\n", strip=True) if synopsis_div else None

                    date_div = anime.find('div', class_='col-anime-date')
                    release_season = date_div.text.strip() if date_div else None

                    trailer_div = anime.find('div', class_='col-anime-trailer')
                    trailer_link = trailer_div.find('a')['href'] if trailer_div and trailer_div.find('a') else None

                    anime_data = {
                        'judul': title,
                        'slug': slug,
                        'link': link,
                        'studio': studio,
                        'episode': episode,
                        'rating': rating,
                        'genres': genres,
                        'img_url': img_url,
                        'sinopsis': sinopsis,
                        'release_season': release_season,
                        'trailer_link': trailer_link
                    }

                    anime_list.append(anime_data)

                except Exception as e:
                    print(f"Error parsing anime genre item: {e}")
                    continue

            pagination_info = {}
            pagination_div = soup.find('div', class_='pagination')
            if pagination_div:
                pagenavix = pagination_div.find('div', class_='pagenavix')
                if pagenavix:
                    current_page = pagenavix.find('span', class_='current')
                    pagination_info['current_page'] = int(current_page.text.strip()) if current_page else 1
                        
                    page_links = []
                    page_numbers = pagenavix.find_all('a', class_='page-numbers')
                    for link in page_numbers:
                        if 'next' not in link.get('class', []):
                            page_links.append({
                            'page': link.text.strip(),
                            'url': link['href'].rstrip('/').split('/')[-1] + '/'
                            })
                        
                    pagination_info['page_links'] = page_links
                        
                    next_link = pagenavix.find('a', class_='next')
                    pagination_info['next_page'] = next_link['href'].rstrip('/').split('/')[-1] + '/' if next_link else None

            return {
                'anime_list': anime_list,
                'pagination': pagination_info
            }

        except Exception as e:
            print(f"Error fetching genre detail: {e}")
            return []

otaku_api = OtakudesuApi()

@app.route('/')
def index():
    """Home page with latest anime"""
    complete_anime = otaku_api.fetch_complete_anime("1")
    latest_anime = otaku_api.fetch_ongoing_anime("1")
    return render_template('index.html', latest_anime=latest_anime, complete_anime=complete_anime)

@app.route('/genres')
def genres():
    """Anime genres page"""
    genres = otaku_api.fetch_anime_genres()
    return render_template('genres.html', genres=genres)

@app.route('/schedule')
def schedule():
    """Anime release schedule page"""
    schedule = otaku_api.fetch_anime_release_schedule()
    return render_template('schedule.html', schedule=schedule)

@app.route('/ongoing')
def ongoing():
    """Ongoing anime page"""
    page = request.args.get('page', '1', )
    ongoing_anime = otaku_api.fetch_ongoing_anime(page)
    return render_template('ongoing.html', ongoing_anime=ongoing_anime)

@app.route('/complete')
def complete():
    """Complete anime page"""
    page = request.args.get('page', '1', )
    complete_anime = otaku_api.fetch_complete_anime(page)
    return render_template('complete.html', complete_anime=complete_anime)

@app.route('/search')
def search():
    """Search page"""
    keyword = request.args.get('name', '')
    results = None
    
    if keyword:
        results = otaku_api.fetch_search_anime(keyword)
    
    return render_template('search.html', results=results, keyword=keyword)

@app.route('/detail/<path:anime_url>')
def anime_detail(anime_url):
    """Anime detail page"""
    detail = otaku_api.fetch_anime_detail(anime_url)
    return render_template('detail.html', anime=detail, anime_url=anime_url)

@app.route('/watch/<path:episode_url>')
def watch_anime(episode_url):
    """Watch anime episode"""
    selected_reso = request.args.get('reso', '360p')
    stream_data = otaku_api.fetch_watch_anime(episode_url)
    return render_template('watch.html', stream_data=stream_data, episode_url=episode_url, selected_reso=selected_reso)

@app.route('/<path:genre_url>')
def genre_detail(genre_url):
    """Genre detail page showing anime list"""
    page = request.args.get('page', '1', )
    detail_genre = otaku_api.fetch_genre_detail(genre_url, page)
    genres = otaku_api.fetch_anime_genres()
    genre_name = None
    for genre in genres:
        if genre['url'].strip('/') == genre_url.strip('/'):
            genre_name = genre['name']
            break

    if not genre_name:
        genre_name = "Unknown Genre"
    return render_template('genre_detail.html', detail_genre=detail_genre, genre_name=genre_name)

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
