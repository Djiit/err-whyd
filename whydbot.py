import json
try:
    from http import client
except ImportError:
    import httplib as client

from errbot import BotPlugin, botcmd, arg_botcmd


class WhydBot(BotPlugin):
    """
    Basic Err integration with whyd.com
    """

    @botcmd
    def whyd_last(self, message, args):
        """Display the last track of a user.
        Example: !whyd last djiit
        """
        if len(args) < 1:
            return 'I need a username to fetch hist last track!'

        status, res = self.request_playlist(args)

        if status != 200:
            return 'Oops, something went wrong.'

        return 'Last {user} track on Whyd: {track}.'.format(
            user=args, track=self.format_track(res[0]))

    @botcmd
    def whyd_hot(self, message, args):
        """Display the top 3 track on Whyd.
        Example: !whyd hot
        """
        status, res = self.request_playlist('hot')

        if status != 200:
            return 'Oops, something went wrong.'

        yield 'Current top tracks on Whyd:'

        yield '\n'.join([self.format_track(i) for i in res['tracks'][:3]])

    @staticmethod
    def format_track(track):
        """Format a single track."""
        return '{name} (https://whyd.com/c/{track_id})'.format(
            name=track['name'], track_id=track['_id'])

    @staticmethod
    def request_playlist(url):
        """Fetch whyd.com playlist."""
        conn = client.HTTPSConnection('whyd.com')
        conn.request('GET', '/{url}?format=json'.format(url=url))
        r = conn.getresponse()
        return r.status, json.loads(r.read().decode())
