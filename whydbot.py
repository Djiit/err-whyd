# coding: utf-8
from http import client
from socket import timeout
import json

from errbot import BotPlugin, botcmd


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

        try:
            status, res = self.request_playlist(args)
        except timeout:
            return 'Oops, I can\'t reach whyd.com...'

        if status != 200:
            return 'Oops, something went wrong.'

        return 'Last {user} track on Whyd: {track}.'.format(
            user=args, track=self.format_track(res[0]))

    @botcmd
    def whyd_hot(self, message, args):
        """Display the top 3 track on Whyd.
        Example: !whyd hot
        """
        try:
            status, res = self.request_playlist('hot')
        except timeout:
            return 'Oops, I can\'t reach whyd.com...'

        if status != 200:
            return 'Oops, something went wrong.'

        return ('Current top tracks on Whyd:\n' +
                '\n'.join([self.format_track(i) for i in res['tracks'][:3]]))

    @staticmethod
    def format_track(track):
        """Format a single track."""
        return '{name} (https://whyd.com/c/{track_id})'.format(
            name=track['name'], track_id=track['_id'])

    @staticmethod
    def request_playlist(url):
        """Fetch whyd.com playlist."""
        conn = client.HTTPSConnection('whyd.com', timeout=5)
        conn.request('GET', '/{url}?format=json'.format(url=url))
        r = conn.getresponse()
        return r.status, json.loads(r.read().decode())
