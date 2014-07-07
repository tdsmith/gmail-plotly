#!/usr/bin/env python2

import argparse
import datetime
import os
import httplib2
from retrying import retry
from decorator import decorator

from apiclient.discovery import build
import oauth2client as o2c
import oauth2client.client
import oauth2client.file
import oauth2client.tools

from plotly import plotly
from plotly import graph_objs as go

CONFIG_DIR = os.path.expanduser('~/.config/gmail-plotly')
CLIENT_SECRET_FILE = os.path.join(CONFIG_DIR, 'google_client_secret.json')
GMAIL_CREDENTIALS = os.path.join(CONFIG_DIR, 'gmail.storage')
PLOTLY_KEY_FILE = os.path.join(CONFIG_DIR, 'plotly_key')
PLOTLY_USERNAME_FILE = os.path.join(CONFIG_DIR, 'plotly_username')
PLOTLY_WORLD_READABLE = os.path.exists(os.path.join(CONFIG_DIR, 'plotly_make_public'))

OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

def g_authorized(flags):
    flow = o2c.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()
    credential_storage = o2c.file.Storage(GMAIL_CREDENTIALS)
    credentials = credential_storage.get()
    if credentials is None or credentials.invalid:
        credentials = o2c.tools.run_flow(flow, credential_storage, flags)
    http = credentials.authorize(http)
    return build('gmail', 'v1', http=http)

is_none = lambda result: result is None

@decorator
def none_on_fail(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except:
        return None

@none_on_fail
@retry(stop_max_attempt_number=5,
       wait_exponential_multiplier=1000,
       wait_exponential_max=16000)
def count_threads(gmail_service, q):
    print q
    gmail_threads = gmail_service.users().threads()
    request = gmail_threads.list(userId='me', q=q, fields='nextPageToken,threads/id')
    threads = []
    while request:
        response = request.execute()
        if 'threads' in response and response['threads']:
            threads.extend(response['threads'])
        else:
            raise KeyError(response)
        request = gmail_threads.list_next(request, response)
    print '  ', len(threads)
    return len(threads)

def grab(filename):
    with open(filename) as f:
        return f.readlines()[0][:-1]

def main():
    parser = argparse.ArgumentParser(parents=[o2c.tools.argparser])
    parser.add_argument('--no-plot', help="don't plot", action='store_true')
    flags = parser.parse_args()

    gmail_service = g_authorized(flags)
    searches = {'primary_unread': 'category:primary is:unread',
                'primary_total': 'category:primary',
                'inbox_unread': 'in:inbox is:unread',
                'inbox_total': 'in:inbox'}
    counts = {key: count_threads(gmail_service, search) for key, search in searches.iteritems()}

    if flags.no_plot: return

    plotly_key = grab(PLOTLY_KEY_FILE)
    plotly_username = grab(PLOTLY_USERNAME_FILE)

    polite_names = {'primary_unread': 'Primary inbox, unread',
                    'primary_total': 'Primary inbox',
                    'inbox_unread': 'Inbox, unread',
                    'inbox_total': 'Inbox'}

    now = datetime.datetime.now()
    data = go.Data([go.Scatter(x=[now], y=[counts[key]], mode='lines+markers', name=polite_names[key]) for key in counts])
    layout = go.Layout(title="Emails in inbox")
    fig = go.Figure(data=data, layout=layout)
 
    plotly.sign_in(plotly_username, plotly_key)
    url = plotly.plot(fig, filename='gmail-plotly', fileopt='extend', world_readable=PLOTLY_WORLD_READABLE, auto_open=False)
    print url

if __name__ == '__main__':
    main()
