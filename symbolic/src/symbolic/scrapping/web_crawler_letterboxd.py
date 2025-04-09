import requests
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
from langdetect import detect, LangDetectException

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

def get_all_reviews(base_url, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': 'https://letterboxd.com/'
    }

    page = 1
    total_reviews = 0
    movie_title = "N/A"

    while True:
        url = urljoin(base_url, f"page/{page}/") if page > 1 else base_url
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro na página {page}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrai nome do filme apenas na primeira página
        title_tag = soup.find('h1', class_='headline-2 prettify')
        if title_tag:
            movie_title = title_tag.find('a').text.strip()
        else:
            movie_title = "N/A"

        review_elements = soup.find_all('li', class_='film-detail')

        if not review_elements:
            break

        batch_reviews = []
        
        for review in review_elements:
            try:
                # Dados básicos
                username_tag = review.find('a', class_='avatar')
                username = username_tag['href'].split('/')[-2] if username_tag else "N/A"

                # Rating
                rating_tag = review.find('span', class_='rating')
                rating_class = [c for c in rating_tag['class'] if c.startswith('rated-')][0] if rating_tag else None
                numeric_rating = RATING_MAP.get(rating_class, 0.0)

                # Likes
                likes_element = review.find('p', class_='react-component')
                likes = int(likes_element['data-count'].replace(',', '')) if (likes_element and 'data-count' in likes_element.attrs) else 0

                # Comentário e idioma
                comment_tag = review.find('div', class_='js-review-body')
                comment = comment_tag.get_text(strip=True, separator=' ') if comment_tag else "N/A"
                
                # Detecção de idioma
                try:
                    language = detect(comment) if comment not in ["N/A", ""] else "unknown"
                except LangDetectException:
                    language = "unknown"

                batch_reviews.append({
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

        # Atualiza o CSV
        save_to_csv(batch_reviews, output_file, is_first_page=(page == 1))
        total_reviews += len(batch_reviews)
        
        print(f"Página {page} processada: {len(batch_reviews)} comentários (Total: {total_reviews})")
        page += 1
        sleep(0.25)

def save_to_csv(reviews, filename, is_first_page):
    mode = 'w' if is_first_page else 'a'
    header = is_first_page
    
    with open(filename, mode, newline='', encoding='utf-8') as csvfile:
        fieldnames = ['movie_title', 'username', 'numeric_rating', 'likes', 'language', 'comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if header:
            writer.writeheader()
        
        writer.writerows(reviews)

if __name__ == "__main__":
    movie_url = input("Cole a URL completa da seção de reviews (ex: .../film/.../reviews/): ").strip()
    output_file = "movie_reviews_with_language.csv"

    if os.path.exists(output_file):
        os.remove(output_file)

    get_all_reviews(movie_url, output_file)
    
    print(f"\n✅ Coleta finalizada! Arquivo salvo: {output_file}")


# Website example: https://letterboxd.com/film/julie-keeps-quiet/reviews/