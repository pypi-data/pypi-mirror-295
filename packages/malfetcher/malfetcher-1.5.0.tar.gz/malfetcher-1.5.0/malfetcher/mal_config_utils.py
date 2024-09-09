import socket
import os, webbrowser, platform, requests, gevent, gc, string, random
from flask import Flask, request, redirect
from gevent.pywsgi import WSGIServer
from urllib.parse import parse_qs
from .utils import utils_save_json, utils_read_json

def generate_mal_verifier():
    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choice(characters) for _ in range(length))
        return random_string
    
    # Generate a random code verifier between 43 and 128 characters
    code_verifier_length = random.randint(43, 128)
    code_verifier = generate_random_string(code_verifier_length)
    return code_verifier

code_verifier = generate_mal_verifier()

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None

host_ip = get_ip_address()

# Paths
script_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_path, 'config', 'config.json')

is_ssh = 'SSH_CONNECTION' in os.environ
is_displayless = 'DISPLAY' not in os.environ
is_linux = platform.system() == "Linux"
headless_config = False
if is_linux:
    if is_ssh or is_displayless:
        headless_config = True

def generate_mal_verifier():
    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choice(characters) for _ in range(length))
        return random_string
    
    # Generate a random code verifier between 43 and 128 characters
    code_verifier_length = random.randint(43, 128)
    code_verifier = generate_random_string(code_verifier_length)
    return code_verifier

def generate_user_agents(num_agents):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.'
    ]
    return random.sample(user_agents, num_agents)

def regenerate_token():
    global code_verifier
    user_agents = generate_user_agents(8)
    chosen_user_agent = random.choice(user_agents)
    current_config = utils_read_json(config_path)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json",
        'Authorization': current_config['myanimelist_client_id'],
        'User-Agent': chosen_user_agent
    }
    json = {
        'client_id': current_config['myanimelist_client_id'],
        'client_secret': current_config['myanimelist_client_secret'],
        'grant_type': "refresh_token",
        'refresh_token': current_config['myanimelist_refresh_token'],
    }
    response = requests.post("https://myanimelist.net/v1/oauth2/token", data=json, headers=headers)
    if response.status_code == 200:
        response = response.json()
    else:
        print('Refreshing token failed, please try again...')
        exit(0)
    current_config['myanimelist_user_token'] = response['access_token']
    current_config['myanimelist_refresh_token'] = response['refresh_token']
    utils_save_json(config_path, current_config)

def setup_webserver():
    app = Flask(__name__)

    # Enable CORS for all routes
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Headers'] = "Content-Type"
        response.headers['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
        return response

    @app.route('/access_token') #Listen for token webhook
    def receive_token():
        def make_request(code):
            global code_verifier
            user_agents = generate_user_agents(5)
            chosen_user_agent = random.choice(user_agents)
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Accept': "application/json",
                'Authorization': global_id,
                'User-Agent': chosen_user_agent
            }
            json = {
                'client_id': global_id,
                'client_secret': global_secret,
                'grant_type': "authorization_code",
                'code': code,
                'redirect_uri': f"http://{host_ip}:8888/access_token",
                'code_verifier': code_verifier,
                'state': "authrequest"
            }
            response = requests.post("https://myanimelist.net/v1/oauth2/token", data=json, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print('Access token obtaining failed, please try again')
                exit(0)

        # Extracting query parameters from the request URL
        query = request.query_string.decode()
        params = parse_qs(query)

        # Extracting the 'code' parameter from the query
        code = params.get('code', [''])[0]

        # Do something with the code
        global access_token, refresh_token
        tokens = make_request(code)
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        
        http_server.stop()
        return redirect("https://myanimelist.net/")
        
    def start_webserver():
        if headless_config:
           print("Open this URL in your browser: ", global_tooltip)
        else:
            print("Authentificate in the opened tab")
            webbrowser.open(global_tooltip, 0)
        http_server.serve_forever()

    http_server = WSGIServer((host_ip, 8888), app, log=None)

    return start_webserver, http_server 
        
def config_setup(print_only = False):
    setup_function, _ = setup_webserver()  # Setup the server function here
    
    def gen_please(name, help):
        return f"Please input your {name} here ({help}):\n"
    
    def get_input(prompt, data_type = str):
        while True:
            user_input = input(prompt)
            try:
                converted_input = data_type(user_input)
                return converted_input
            except ValueError:
                print("Invalid input. Please enter a valid", data_type.__name__)     
    
    def generate_api_key(client_id, client_secret):
        global global_id
        global global_secret
        global global_tooltip
        global code_verifier
        global_id = client_id
        global_secret = client_secret
        global_tooltip = "https://myanimelist.net/v1/oauth2/authorize?"
        global_tooltip += "response_type=code"
        global_tooltip += f"&client_id={global_id}"
        global_tooltip += f"&redirect_uri=http://{host_ip}:8888/access_token"
        global_tooltip += f"&code_challenge={code_verifier}"
        global_tooltip += "&code_challenge_method=plain"
        global_tooltip += "&state=authrequest"
        
        setup_function()  # Start the server here
        user_token = access_token
        user_refresh_token = refresh_token
        gevent.killall(
            [obj for obj in gc.get_objects() if isinstance(obj, gevent.Greenlet)]
        ) #kill all gevent greenlets to prevert interference
        return [user_token, user_refresh_token]
    
    config_dict = {}
    print("Please create a new API client")
    if headless_config:
        if is_displayless:
            print("The setup process cannot be continued on this machine")
            print("Please SSH into this machine, set the access key as an env variable or import the config directly")
        client_id = get_input(gen_please("MyAnimeList API Client ID","https://myanimelist.net/apiconfig"))
        client_secret = get_input(gen_please("MyAnimeList API Client Secret",f"https://myanimelist.net/apiconfig/edit/{client_id}"))
    else:
        webbrowser.open("https://myanimelist.net/apiconfig", 0)
        client_id = get_input(gen_please("MyAnimeList API Client ID","Paste the Client ID"))    
        client_secret = get_input(gen_please("MyAnimeList API Client Secret","Paste the Client Secret"))
    tokens = generate_api_key(client_id, client_secret)
    config_dict['myanimelist_client_id'] = client_id
    config_dict['myanimelist_client_secret'] = client_secret   
    config_dict['myanimelist_user_token'] = tokens[0]
    config_dict['myanimelist_refresh_token'] = tokens[1]
    if not print_only:    
        utils_save_json(config_path, config_dict)
    return config_dict