import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langdetect import detect, LangDetectException
from concurrent.futures import ThreadPoolExecutor
import threading

RATING_MAP = {
    'rated-1': 0.5,
    'rated-2': 1.0,
    'rated-3': 1.5,
    'rated-4': 2.0,
    'rated-5': 2.5,
    'rated-6': 3.0,
    'rated-7': 3.5,
    'rated-8': 4.0,
    'rated-9': 4.5,
    'rated-10': 5.0
}

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': 'https://letterboxd.com/'
}

def url_generator(base_url):
    i = 1
    while True:
        yield urljoin(base_url, f"page/{i}/")
        i += 1

def worker(url_gen, shared_data, lock):
    while True:
        with lock:
            if shared_data['page_count'] >= shared_data['max_pages'] or shared_data['comment_count'] >= shared_data['max_comments']:
                return
            url = next(url_gen)
            shared_data['page_count'] += 1

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
            break

        # Extrai nome do filme apenas na primeira página
        title_tag = soup.find('h1', class_='headline-2 prettify')
        if title_tag:
            movie_title = title_tag.find('a').text.strip()
        else:
            movie_title = "N/A"

        review_elements = soup.find_all('li', class_='film-detail')
        if not review_elements:
            break

        comments = []
        for review in review_elements:
            try:
                username_tag = review.find('a', class_='avatar')
                username = username_tag['href'].split('/')[-2] if username_tag else "N/A"

                rating_tag = review.find('span', class_='rating')
                rating_class = [c for c in rating_tag['class'] if c.startswith('rated-')][0] if rating_tag else None
                numeric_rating = RATING_MAP.get(rating_class, 0.0)

                likes_element = review.find('p', class_='react-component')
                likes = int(likes_element['data-count'].replace(',', '')) if (
                        likes_element and 'data-count' in likes_element.attrs) else 0

                comment_tag = review.find('div', class_='js-review-body')
                comment = comment_tag.get_text(strip=True, separator=' ') if comment_tag else "N/A"

                try:
                    language = detect(comment) if comment not in ["N/A", ""] else "unknown"
                except LangDetectException:
                    language = "unknown"

                if language == 'pt':
                    comments.append({
                        'movie_title': movie_title,
                        'username': username,
                        'numeric_rating': numeric_rating,
                        'likes': likes,
                        'language': language,
                        'comment': comment
                    })

            except Exception as e:
                print(f"Erro no comentário: {e}")
                continue

        with lock:
            allowed = shared_data['max_comments'] - shared_data['comment_count']
            comments = comments[:allowed]
            shared_data['comment_count'] += len(comments)
            shared_data['all_comments'].extend(comments)

def get_movie_url(movie_name: str):
    result = requests.get(f'https://api.letterboxd.com/api/v0/search', params={'input': movie_name}).json()
    film_url = result['items'][0]['film']['links'][0]['url']
    poster_url = result['items'][0]['film']['poster']['sizes'][1]['url']
    return film_url, poster_url

def get_movie_reviews(movie_name: str):
    movie_url, poster_url = get_movie_url(movie_name)
    movie_reviews_url = f'{movie_url}reviews/'

    url_gen = url_generator(movie_reviews_url)
    num_workers=10

    shared_data = {
        'max_pages': 75,
        'max_comments': 100,
        'page_count': 0,
        'comment_count': 0,
        'all_comments': []
    }

    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, url_gen, shared_data, lock) for _ in range(num_workers)]
        for f in futures:
            f.result()

    return poster_url, shared_data['all_comments']