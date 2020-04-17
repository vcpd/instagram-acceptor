#YOU WILL NEED THE REQUESTS AND COLORAMA MODULES INSTALLED TO USE!

import requests, time
from colorama import init

RED = "\033[1;31;40m"
GREEN = "\033[1;32;40m"
WHITE = "\033[1;37;40m"

class instagram_web:
    def __init__(self):
        self.s = requests.session()
        self.csrf = None
        self.accepted = 0

    def login(self, username, password):
        self.s.get(url='https://www.instagram.com/accounts/login/', headers={
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"})
        self.csrf = self.s.cookies.get('csrftoken')
        login_response = self.s.post('https://www.instagram.com/accounts/login/ajax/', headers={'origin': "www.instagram.com",
                          'accept-encoding': "gzip, deflate, br",
                          'accept-language': "en-US,en;q=0.9",
                          'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                          'x-requested-with': "XMLHttpRequest",
                          'x-csrftoken': self.csrf,
                          'x-instagram-ajax': "-hot",
                          'content-type': "application/x-www-form-urlencoded",
                          'accept': "/",
                          'referer': 'https://www.instagram.com/accounts/login%22%7D'},
                          data={'username': username, 'password': password})

        if 'authenticated": true,' in str(login_response.text):
            print(f'Successfully logged into @{username}')
            return True
        elif 'authenticated": false' in login_response.text:
            print('Please check your username or password and try again')
        elif 'checkpoint_required' in login_response.text:
            print('Username and password is correct but there was suspicious login. \nTry to accept and try again. If you have 2fac login then this tool will not work for you')
        else:
            print(login_response.text)
            return False

    def pull(self):
        try:
            pull = self.s.get(url='https://www.instagram.com/accounts/activity/?__a=1&include_reel=true', headers={
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': 'mid={}; csrftoken={}; ds_user_id={}; shbid={}; shbts={}; datr={}; rur={}; sessionid={}; urlgen={}'.format(
                    self.s.cookies.get('mid'), self.s.cookies.get('cserftoken'), self.s.cookies.get('ds_user_id'),
                    self.s.cookies.get('shbid'), self.s.cookies.get('shbts'), self.s.cookies.get('datr'),
                    self.s.cookies.get('rur'), self.s.cookies.get('sessionid'), self.s.cookies.get('urlgen')),
                'referer': 'https://www.instagram.com/accounts/activity/',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
                'x-requested-with': 'XMLHttpRequest',
            })
            if pull.status_code == 200:
                print('Successfully pulled requested user information')
                return pull.text
            else:
                print(f'Error pulling requested users  |  {pull.text}')
                return False
        except Exception as e:
            print(e)

    def accept_user(self, userid):
        accept_response = self.s.post(f'https://www.instagram.com/web/friendships/{userid}/approve/', headers={
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'mid={}; shbid={}; shbts={}; datr={}; rur={}; csrftoken={}; ds_user_id={}; sessionid={}; urlgen={}'.format(
                self.s.cookies.get('mid'), self.s.cookies.get('shbid'), self.s.cookies.get('shbts'),
                self.s.cookies.get('datr'), self.s.cookies.get('rur'), self.s.cookies.get('csrftoken'),
                self.s.cookies.get('ds_user_id'), self.s.cookies.get('sessionid'), self.s.cookies.get('urlgen')),
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/activity/?followRequests=1',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
            'x-csrftoken': self.s.cookies.get('csrftoken'),
            'x-requested-with': 'XMLHttpRequest'
        })
        if accept_response.status_code == 200:
            return True
        else:
            return False

def main():
    init()
    print(f'>>Simple Instagram Acceptor | @xeou<<\n')
    login_username = input("username: ")
    login_password = input("password: ")
    instagram = instagram_web()
    if instagram.login(login_username, login_password):
        pull_response = instagram.pull()
        if not str(pull_response) == False:
            cycle = 1
            accepted = 0
            while True:
                try:
                    cycle += 1
                    userid = str(pull_response).split('GraphUser","id":"')[cycle].split('"')[0]

                    if len(userid) > 20:
                        continue
                    if instagram.accept_user(userid):
                        accepted += 1
                        print(f'[{accepted}]  {GREEN}Accepted {userid}{WHITE}')
                        time.sleep(.7)
                    else:
                        print(f'{RED}Error accepting {userid}{WHITE}')
                        time.sleep(.7)
                except Exception as e:
                    break
            print(f'Accepted {accepted} accounts')
            input('Enter to close')
    else:
        input('Fix any issues and try again or contact @xeou on IG for help')

main()


