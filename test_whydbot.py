# coding: utf-8
from errbot.backends.test import testbot

import whydbot


class TestMeetUpPlugin(object):
    extra_plugin_dir = '.'

    def test_whyd_hot(self, testbot):
        testbot.push_message('!whyd hot')
        assert ('Current top track on Whyd:' in testbot.pop_message())

    def test_whyd_last(self, testbot):
        testbot.push_message('!whyd last djiit')
        assert ('Last djiit track on Whyd:' in testbot.pop_message())


class TestMeetUpPluginStaticMethods(object):

    def test_format_track(self):
        data = {
            '_id': '56f908cb8f4e437c7f6f41cf',
            'text': '',
            'src': {
                'name': 'Saga Africa by Frangi',
                'id': 'https://soundcloud.com/frangiparis/saga-africa'},
            'lov': [
                '5114c4fc7e91c862b2aabbda',
                '552555f97d50a7417678a233',
                '55d4c6b04bf212908fb477c4',
                '52e597807e91c862b2b43735'],
            'ctx': 'bk',
            'score': 1100,
            'rankIncr': None,
            'img': 'https://i1.sndcdn.com/artworks-000154298371-zm9z31-t300x300.jpg',
            'isMailed': {
                'top3': 1},
            'nbP': 141,
            'eId': '/sc/frangiparis/saga-africa#https://api.soundcloud.com/tracks/255271990/stream',
            'nbL': 6,
            'uNm': 'BPM : le Blog des Pépites Musicales',
            'uId': '51b382bc7e91c862b2ae94d7',
            'nbR': 16,
            'trackId': '56f908324bf212908fb777fb',
            'name': 'Frangi - Saga Africa'
        }
        
        result = whydbot.WhydBot.format_track(data)
        assert result == 'Frangi - Saga Africa (https://whyd.com/c/56f908cb8f4e437c7f6f41cf)'
