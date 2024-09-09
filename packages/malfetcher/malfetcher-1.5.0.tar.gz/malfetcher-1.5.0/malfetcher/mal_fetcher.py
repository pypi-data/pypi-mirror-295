import requests, time, os, copy, math
from datetime import datetime, timedelta
from .utils import utils_save_json, utils_read_json, print_deb
from .mal_config_utils import config_setup, regenerate_token

script_path = os.path.dirname(os.path.abspath(__file__))
mal_id_cache_path = os.path.join(script_path, 'cache', 'myanimelist_id_cache.json')
mal_search_cache_path = os.path.join(script_path, 'cache', 'myanimelist_search_cache.json')
config_path = os.path.join(script_path, 'config', 'config.json')
anime_request_url = "https://api.myanimelist.net/v2/anime"

al_to_mal_user_status = {
    'CURRENT': "watching",
    'COMPLETED': "completed",
    'PAUSED': "on_hold",
    'DROPPED': "dropped",
    'PLANNING': "plan_to_watch"
}

mal_to_al_user_status = {v:k for k, v in al_to_mal_user_status.items()}

al_to_mal_status = {
    'FINISHED': "finished_airing",
    'RELEASING': "currently_airing",
    'NOT_YET_RELEASED': "not_yet_aired"
}

mal_to_al_status = {v:k for k, v in al_to_mal_status.items()}
skip_user_statuses = ["REPEATING"]

# Minimal user setup to interact with MyAnimeList API
config = utils_read_json(config_path)
if not config or 'myanimelist_client_id' not in config:
    client_id = input("Please input your MyAnimeList API Client ID.\nhttps://myanimelist.net/apiconfig\n")
    if not config:
        config = {}
    config['myanimelist_client_id'] = client_id
    utils_save_json(config_path, config)
else:
    client_id = config['myanimelist_client_id']

# Utils

def clear_cache():
    config = utils_read_json(config_path)
    try:
        del config["checked_date"]
    except:
        pass
    os.remove(mal_id_cache_path)
    os.remove(mal_search_cache_path)

def check_status_in_cache():
    og_cache = utils_read_json(mal_id_cache_path)
    if not og_cache: return
    cache = copy.deepcopy(og_cache)
    config_dict = utils_read_json(config_path) if utils_read_json(config_path) else {}
    current_date = datetime.now().date()
    try:
        checked_date = datetime.strptime(config_dict['checked_date'], '%Y-%m-%d').date()
    except:
        config_dict['checked_date'] = current_date.strftime('%Y-%m-%d')
        utils_save_json(config_path, config_dict)
        checked_date = current_date
    if current_date > checked_date:
        for anime in og_cache:
            try:
                release_date = datetime.strptime(cache[anime]['release_date'], '%Y-%m-%d').date()
            except:
                release_date = None
            try:
                end_date = datetime.strptime(cache[anime]['end_date'], '%Y-%m-%d').date()
            except:
                end_date = None
            status = cache[anime]['status']
            if status == "NOT_YET_RELEASED":
                cache.update(get_anime_info(anime, True)) #force update everytime
            elif status == "RELEASING" and release_date:
                    try:
                        next_ep_date = release_date + timedelta(cache[anime]['upcoming_ep'] * 7)
                        if end_date and current_date > end_date:
                            updated_info = get_anime_info(anime, True)
                            cache.update(updated_info)
                        if current_date > next_ep_date:
                            updated_info = get_anime_info(anime, True)
                            cache.update(updated_info)
                    except: #force update if we don't have the next episode
                        updated_info = get_anime_info(anime, True)
                        cache.update(updated_info)
        config_dict['checked_date'] = current_date.strftime('%Y-%m-%d')
        utils_save_json(config_path, config_dict)
        utils_save_json(mal_id_cache_path, cache, True)

def load_cache():
    check_status_in_cache()
    return utils_read_json(mal_id_cache_path)

def load_config():
    config = utils_read_json(config_path)
    try:
        return config['myanimelist_user_token']
    except:
        return config_setup()['myanimelist_user_token']

# Functions

def make_graphql_request(mal_api_url, params, method='get', mal_token=None, user_request = False):
    local_token = False
    if user_request:
        if mal_token:
            pass
        elif 'myanimelist_key' in os.environ:
            mal_token = os.getenv('myanimelist_key')
            if not os.path.exists(config_path):
                os.makedirs(os.path.dirname(config_path))
        else:
            mal_token = load_config()
            local_token = True
        HEADERS = {'Authorization': f"Bearer {mal_token}"}
    else:
        HEADERS = {'X-MAL-CLIENT-ID': f"{client_id}"}

    def make_request():
        request_func = getattr(requests, method.lower(), None)
        if method.lower() == 'put':
           response = request_func(mal_api_url, data=params, headers=HEADERS)
        else: 
            response = request_func(mal_api_url, params=params, headers=HEADERS)    
        return response

    retries = 0
    while True:
        response = make_request()
        if response.status_code == 200:
            json_response = response.json()
            if 'data' in json_response:
                return json_response['data']
            return json_response
        elif response.status_code == 429:
            print_deb(f"Rate limit exceeded. Waiting before retrying...")
            print_deb(params, HEADERS, sep="\n")
            print_deb(response.json())
            retry_after = int(response.headers.get('retry-after', 1))
            time.sleep(retry_after)
            retries += 1
        elif response.status_code == 500 or response.status_code == 400:
            print_deb(f"Unknown error occurred, retrying...")
            print_deb(params, HEADERS, sep="\n")
            print_deb(response.json())
            retries += 1
        elif response.status_code == 404:
            print(f"Anime not found")
            return None
        elif response.status_code == 401 and local_token:
            print_deb(f"Access token expired, refreshing")
            regenerate_token()
            retries += 1
        else:
            print_deb(f"Error {response.status_code}: {params}")
            return {}

        # Exponential backoff with a maximum of 5 retries
        if retries >= 5:
            print_deb("Maximum retries reached. Exiting.")
            return {}
                
        print(f"Retrying... (Attempt {retries})")

def get_latest_anime_entry_for_user(status = "ALL", mal_token=None,  username = None):
    if not username:
        username = get_userdata(mal_token)[0]
        user_request = True
    else:
        user_request = False

    status = status.upper()
    status_options = ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED", "REPEATING"]
    params = {}
    params['sort'] = 'anime_start_date'
    params['fields'] = (
        "id,"
        "title,"
        "alternative_titles,"
        "start_date,"
        "end_date,"
        "nsfw,"
        "media_type,"
        "status,"
        "genres,"
        "my_list_status,"
        "num_episodes,"
        "related_anime"
    )
    params['limit'] = 1
    if status != "ALL":
        if not status in status_options:
            print("Invalid status option. Allowed options are:", ", ".join(str(option) for option in status_options) )
            return
        if status in skip_user_statuses:
            return
        params['status'] = al_to_mal_user_status[status]

    request_url = f"https://api.myanimelist.net/v2/users/{username}/animelist"
    data = make_graphql_request(request_url, params, mal_token = mal_token, user_request = user_request)

    if data:
        anime = data[0]['node']
        anime_id = str(anime['id'])
        anime_info = generate_anime_entry(anime, mal_token)
        user_entry = {}    # Initialize as a dictionary if not already initialized
        user_entry[anime_id] = {}    # Initialize as a dictionary if not already initialized
        user_entry[anime_id].update(anime_info)
        try:
            user_entry[anime_id]['watched_ep'] = anime['my_list_status']['num_episodes_watched']
            user_entry[anime_id]['watching_status'] = mal_to_al_user_status[anime['my_list_status']['status']]
        except:
            pass
        return user_entry

    print(f"No entries found for {username}'s {status.lower()} anime list.")
    return None

def get_all_anime_for_user(status_list="ALL", mal_token=None, username = None):
    if not username:
        username = get_userdata(mal_token)[0]
        user_request = True
    else:
        user_request = False
        
    def main_function(status):
        status = status.upper()
        status_options = ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED", "REPEATING"]
        params = {}
        params['sort'] = "anime_start_date"
        params['fields'] = (
            "id,"
            "title,"
            "alternative_titles,"
            "start_date,"
            "end_date,"
            "nsfw,"
            "media_type,"
            "status,"
            "genres,"
            "my_list_status,"
            "num_episodes,"
            "related_anime"
        )
        if status != "ALL":
            if not status in status_options:
                print("Invalid status option. Allowed options are:", ", ".join(str(option) for option in status_options))
                return
            params['status'] = al_to_mal_user_status[status]

        request_url = f"https://api.myanimelist.net/v2/users/{username}/animelist"
        data = make_graphql_request(request_url, params, mal_token = mal_token, user_request = user_request)

        user_ids = {}
            
        if data:
            for anime_entry in data:
                anime_entry_data = anime_entry['node']
                anime_id = anime_entry_data['id']
                anime_id = str(anime_id)
                anime_info = generate_anime_entry(anime_entry_data, mal_token)
                if not anime_id in user_ids:
                    user_ids[anime_id] = {}    # Initialize as a dictionary if not already initialized
                user_ids[anime_id].update(anime_info)
                try:
                    user_ids[anime_id]['watched_ep'] = anime_entry_data['my_list_status']['num_episodes_watched']
                    user_ids[anime_id]['watching_status'] = mal_to_al_user_status[anime_entry_data['my_list_status']['status']]
                except:
                    pass
            return user_ids
        print(f"No entries found for {username}'s {status.lower()} anime list.")
        return None    

    if isinstance(status_list, str):
        status_list = status_list.upper()
        main_function(status_list)
        return main_function(status_list)
    elif len(status_list) == 1:
        status = status_list[0].upper()
        if status in skip_user_statuses:
            return
        main_function(status)
        return main_function(status_list)
    elif isinstance(status_list, list):
        ani_list = {}
        for status in status_list:
            if status in skip_user_statuses:
                continue
            status.upper()
            ani_list.update(main_function(status))
        return ani_list

def get_anime_entry_for_user(mal_id, mal_token=None):
    mal_id = str(mal_id)

    params = {}
    params['fields'] = (
        "id,"
        "title,"
        "alternative_titles,"
        "start_date,"
        "end_date,"
        "nsfw,"
        "media_type,"
        "status,"
        "genres,"
        "my_list_status,"
        "num_episodes,"
        "related_anime"
    )
    request_url = f"{anime_request_url}/{mal_id}"
    data = make_graphql_request(request_url, params, mal_token = mal_token, user_request=True)
    anime_data = {}
    if data:
        anime_id = str(data['id'])
        if 'my_list_status' not in data:
            return None
        anime_data[anime_id] = generate_anime_entry(data, mal_token)
        anime_data[anime_id]['watched_ep'] = data['my_list_status']['num_episodes_watched']
        anime_data[anime_id]['watching_status'] = mal_to_al_user_status[data['my_list_status']['status']]
        return anime_data
    return None

def get_anime_info(anime_id, force_update = False, mal_token=None):
    if force_update:
        anime_cache = {}
    else:
        anime_cache = load_cache()
    anime_id = str(anime_id)
    if not anime_id:
        return None
    def fetch_from_mal():
        # Fetch anime info from myanimelist API or any other source
        anime_info = mal_fetch_anime_info(anime_id, mal_token)
        # Cache the fetched anime info
        utils_save_json(mal_id_cache_path, anime_info, False)
        return anime_info
    # Check if anime_id exists in cache
    try:
        if anime_id in anime_cache and not force_update:
                print_deb("Returning cached result for anime_id:", anime_id)
                return {anime_id: anime_cache[anime_id]}
        else:
            return fetch_from_mal()
    except TypeError:
        return fetch_from_mal()

def mal_fetch_anime_info(mal_id, mal_token=None):
    params = {
        'fields': (
            "id,"
            "title,"
            "alternative_titles,"
            "start_date,"
            "end_date,"
            "nsfw,"
            "media_type,"
            "status,"
            "genres,"
            "my_list_status,"
            "num_episodes,"
            "related_anime"
        )
    }
    
    request_url = f'{anime_request_url}/{mal_id}'
    data = make_graphql_request(request_url, params, mal_token = mal_token)
    anime_data = {}
    if data:
        anime_id = str(data['id'])
        anime_data[anime_id] = {}
        anime_data[anime_id].update(generate_anime_entry(data, mal_token))
    return anime_data

def generate_anime_entry(anime_info, mal_token):
    def getRelated():
        def get_additional_info(relation_id):
            params = {
                'fields': "status, related_anime"
            }
            data = make_graphql_request(anime_request_url + f"/{relation_id}", params, mal_token = mal_token)
            return data            
        
        relations = {}
        try:
            edges = anime_info['related_anime']
        except:
            edges = get_additional_info(anime_info['id'])['related_anime']
        for edge in edges:
            relation_type = edge['relation_type'].upper()
            if relation_type == "PREQUEL" or relation_type == "SEQUEL":
                relation_id = str(edge['node']['id'])
                relations[relation_id] = {}
                relations[relation_id]['main_title'] = edge['node']['title']
                relations[relation_id]['status'] = mal_to_al_status[get_additional_info(relation_id)['status']]
                relations[relation_id]['type'] = relation_type
        if not relations:
            relations = None
        return relations

    def is_sus(anime_data):
        genres = [item['name'] for item in anime_data['genres']]
        adult_status = False if anime_data['nsfw']== 'white' else True
        sus_genres = ['Hentai', 'Ecchi', 'Erotica']
        for sus_genre in sus_genres:
            if sus_genre in genres:
                return True
        return adult_status

    def generate_upcoming_ep(release_date):
            current_date = datetime.now().date()
            release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
            upcoming_ep = math.ceil(int((current_date - release_date).days)/7) + 1
            return upcoming_ep

    def ensure_day_in_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            try:
                year_month = datetime.strptime(date_str, '%Y-%m')
                full_date = year_month.replace(day=1)
                return full_date.strftime('%Y-%m-%d')
            except ValueError:
                return None

    anime_id = str(anime_info['id'])
    anime_data = {}
    anime_data['al_id'] = mal_to_al_id(anime_id)
    anime_data['total_eps'] = anime_info['num_episodes']
    anime_data['is_sus'] = is_sus(anime_info)
    anime_data['main_title'] = anime_info['title']
    anime_data['synonyms'] = [
            anime_info['alternative_titles']['ja'],
            anime_info['alternative_titles']['en'],
    ] + anime_info['alternative_titles']['synonyms']
    anime_data['synonyms'] = [item for item in anime_data['synonyms'] if item is not None]    
    anime_data['status'] = mal_to_al_status[anime_info['status']]
    anime_data['release_date'] = ensure_day_in_date(anime_info['start_date']) if 'start_date' in anime_info else None
    anime_data['end_date'] = ensure_day_in_date(anime_info['end_date']) if 'end_date' in anime_info else None
    anime_data['upcoming_ep'] = generate_upcoming_ep(anime_data['release_date']) if anime_data['status'] == "RELEASING" else None
    anime_data['format'] = anime_info['media_type'].upper()
    anime_data['related'] = getRelated()
    utils_save_json(mal_id_cache_path, {anime_id: anime_data}, False)
    return anime_data

def get_id(name, mal_token=None):
    search_cache = utils_read_json(mal_search_cache_path)
    
    def fetch_from_mal():
        # Fetch anime info from myanimelist API or any other source
        anime_name = mal_fetch_id(name)
        anime_info = str(anime_name) if anime_name else None
        if anime_info:
            ani_dict = get_anime_info(anime_info, False, mal_token)
            status = ani_dict[anime_info]['status']
            if status == "NOT_YET_RELEASED":
                anime_info = None
            json_out = {name: anime_info}
            if anime_info:
                utils_save_json(mal_search_cache_path, json_out, False)
            return anime_info
        return None
    # Check if anime_id exists in cache
    try:
        if search_cache and name in search_cache:
                print_deb("Returning cached result for search query:", name)
                return str(search_cache[name])
        else:
                return fetch_from_mal()
    except TypeError:
        return fetch_from_mal()
            
def mal_fetch_id(name, mal_token=None):
    params = {
        'q': name,
        'limit': 1
    }
    data = make_graphql_request(anime_request_url, params, mal_token = mal_token)

    if data:
        return str(data[0]['node']['id'])

    return None

def get_userdata(mal_token):
    params = {}
    request_url = "https://api.myanimelist.net/v2/users/@me"
    data = make_graphql_request(request_url, params, mal_token = mal_token, user_request = True)

    if data:
        # Extract the username from the response data
        username = data['name']
        profile_pic = data['picture']
        return [username, profile_pic]

def mal_to_al_id(mal_id):
    # GraphQL query to get the username of the authenticated user
    query = """
    query ($malId: Int) {
        Media(idMal: $malId type: ANIME) {
            id
        }
    }
    """
    # Constants for GraphQL endpoint and headers
    ANILIST_API_URL = "https://graphql.anilist.co"
    HEADERS = {'Content-Type': "application/json"}
    variables = {'malId': mal_id}
    response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS).json()

    if response:
        return int(response['data']['Media']['id'])
    return None

def update_entry(anime_id, progress, mal_token=None):
    anime_id = str(anime_id)
    progress = int(progress)
    total_eps = get_anime_info(anime_id, mal_token=mal_token)[anime_id]['total_eps']
    try:
        user_eps = get_anime_entry_for_user(anime_id, mal_token=mal_token)[anime_id]['watched_ep']
    except:
        user_eps = 0

    if progress <= user_eps:
        print_deb('Not updating, progress is lower or equal than user progress')
        return

    params = {}
    params['num_watched_episodes'] = progress
    if progress == total_eps:
        params['status'] = 'COMPLETED'
    elif progress == 0:
        params['status'] = 'PLANNING'
        del params['num_watched_episodes']
    else:
        params['status'] = 'CURRENT'
    request_url = f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status"
    make_graphql_request(request_url, params, 'put', mal_token, True)
    print_deb('Updating progress successful')