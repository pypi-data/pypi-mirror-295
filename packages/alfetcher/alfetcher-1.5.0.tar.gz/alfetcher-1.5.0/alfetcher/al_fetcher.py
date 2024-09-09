import requests, time, os, copy, math
from datetime import datetime, timedelta
from .utils import utils_save_json, utils_read_json, print_deb
from .al_config_utils import config_setup

script_path = os.path.dirname(os.path.abspath(__file__))
al_id_cache_path = os.path.join(script_path, 'cache', 'anilist_id_cache.json')
al_search_cache_path = os.path.join(script_path, 'cache', 'anilist_search_cache.json')
config_path = os.path.join(script_path, 'config', 'config.json')


# Utils

def clear_cache():
    config = utils_read_json(config_path)
    try:
        del config['checked_date']
    except:
        pass
    os.remove(al_id_cache_path)
    os.remove(al_search_cache_path)

def check_status_in_cache():
    og_cache = utils_read_json(al_id_cache_path)
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
            if not release_date:
                continue
            status = cache[anime]['status']
            if status == "RELEASING":
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
            elif status == "NOT_YET_RELEASED":
                if release_date:
                    if current_date > release_date:
                        cache.update(get_anime_info(anime, True))
        config_dict['checked_date'] = current_date.strftime('%Y-%m-%d')
        utils_save_json(config_path, config_dict)
        utils_save_json(al_id_cache_path, cache, True)

def load_cache():
    check_status_in_cache()
    return utils_read_json(al_id_cache_path)

def load_config():
    config = utils_read_json(config_path)
    try:
        return config['anilist_user_token']
    except:
        return config_setup()['anilist_user_token']

# Functions

def make_graphql_request(query, variables=None, al_token=None, user_request = False):
    # Constants for GraphQL endpoint and headers
    ANILIST_API_URL = "https://graphql.anilist.co"
    HEADERS = {}
    HEADERS['Content-Type'] = "application/json"
    
    if user_request:
        if al_token:
            pass
        elif 'anilist_key' in os.environ:
            al_token = os.getenv('anilist_key')
            if not os.path.exists(os.path.dirname(config_path)):
                os.makedirs(os.path.dirname(config_path))
        else:
            al_token = load_config()
        HEADERS['Authorization'] = f"Bearer {al_token}"

    def make_request():
        response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
        return response

    retries = 0
    while True:
        response = make_request()
        if response.status_code == 200:
            return response.json().get('data', {})
        elif response.status_code == 429:
            print_deb(f"Rate limit exceeded. Waiting before retrying...")
            print_deb(query, variables, HEADERS, sep="\n")
            print_deb(response.json())
            retry_after = int(response.headers.get('retry-after', 1))
            time.sleep(retry_after)
            retries += 1
        elif response.status_code == 500 or response.status_code == 400:
            print_deb(f"Unknown error occurred, retrying...")
            print_deb(query, variables, HEADERS, sep="\n")
            print_deb(response.json())
            retries += 1
        elif response.status_code == 404:
            print(f"Anime not found")
            return None
        else:
            print_deb(f"Error {response.status_code}: {variables}")
            return {}

        # Exponential backoff with a maximum of 5 retries
        if retries >= 5:
            print_deb("Maximum retries reached. Exiting.")
            return {}
                
        print(f"Retrying... (Attempt {retries})")

def get_latest_anime_entry_for_user(status = "ALL", al_token=None,  username=None):
    if al_token:
        if not username:
            username = get_userdata(al_token)[0]
        user_request = True
    else:
        user_request = False
        
    status = status.upper()
    status_options = ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED", "REPEATING"]
    if status != "ALL":
        if not status in status_options:
            print("Invalid status option. Allowed options are:", ", ".join(str(option) for option in status_options) )
            return
        query = '''
        query ($username: String) {
            MediaListCollection(userName: $username, type: ANIME, status: %s, sort: [UPDATED_TIME_DESC]) {
        ''' %status
    else:
        query = '''
        query ($username: String) {
            MediaListCollection(userName: $username, type: ANIME, sort: [UPDATED_TIME_DESC]) {
        '''        
    query += '''
            lists {
                entries {
                    id
                    progress
                    status
                    media {
                        id
                        idMal
                        episodes
                        tags {
                            name
                        }
                        genres
                        isAdult
                        title {
                            romaji
                            english
                            native
                        }
                        synonyms
                        status
                        startDate {
                            year
                            month
                            day
                        }
                        endDate {
                            year
                            month
                            day
                        }
                        nextAiringEpisode {
                            episode
                        }
                        format
                        relations {
                            edges {
                                relationType(version: 2)
                                node {
                                    id
                                    title {
                                        romaji
                                    }
                                    status
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    '''
    variables = {'username': username}

    data = make_graphql_request(query, variables, al_token, user_request=user_request)

    if data:
        entries = data.get('MediaListCollection', {}).get('lists', [])[0].get('entries', [])
        if entries:
            for anime in entries:
                anime_id = str(anime['media']['id'])
                anime_info = generate_anime_entry(anime['media'])
                user_entry = {}    # Initialize as a dictionary if not already initialized
                user_entry[anime_id] = {}    # Initialize as a dictionary if not already initialized
                user_entry[anime_id].update(anime_info)
                user_entry[anime_id]['watched_ep'] = anime['progress']
                user_entry[anime_id]['watching_status'] = anime['status']
                return user_entry

    print(f"No entries found for {username}'s {status.lower()} anime list.")
    return None

def get_all_anime_for_user(status_list="ALL", al_token=None, username=None):
    if al_token:
        if not username:
            username = get_userdata(al_token)[0]
        user_request = True
    else:
        user_request = False
        
    def main_function(status):
        status = status.upper()
        status_options = ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED", "REPEATING"]
        if status != "ALL":
            if not status in status_options:
                print("Invalid status option. Allowed options are:", ", ".join(str(option) for option in status_options))
                return
            query = '''
            query ($username: String) {
                MediaListCollection(userName: $username, type: ANIME, status: %s, sort: [UPDATED_TIME_DESC]) {
            ''' %status
        else:
            query = '''
            query ($username: String) {
                MediaListCollection(userName: $username, type: ANIME, sort: [UPDATED_TIME_DESC]) {
            '''        
        query += '''
                lists {
                    entries {
                        id
                        progress
                        status
                        media {
                            id
                            idMal
                            episodes
                            tags {
                                name
                            }
                            genres
                            isAdult
                            title {
                                romaji
                                english
                                native
                            }
                            synonyms
                            status
                            startDate {
                                year
                                month
                                day
                            }
                            endDate {
                                year
                                month
                                day
                            }
                            nextAiringEpisode {
                                episode
                            }
                            format
                            relations {
                                edges {
                                    relationType(version: 2)
                                    node {
                                        id
                                        title {
                                            romaji
                                        }
                                        status
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        '''
        variables = {'username': username}

        data = make_graphql_request(query, variables, al_token, user_request=user_request)

        user_ids = {}
            
        if data:
                entries = data.get('MediaListCollection', {}).get('lists', [])
                full_entries = {}
                for entry in entries: 
                    for list_entry in entry['entries']:
                        full_entries[str(list_entry['id'])] = {}
                        full_entries[str(list_entry['id'])].update(list_entry) 
                if full_entries:
                        for anime_entry in full_entries:
                            anime = full_entries[anime_entry]
                            anime_entry_data = anime['media']
                            anime_id = anime_entry_data['id']
                            anime_id = str(anime_id)
                            anime_info = generate_anime_entry(anime_entry_data)
                            if not anime_id in user_ids:
                                user_ids[anime_id] = {}    # Initialize as a dictionary if not already initialized
                            user_ids[anime_id].update(anime_info)
                            user_ids[anime_id]['watched_ep'] = anime['progress']
                            user_ids[anime_id]['watching_status'] = anime['status']
                        return user_ids
        print(f"No entries found for {username}'s {status.lower()} anime list.")
        return None    

    if isinstance(status_list, str):
        status_list = status_list.upper()
        main_function(status_list)
        return main_function(status_list)
    elif len(status_list) == 1:
        status_list = status_list[0].upper()
        return main_function(status_list)
    elif isinstance(status_list, list):
        ani_list = {}
        for status in status_list:
            status.upper()
            ani_list.update(main_function(status))
        return ani_list

def get_anime_entry_for_user(al_id, al_token=None, username=None):
    if al_token:
        if not username:
            username = get_userdata(al_token)[0]
        user_request = True
    else:
        user_request = False
        
    al_id = str(al_id)
    query = '''
    query ($mediaId: Int, $username: String) {
        MediaList(mediaId: $mediaId, userName: $username, type: ANIME) {
            mediaId
            progress
            status
        }   
    }
    '''
    variables = {'mediaId': al_id, 'username': username}
    data = make_graphql_request(query, variables, al_token, user_request=user_request)
    if data:
        anime = data.get('MediaList', {})
        anime_id = str(anime['mediaId'])
        anime_info = get_anime_info(anime_id, False, al_token)
        user_entry = {}    # Initialize as a dictionary if not already initialized
        user_entry.update(anime_info)
        user_entry[anime_id]['watched_ep'] = anime['progress']
        user_entry[anime_id]['watching_status'] = anime['status']
        return user_entry
    return None

def get_anime_info(anime_id, force_update = False, al_token=None):
    if force_update:
        anime_cache = {}
    else:
        anime_cache = load_cache()
    anime_id = str(anime_id)
    if not anime_id:
        return None
    def fetch_from_al():
        # Fetch anime info from Anilist API or any other source
        anime_info = al_fetch_anime_info(anime_id, al_token)
        # Cache the fetched anime info
        utils_save_json(al_id_cache_path, anime_info, False)
        return anime_info
    # Check if anime_id exists in cache
    try:
        if anime_id in anime_cache and not force_update:
                print_deb("Returning cached result for anime_id:", anime_id)
                return {anime_id: anime_cache[anime_id]}
        else:
            return fetch_from_al()
    except TypeError:
        return fetch_from_al()

def al_fetch_anime_info(al_id, al_token=None):
    query = '''
    query ($mediaId: Int) {
        Media(id: $mediaId) {
            id
            idMal
            episodes
            tags {
                name
            }
            genres
            isAdult
            title {
                romaji
                english
                native
            }
            synonyms
            status
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            nextAiringEpisode {
                episode
            }
            format
            relations {
                edges {
                    relationType(version: 2)
                    node {
                        id
                        title {
                            romaji
                        }    
                        status
                    }
                }
            }
        }
    }
    '''
    
    variables = {'mediaId': al_id}

    data = make_graphql_request(query, variables, al_token)
    anime_data = {}
    if data:
        anime = data.get('Media', {})
        if anime:
            anime_id = str(anime['id'])
            anime_info = anime
            anime_data[anime_id] = {}
            anime_data[anime_id].update(generate_anime_entry(anime_info))
        return anime_data
    return {}

def generate_anime_entry(anime_info):
    def get_release_date(anime_data):
        start_date = anime_data.get('startDate', {})
        year = start_date.get('year')
        month = start_date.get('month')
        if not year or not month:
            return None
        day = start_date.get('day') if start_date['day'] else 1
        release_date = datetime(year, month, day).strftime('%Y-%m-%d')
        return release_date
        
    def get_end_date(anime_data):
        end_date = anime_data.get('endDate', {})
        year = end_date.get('year')
        month = end_date.get('month')
        if not year or not month:
            return None
        day = end_date.get('day') if end_date['day'] else 1
        end_date = datetime(year, month, day).strftime('%Y-%m-%d')
        return end_date         

    def getRelated():
        relations = {}
        edges = anime_info['relations']['edges']
        for edge in edges:
            if edge['relationType'] == "PREQUEL" or edge['relationType'] == "SEQUEL":
                relation_id = str(edge['node']['id'])
                relations[relation_id] = {}
                relations[relation_id]['main_title'] = edge['node']['title']['romaji']
                relations[relation_id]['status'] = edge['node']['status']
                relations[relation_id]['type'] = edge['relationType']
        if not relations:
            relations = None
        return relations

    def is_sus(anime_data):
        genres = anime_data['genres']
        tags = [item['name'] for item in anime_data['tags']]
        adult_status = anime_data['isAdult']
        sus_tags = ["Nudity", "Bondage", "Masochism", "Sadism", "Exhibitionism"]
        for sus_tag in sus_tags:
            if sus_tag in tags:
                return True
        if "Ecchi" in genres or adult_status:
            return True
        else:
            return False

    def generate_upcoming_ep(release_date):
        current_date = datetime.now().date()
        release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
        upcoming_ep = math.ceil(int((current_date - release_date).days)/7) + 1
        return upcoming_ep

    anime_id = str(anime_info['id'])
    anime_data = {}
    anime_data['mal_id'] = anime_info['idMal']
    anime_data['total_eps'] = anime_info['episodes']
    anime_data['is_sus'] = is_sus(anime_info)
    anime_data['main_title'] = anime_info['title']['romaji']
    anime_data['synonyms'] = [
        anime_info['title']['romaji'],
        anime_info['title']['english'],
        anime_info['title']['native'],
    ] + anime_info['synonyms']
    anime_data['synonyms'] = [item for item in anime_data['synonyms'] if item is not None]    
    anime_data['status'] = anime_info['status']
    anime_data['release_date'] = get_release_date(anime_info)
    anime_data['end_date'] = get_end_date(anime_info)
    anime_data['upcoming_ep'] = ((generate_upcoming_ep(anime_data['release_date']) if anime_data['status'] == "RELEASING" else None) 
                                if not anime_info['nextAiringEpisode'] else anime_info['nextAiringEpisode']['episode']) #who needs readability
    anime_data['format'] = anime_info['format']
    anime_data['related'] = getRelated()
    utils_save_json(al_id_cache_path, {anime_id: anime_data}, False)
    return anime_data

def get_id(name, al_token=None):
    search_cache = utils_read_json(al_search_cache_path)
    
    def fetch_from_al():
        # Fetch anime info from Anilist API or any other source
        anime_name = al_fetch_id(name)
        anime_info = str(anime_name) if anime_name else None
        if anime_info:
            ani_dict = get_anime_info(anime_info, False, al_token)
            status = ani_dict[anime_info]['status']
            if status == "NOT_YET_RELEASED":
                anime_info = None
            json_out = {name: anime_info}
            if anime_info:
                utils_save_json(al_search_cache_path, json_out, False)
            return anime_info
        return None
    # Check if anime_id exists in cache
    try:
        if search_cache and name in search_cache:
            print_deb("Returning cached result for search query:", name)
            return str(search_cache[name])
        else:
            return fetch_from_al()
    except TypeError:
        return fetch_from_al()
            
def al_fetch_id(name, al_token=None):
    query = '''
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            id
        }
    }
    '''
    variables = {'search': name}
    data = make_graphql_request(query, variables, al_token)

    if data:
        anime_list = data['Media']['id']

        if anime_list:
            return anime_list

    return None

def get_userdata(al_token=None):
    # GraphQL query to get the username of the authenticated user
    query = """
    query {
        Viewer {
            name
            avatar {
                large
            }
        }
    }
    """
    
    variables = {}
    data = make_graphql_request(query, variables, al_token, user_request = True)

    if data:
        # Extract the username from the response data
        username = data['Viewer']['name']
        profile_pic = data['Viewer']['avatar']['large']
        return [username, profile_pic]

def al_to_mal_id(al_id):
    query = """
    query ($mediaId: Int) {
        Media(id: $mediaId, type: ANIME) {
            idMal
        }
    }
    """
    variables = {'mediaId': al_id}
    data = make_graphql_request(query, variables)

    if data:
        return int(data['Media']['idMal'])
    return None

def update_entry(anime_id, progress, al_token=None):
    anime_id = str(anime_id)
    progress = int(progress)
    total_eps = get_anime_info(anime_id, al_token=al_token)[anime_id]['total_eps']
    try:
        user_eps = get_anime_entry_for_user(anime_id, al_token=al_token)[anime_id]['watched_ep']
    except:
        user_eps = 0

    if progress <= user_eps:
        print_deb('Not updating, progress is lower or equal than user progress')
        return

    query = """
        mutation ($mediaId: Int, $progress: Int, $status: MediaListStatus) {
            SaveMediaListEntry(mediaId: $mediaId, progress: $progress, status: $status) {
                id
            }
        }
    """
    variables = {}
    variables['mediaId'] = anime_id
    variables['progress'] = progress
    if progress == total_eps:
        variables['status'] = 'COMPLETED'
    elif progress == 0:
        variables['status'] = 'PLANNING'
        query = """
            mutation ($mediaId: Int, $status: MediaListStatus) {
                SaveMediaListEntry(mediaId: $mediaId, status: $status) {
                    id
                }
            }
        """
        del variables['progress']
    else:
        variables['status'] = 'CURRENT'
    make_graphql_request(query, variables, al_token, user_request = True)
    print_deb('Updating progress successful')