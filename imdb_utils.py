from imdb import Cinemagoer
import logging

ia = Cinemagoer()


def safe_search_movie(title):
    FETCH_LIMIT = 5
    for i in range(FETCH_LIMIT):
        try:
            result = ia.search_movie(title)
            if result:
                return result
        except Exception as e:
            logging.warning(
                f'Fetch movie "{title}" failed ({1+i}/{FETCH_LIMIT}): {e}')


def safe_get_movie(id):
    FETCH_LIMIT = 5
    for i in range(FETCH_LIMIT):
        try:
            result = ia.get_movie(id)
            if result:
                return result
        except Exception as e:
            logging.warning(
                f'Fetch movie "{id}" failed ({1+i}/{FETCH_LIMIT}): {e}')


def get_movie_info_by_title(title):
    REVENUE_KEY = 'Cumulative Worldwide Gross'

    def extract_budget_from_text(original_text):
        text = original_text.replace('$', '').replace(
            ' (estimated)', '').replace(',', '')
        text=''.join(filter(lambda x:x.isdigit(),[c for c in text]))
        return int(text)

    def extract_revenue_from_text(original_text):
        text = original_text.split(' ')[0].replace('$', '').replace(",", "")
        text=''.join(filter(lambda x:x.isdigit(),[c for c in text]))
        return int(text)

    def get_info_by_id(id):
        movie_info = safe_get_movie(id)
        # 提取电影信息中的budget、runtime、genres和revenue
        runtime = movie_info.get('runtime', '信息无法获取')
        genres = movie_info.get('genres', '信息无法获取')
        box_office = movie_info.get('box office', '信息无法获取')
        if box_office:
            print(box_office)
            budget = extract_budget_from_text(
                box_office['Budget']) if 'Budget' in box_office else -1.0
            revenue = extract_revenue_from_text(
                box_office[REVENUE_KEY]) if REVENUE_KEY in box_office else -1.0
        else:
            budget = None
            revenue = None
        return (budget, runtime, genres, revenue)

    movie_candidates = safe_search_movie(title)
    for candidate in movie_candidates:
        candidate_title = candidate.get('title', '')
        if candidate_title == title:
            (budget, runtime, genres, revenue) = get_info_by_id(
                candidate.movieID)

            return {
                'budget': budget,
                'runtime': runtime,
                'genres': genres,
                'revenue': revenue
            }


if __name__ == "__main__":

    # 要查询的电影标题
    movie_title = "The Blue Butterfly"

    # 调用函数打印电影信息
    print(get_movie_info_by_title(movie_title))

    # https://cn.linux-console.net/?p=28972
