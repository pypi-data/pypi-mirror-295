import json
import logging
import requests

from . import settings

def get_posts(username):

    try:
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        if hasattr(settings, 'INSTAGRAM_UA') and settings.INSTAGRAM_UA:
            ua = settings.INSTAGRAM_UA

        # URL of the Instagram Endpoint
        url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=farandride'

        headers = {
            'accept': '*/*',
            'accept-language': 'en',
            'cookie': 'csrftoken=dLUk2HS4UMoL4j5yHNORNw;',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/farandride/?hl=de',
            'user-agent': ua,
            'x-asbd-id': '129477',
            'x-csrftoken': 'dLUk2HS4UMoL4j5yHNORNw',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-requested-with': 'XMLHttpRequest',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # print(response.headers)
            # print(response.text)
            data = response.json()
            print("Fetched Instagram data.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

        media = []
        for node in data['data']['user']['edge_owner_to_timeline_media']['edges']:

            for tn in node['node']['thumbnail_resources']:
                if tn['config_width'] == 480 or tn['config_height'] == 480:
                    thumb = tn['src']

            media.append({"taken_at_timestamp":node['node']['taken_at_timestamp'],"description":node['node']['edge_media_to_caption']['edges'][0]['node']['text'], "thumbnail_src": thumb})

        media.sort(key=lambda x: x['taken_at_timestamp'], reverse=True)

        print(media)

        return media

    except:
        logging.exception("An error occurred scraping Instagram")

