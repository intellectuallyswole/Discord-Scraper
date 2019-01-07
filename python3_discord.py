'''
''  @author KimChoJapFan <https://github.com/KimChoJapFan>
''  @date   November 13, 2018
''  @target Python 3.7.0+
'''

# Discord uses SSL and there's no need to make any connections over HTTP.
# Create folders and files in respective subfolders.
# Read JSON into a Python list.
# Write to STDERR and STDOUT.
# Allow for multiple downloads at a time.
# Choose random value from a list using MT19937.

from http.client import HTTPSConnection
from os import path, makedirs, getcwd
from json import loads as json_load
from sys import stderr, stdout
from threading import Thread
from random import choice

# Set our filename appropriate character set for files with duplicate filenames.
# Select a random string from our character set.

charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
randoms = lambda length: ''.join(choice(charset) for i in range(length))


'''
''  Discord Class
'''
class Discord:

    '''
    ''  Discord Class Constructor
    ''
    ''  @param config
    '''
    def __init__(self, config='config.json'):

        # Throw an error and close the script if the configuration file isn't found.
        if not path.exists(path.join(getcwd(), 'config.json')):
            stderr.write('Configuration file not found.\n')
            exit(1)

        # Open and read the JSON contents of the configuration file.
        with open('config.json', 'r') as file_handler:
            config_data = json_load(file_handler.read())

        # Throw an error and close the script if the configuration is missing an authorization token.
        if not config_data['token']:
            stderr.write('Missing Discord Authorization Token.\n')
            exit(1)

        # Throw an error and close the script if the configuration is set to scrape no servers.
        if not config_data['servers'] or len(config_data['servers']) == 0:
            stderr.write('Missing servers to crawl.\n')
            exit(1)

        # Set our User-Agent string.
        # Set our Authorization token.
        # Set our threaded stack array.

        self.agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.301 Chrome/56.0.2924.87 Discord/1.6.15 Safari/537.36'
        self.auth  = config_data['token']
        threads    = []
        
        # Traverse all servers and channels in the configuration.
        for server_id, v in config_data['servers'].items():
            for channel_id in config_data['servers'][server_id]:
                
                # Create our scraper folders.
                scrape_folder = path.join(getcwd(), 'Discord Scrapes', server_id, channel_id)
                if not path.exists(scrape_folder):
                    makedirs(scrape_folder)

                # Add queues to our threaded stack.
                for offset in range(0, 100):
                    thread = Thread(target=self.grabInfo, args=(server_id, channel_id, offset * 25, ))
                    threads.append(thread)

                # Execute threaded stack queues.
                for thread in threads:
                    thread.start()
                    thread.join()

                # Empty threaded stack.
                del threads[:]

                
    '''
    ''  Grab the JSON information from our search query.
    ''
    ''  @param serverid
    ''  @param channelid
    ''  @param offset
    '''
    def grabInfo(self, server_id, channel_id, offset):

        # Create an HTTPS connection to discordapp.com
        conn = HTTPSConnection('discordapp.com', 443)

        # Request all images and videos in the selected channel.
        conn.request(
            'GET',
            '/api/v6/guilds/{0}/messages/search?has=image&has=video&channel_id={1}&offset={2}&include_nsfw=true'.format(server_id, channel_id, offset),
            headers={'user-agent': self.agent, 'authorization': self.auth}
        )

        # Gather server response
        resp = conn.getresponse()
        data = resp.read().decode('utf-8', 'replace')
        json = json_load(data)
        file_data = []
        
        # Handle all messages
        for messages in json['messages']:
            for i in range(len(messages)):
                for attachment in messages[i]['attachments']:
                    file_data.append([attachment['url'], attachment['filename']])

        # Remove duplicate files.
        seen = set()
        new_data = []

        for item in file_data:
            t = tuple(item)
            if t not in seen:
                new_data.append(item)
                seen.add(t)

        # Download the files.
        for url, filename in new_data:
            file_location = path.join(getcwd(), 'Discord Scrapes', server_id, channel_id, '{0}({1}).{2}'.format('.'.join(filename.split('.')[:-1]), randoms(10), filename.split('.')[-1]))
            file_url = '/{0}'.format('/'.join(url.split('/')[3::]))

            with open(file_location, 'wb') as file_stream:
                conn = HTTPSConnection('cdn.discordapp.com', 443)
                conn.request('GET', file_url)
                resp = conn.getresponse()
                file_stream.write(resp.read())

'''
''  Script entry point.
'''
if __name__ == '__main__':
    discord = Discord()