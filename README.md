# gmail-plotly

A stupid gadget to plot the number of messages in your gmail inbox to plot.ly.

## Setup instructions

1. `git clone https://github.com/tdsmith/gmail-plotly`
1. `mkdir -p ~/.config/gmail-plotly` (or change `CONFIG_DIR`)
1. Set up a project in the [Google Developer's Console](https://console.developers.google.com//start/api?id=gmail&credential=client_key).
1. In the APIs & auth section on the left, choose APIs, and switch on the Gmail
   API.
1. In the sidebar on the left, select Credentials and expand the OAuth 2.0
   Client ID section. Choose "desktop app" and download the client secret
   JSON that's generated to `CONFIG_DIR/google_client_secret.json`.
1. Visit your plot.ly settings and copy-paste the API Key on the "Profile" tab
   into `CONFIG_DIR/plotly_key`.
1. `echo your_plotly_username > CONFIG_DIR/plotly_username`
1. If you would like to make your graph public so that you can embed it in
   webpages and other silliness, `touch CONFIG_DIR/plotly_make_public`.
1. From the gmail-plotly root, `virtualenv .` and activate with `.
   bin/activate`
1. `pip install -r requirements.txt`
1. Set up your Google credentials by running `./gmail-plotly.py --noauth_local_webserver` and following the directions. This will also add the first data point to your plot.ly graph. The URL will be printed at the end.
1. Add gmail-plotly to your crontab by having it run `run-external.sh`, which
   takes care of setting up the virtualenv. Or just run `gmail-plotly.py`
   whenever you want to update.

And now you have one of these:

<iframe id="igraph" style="border: none" src="https://plot.ly/~tdsmith/2/600/400"
    width="100%"></iframe>
