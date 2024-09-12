import os
import re
import time
import requests
from tqdm import tqdm


def find_id_in_script(script_text, id_pattern):
    pattern = re.compile(id_pattern)
    matches = pattern.findall(script_text)
    return matches

class Instapy:
    def __init__(self, cookies, headers=None):
        self.cookies = cookies
        self.headers = headers

    def get_user_id(self, username=None):

        print("Getting user id for user: ", username)

        if username is None:
            raise ValueError("Username is required")
        if self.cookies is None:
            raise ValueError("You need to provide the instagram cookie when creating the instapy instance")
        

        response = requests.get(f'https://www.instagram.com/{username}/', cookies=self.cookies)

        if response.status_code == 200:
            user_id = find_id_in_script(response.text, r'"id":"(\d+)"')[0]
            print("User id for", username, "is:", user_id)
            return user_id
        else:
            print("server returned ", response.status_code, " status code")
            raise ValueError("Error getting user id")
    
    def get_reels_links(self, user, count=12, user_id=None):

        if user is None:
            raise ValueError("User id is required for getting the reels")
        if self.cookies is None:
            raise ValueError("You need to provide the instagram cookie when creating the instapy instance")
        
        if user_id is None:
            user_id = self.get_user_id(user)

        variables = {'variables': f'{{"data":{{"count":{count},"include_relationship_info":true,"latest_besties_reel_media":true,"latest_reel_media":true}},"username":"{user}","__relay_internal__pv__PolarisIsLoggedInrelayprovider":true,"__relay_internal__pv__PolarisFeedShareMenurelayprovider":true}}'}
        
        data = {
            'av': user_id,
            'doc_id': '8388565321195220',
        }
        data.update(variables)
        print("Getting reels links")
        response = requests.post('https://www.instagram.com/graphql/query', cookies=self.cookies,  data=data)
        links = []
        if response.status_code == 200:
            nodes = response.json()['data']['xdt_api__v1__feed__user_timeline_graphql_connection']['edges']
            for node in nodes:
                video_url = node['node']['code']
                links.append(video_url)
            last_id = nodes[-1]['node']['id']
        else:
            print("server returned ", response.status_code, " status code")
            raise ValueError("Error getting reels links")
        
        for i in range(12, count, 12):
            try:
                variables = {'variables': f'{{"after":"{last_id}","before":null,"data":{{"count":{count - i},"include_relationship_info":true,"latest_besties_reel_media":true,"latest_reel_media":true}},"username":"{user}","__relay_internal__pv__PolarisIsLoggedInrelayprovider":true,"__relay_internal__pv__PolarisFeedShareMenurelayprovider":true}}'}
                data = {
                    'av': user_id,
                    'doc_id': '8388565321195220',
                }
                data.update(variables)
                response = requests.post('https://www.instagram.com/graphql/query', cookies=self.cookies,  data=data)
                if response.status_code == 200:
                    nodes = response.json()['data']['xdt_api__v1__feed__user_timeline_graphql_connection']['edges']
                    for node in nodes:
                        video_url = node['node']['code']
                        links.append(video_url)
                else:
                    print("server returned ", response.status_code, " status code")
                    raise ValueError("Error getting reels links")
                if len(nodes) == 0:
                    break
                last_id = nodes[-1]['node']['id']
            except:
                print("error getting all the reels")

        urls = [f'https://www.instagram.com/reel/{url}/' for url in links]
        if count != len(urls) and count < len(urls):   
            urls = urls[0:count]
        print("Got:", len(urls), "reels links")
        return urls
    
    def get_job_id(self, link):

        if link is None:
            raise ValueError("Error getting job id for reel download. (This is an internal error)")
        
        print("Getting job id...")

        headers = {
            'accept':
            '*/*',
            'accept-language':
            'en-US,en;q=0.9',
            'content-type':
            'application/json;',
            'origin':
            'https://publer.io',
            'priority':
            'u=1, i',
            'referer':
            'https://publer.io/',
            'sec-ch-ua':
            '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile':
            '?0',
            'sec-ch-ua-platform':
            '"Windows"',
            'sec-fetch-dest':
            'empty',
            'sec-fetch-mode':
            'cors',
            'sec-fetch-site':
            'same-site',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        json_data = {
            'url': link,
            'iphone': False,
        }

        response = requests.post('https://app.publer.io/hooks/media', headers=headers, json=json_data)

        if response.status_code == 200:  
            job_id = response.json()["job_id"]
            print("Job id for the download is:", job_id)
            return job_id
        else:
            raise ValueError("Error getting job id for download")
    
    def download_reels(self, reels_links=None, count=12, user=None, user_id=None, path="videos"):
        if reels_links is None:
            if user is None:
                raise ValueError("You need to provide user")
            if user_id is None:
                user_id = self.get_user_id(user)
            
            reels_links = self.get_reels_links(user, count, user_id)

        print("Starting the download process...")
        for link in reels_links:
            job_id = self.get_job_id(link)

            # INIT JOB
            response = requests.get(f'https://app.publer.io/api/v1/job_status/{job_id}')
            print("Waiting for download to start")
            time.sleep(1)

            # WAIT FOR VIDEO TO BE READY FOR DOWNLOAD
            while response.json()["status"] != "complete":
                response = requests.get(f'https://app.publer.io/api/v1/job_status/{job_id}')
                time.sleep(1)

            downloadLink = response.json()['payload'][0]['path']
            title = f"{link.split('/')[-2]}.mp4"
            os.makedirs(path, exist_ok=True)


            print("Downloading reel...")
            response = requests.get(downloadLink, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            with open(f"{path}/{title}", 'wb') as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            progress_bar.close()
            print("Download video", reels_links.index(link) + 1, "of", len(reels_links))
    def scrape_page(self, user, count=12, path="videos"):
        user_id = self.get_user_id(user)
        reels_links = self.get_reels_links(user, count=count, user_id=user_id)
        self.download_reels(reels_links=reels_links, path=path)

   