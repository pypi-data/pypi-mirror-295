# github.com/sofullstack

import os
import datetime
import colorama
import json

class Logger:
    def __init__(self, type):
        self.types = {
            'success' : f'✅ {colorama.Fore.LIGHTGREEN_EX} ',
            'failure'  : f'❌ {colorama.Fore.LIGHTRED_EX} ',
            'warning' : f'⚠️  {colorama.Fore.LIGHTYELLOW_EX} ',
        }
        self.type = type

    def log(self, msg: str):
        if self.type.lower() not in self.types:
            return Logger('failure').log('Invalid log type')
        
        # colorama.Fore.<self.types.get(type)> , datetime.datetime.now()<extraction_logic> , msg , colorama.Fore.RESET
        return print(f'{{}}{{}} | {{}}{{}}'.format(self.types.get(self.type.lower()), str(datetime.datetime.now()).split(' ')[1].split('.')[0], msg, colorama.Fore.RESET))

class EasyAuthorization:
    def __init__(self):
        if os.path.exists('auth.json'):
            self.auth_file = json.load(open('auth.json'))
            Logger('success').log('Auth file loaded')
        else:
            Logger('warning').log('Auth file not found, creating...')
            open('auth.json','w+').write('[\n\n]')
            Logger('success').log('Auth file created')
            self.auth_file = json.load(open('auth.json'))
            Logger('success').log('Auth file loaded')    

    def login(self, username=None, password=None, license=None) -> dict:
        expired = lambda date: datetime.datetime.strptime(date, "%B %d %Y") < datetime.datetime.now()
        if username != None and password != None:
            for user in self.auth_file:
                if user['username'].lower() == username.lower() and user['password'] == password:
                    try:
                        if expired(user['expiry']):
                            return {
                                'status':'success',
                                'username':user['username'],
                                'expiry':'expired'
                            }
                        else:
                            return {
                                'status':'success',
                                'username':user['username'],
                                'expiry':user['expiry']
                            }
                    except ValueError:
                        # user['username'] , user['expiry']
                        Logger('failure').log(f'User "{{}}" has an invalid expiry -> "{{}}"'.format(user['username'], user['expiry']))
                        return {
                            'status':'login failed, check log output.'
                        }
            return {
                'status':'invalid login'
            }
        
        if license != None:
            for user in self.auth_file:
                if user['license'] == license:
                    try:
                        if expired(user['expiry']):
                            return {
                                'status':'success',
                                'license':user['license'],
                                'expiry':'expired'
                            }
                        else:
                            return {
                                'status':'success',
                                'license':user['license'],
                                'expiry':user['expiry']
                            }
                    except ValueError:
                        # user['username'] , user['expiry']
                        Logger('failure').log(f'User "{{}}" has an invalid expiry -> "{{}}"'.format(user['username'], user['expiry']))
                        return {
                            'status':'login failed, check log output.'
                        }
            return {
                'status':'invalid login'
            }
        
    def register(self, username=None, password=None, license=None, expiry=None) -> dict:
        if username != None and password != None and license==None:
            for user in self.auth_file:
                if user['username'] == username:
                    return {
                        'status':'user already exists'
                    }
            data = self.auth_file
            data.append({
                "username" : username,
                "password" : password,
                "license"  : 'na',
                "expiry"   : expiry
            })

            with open('auth.json', 'w') as f: 
                json.dump(data, f, indent=4)

            return {
                'status':'success',
                'username':username,
                'expiry':expiry
            }
        elif username != None and password != None and license != None:
            for user in self.auth_file:
                if user['username'] == username:
                    return {
                        'status':'user already exists'
                    }
                if user['license'] == license:
                    return {
                        'status':'license already exists'
                    }
            data = self.auth_file
            data.append({
                "username" : username,
                "password" : password,
                "license"  : license,
                "expiry"   : expiry
            })

            with open('auth.json', 'w') as f:
                json.dump(data, f, indent=4)
            
            return {
                'status':'success',
                'username':username,
                'expiry':expiry
            }
        elif username == None and password == None and license != None:
            for user in self.auth_file:
                if user['license'] == license:
                    return {
                        'status':'license already exists'
                    }
            data = self.auth_file
            data.append({
                "username" : 'na',
                "password" : 'na',
                "license"  : license,
                "expiry"   : expiry
            })

            with open('auth.json', 'w') as f:
                json.dump(data, f, indent=4)

            return {
                'status':'success',
                'license':license,
                'expiry':expiry
            }
        else:
            return {
                'status':'missing required params'
            }