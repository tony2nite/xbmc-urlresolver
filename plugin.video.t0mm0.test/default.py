'''
    t0mm0 test XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import re
import string
import sys
import xbmcplugin
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from urlresolver import common
import urlresolver
import urllib2


def get_movie_page(url, deep = False):
	success = False
	try:
		html = net.http_GET(url).content
		success = True
	except urllib2.HTTPError, e:
		 addon.log_debug('HTTP Error: %s' % e)
	
	if success:
		# get total pages
		p_r = '(\d+)</a></li><li title="Next Page".+?href="(.+?)(\d+)\/".+?<'
		pages_regex = re.finditer(p_r, html)
		total_pages = 1
		for s in pages_regex:
			total_pages, url, current_page = s.groups()
		#<div class="list_item.+?src="(.+?)".+?(frelease dvd|frelease) to get dvd symbol
		# scan items
		r = '<div class="list_item.+?src="(.+?)".+?(frelease dvd|frelease).+?<a class="plot".+?href="(.+?)".+?<b>(.+?)<\/b>(.+?)<.+?Rank: ([\d\.]+) Votes:(\d+).+?'
		regex = re.finditer(r, html, re.DOTALL)
		total_items = 0
		for s in regex:
			thumb, dvd, url, title, plot, rating, votes = s.groups()
			if dvd.find("dvd") != -1:
			    dvd = " (DVD)"
			else:
			    dvd = ""
			total_items += 1
			addon.add_directory({'mode': 'movie',
								 'url': base_url + url,
								 'imageurl': base_url + thumb},
								 {
								 'title': title + dvd,
								 'votes': int(votes),
								 'rating': float(rating),
								 'plotoutline': plot,
								 'secondlabel': dvd
								 },
								 img=base_url+thumb,
								 total_items=int(total_pages)*10)
		
		# get next page
		if deep == True:
			pages_regex = re.finditer(p_r, html)
			for s in pages_regex:
				total_pages, url, current_page = s.groups()
				print "%s page of %s" % (total_pages, current_page)
				get_movie_page(base_url + url + current_page + "/")

 
addon = Addon('plugin.video.t0mm0.test', sys.argv)
net = Net()


logo = os.path.join(addon.get_path(), 'art','logo.jpg')

base_url = 'http://tubeplus.me'

mode = addon.queries['mode']
play = addon.queries.get('play', None)
print "mode=" + mode
if play:
    url = addon.queries.get('url', '')
    host = addon.queries.get('host', '')
    media_id = addon.queries.get('media_id', '')
    #stream_url = urlresolver.resolve(play)
    stream_url = urlresolver.HostedMediaFile(url=url, host=host, media_id=media_id).resolve()
    addon.resolve_url(stream_url)

elif mode == 'resolver_settings':
    urlresolver.display_settings()

elif mode == 'test':
    addon.add_video_item({'url': 'http://www.2gb-hosting.com/v/94fb733db6e9f984b07da3cb238eb277/2074fe10f41c7e1.flv.html'},
                         {'title': '2gbhosting url'})
    addon.add_video_item({'host': '2gb-hosting.com', 'media_id': 'e1593e96e19f7ecced3778668e809c77/efc5d03968fbca6.avi.html'},
                         {'title': '2gbhosting media id'})
    addon.add_video_item({'url': 'http://www.divxstage.eu/video/eb20c352c3ccc'},
                         {'title': 'divxstage url'})
    addon.add_video_item({'host': 'divxstage.eu', 'media_id': 'eb20c352c3ccc'},
                         {'title': 'divxstage media id'})
    addon.add_video_item({'url': 'http://www.ecostream.tv/stream/b83c3c5d07b1ab195fb8245576c27daa.html?' +
                          'width=679&height=365&bGetRedirectUrl=False&sFileName=Larry+Crowne'},
                         {'title': 'ecostream url'})
    addon.add_video_item({'host': 'ecostream', 'media_id': 'b83c3c5d07b1ab195fb8245576c27daa'},
                         {'title': 'ecostream media id'})
    addon.add_video_item({'url': 'http://flashx.tv/video/OKY777MKOXGO/Contagion-TSMD'},
                         {'title': 'flashx url'})
    addon.add_video_item({'host': 'flashx','media_id': '1503'},
                         {'title': 'flashx media id'})
    addon.add_video_item({'url': 'http://www.megaupload.com/?d=9T8NHCK4'},
                         {'title': 'megaupload url'})
    addon.add_video_item({'host': 'megaupload.com', 'media_id': '9T8NHCK4'},
                         {'title': 'megaupload media id'})
    addon.add_video_item({'url': 'http://www.megavideo.com/?v=LYWNYM1J'},
                         {'title': 'megavideo url'})
    addon.add_video_item({'host': 'megavideo.com', 'media_id': 'LYWNYM1J'},
                         {'title': 'megavideo media id'})
    addon.add_video_item({'url': 'http://www.movshare.net/video/rnqmuilri1b71'},
                         {'title': 'movshare url'})
    addon.add_video_item({'host': 'movshare.net', 'media_id': 'rnqmuilri1b71'},
                         {'title': 'movshare media id'})
    addon.add_video_item({'url': 'http://www.nolimitvideo.com/video/bdb6e2c62fe027a7b20a/friends-with-benefits-ts'},
                         {'title': 'nolimitvideo url'})
    addon.add_video_item({'host': 'nolimitvideo.com', 'media_id': 'bdb6e2c62fe027a7b20a'},
                         {'title': 'nolimitvideo media id'})
    addon.add_video_item({'url': 'http://embed.novamov.com/embed.php?width=600&height=480&v=kdshwq2cj6vxv&px=1'},
                         {'title': 'novamov url'})
    addon.add_video_item({'host': 'novamov.com', 'media_id': 'kdshwq2cj6vxv'},
                         {'title': 'novamov media id'})
    addon.add_video_item({'url': 'http://www.putlocker.com/file/A280B88DADE9B8ED'},
                         {'title': 'putlocker url'})
    addon.add_video_item({'host': 'putlocker.com', 'media_id': 'A280B88DADE9B8ED'},
                         {'title': 'putlocker media id'})
    addon.add_video_item({'url': 'http://rapidvideo.com/view/hwksai28'},
                         {'title': 'rapidvideo url'})
    addon.add_video_item({'host': 'rapidvideo', 'media_id': 'hwksai28'},
                         {'title': 'rapidvideo media id'})
    addon.add_video_item({'url': 'http://www.seeon.tv/view/19412/CBS'},
                         {'title': 'seeon.tv url'})
    addon.add_video_item({'host': 'seeon.tv', 'media_id': '19412'},
                         {'title': 'seeon.tv media id'})
    addon.add_video_item({'url': 'http://www.sharefiles4u.com/pknlizmgi6mw/contagion-md-dubbed-german.avi'},
                         {'title': 'sharefiles url'})
    addon.add_video_item({'host': 'sharefiles','media_id': 'pknlizmgi6mw'},
                         {'title': 'sharefiles media id'})
    addon.add_video_item({'url': 'http://skyload.net/File/a25454887fd8cce41bac2e316d9d0a51.flv'},
                         {'title': 'skyload url'})
    addon.add_video_item({'host': 'skyload', 'media_id': 'a25454887fd8cce41bac2e316d9d0a51'},
                         {'title': 'skyload media id'})
    addon.add_video_item({'url': 'http://server4.stream2k.com/playerjw/vConfig56.php?vkey=1d8dc00940da661ffba9'},
                         {'title': 'stream2k url'})
    addon.add_video_item({'host': 'stream2k', 'media_id': '1d8dc00940da661ffba9'},
                         {'title': 'stream2k media id'})
    addon.add_video_item({'url': 'http://www.tubeplus.me/player/1962655/Entourage/season_8/episode_2/Out_With_a_Bang_/'},
                         {'title': 'tubeplus url'})
    addon.add_video_item({'host': 'tubeplus.me', 'media_id': '1962655'},
                         {'title': 'tubeplus media id'})
    addon.add_video_item({'url': 'http://www.ufliq.com/rw52re7f5aul'},
                         {'title': 'ufliq url'})
    addon.add_video_item({'host': 'ufliq', 'media_id': 'rw52re7f5aul'},
                         {'title': 'ufliq media id'})
    addon.add_video_item({'url': 'http://www.uploadc.com/wheon4xa0sh6'},
                         {'title': 'uploadc url'})
    addon.add_video_item({'host': 'uploadc.com', 'media_id': 'wheon4xa0sh6'},
                         {'title': 'uploadc media id'})
    addon.add_video_item({'url': 'http://videobb.com/video/8FvAG6AQpHi8'},
                         {'title': 'videobb url'})
    addon.add_video_item({'host': 'videobb.com', 'media_id': '8FvAG6AQpHi8'},
                         {'title': 'videobb media id'})
    addon.add_video_item({'url': 'http://www.videoweed.es/file/crirmdz3tj116'},
                         {'title': 'videoweed url'})
    addon.add_video_item({'host': 'videoweed.com', 'media_id': 'crirmdz3tj116'},
                         {'title': 'videoweed media id'})
    addon.add_video_item({'url': 'http://www.videozer.com/video/3LsT'},
                         {'title': 'videozer url'})
    addon.add_video_item({'host': 'videozer', 'media_id': '3LsT'},
                         {'title': 'videozer media id'})
    addon.add_video_item({'url': 'http://vidstream.us/video/7XK5WMYBAM5R/RAONE'},
                         {'title': 'vidstream url'})
    addon.add_video_item({'host': 'vidstream', 'media_id': '7XK5WMYBAM5R/RAONE'},
                         {'title': 'vidstream media id'})
    addon.add_video_item({'url': 'http://www.vidxden.com/rn3h4gbh5se7/kdshn-4x4_watchseries-online.dot.com.avi.html'},
                         {'title': 'vidxden url'})
    addon.add_video_item({'host': 'vidxden.com', 'media_id': 'rn3h4gbh5se7'},
                         {'title': 'vidxden media id'})
    addon.add_video_item({'url': 'http://www.vimeo.com/30081785'},
                         {'title': 'vimeo url'})
    addon.add_video_item({'host': 'vimeo.com', 'media_id': '30081785'},
                         {'title': 'vimeo media id'})
    addon.add_video_item({'url': 'http://xvidstage.com/v9t09l63m9vn'},
                         {'title': 'xvidstage url'})
    addon.add_video_item({'host': 'xvidstage', 'media_id': 'v9t09l63m9vn'},
                         {'title': 'xvidstage media id'})
    addon.add_video_item({'url': 'http://www.youtube.com/watch?v=Q3VJOl_XeGs'},
                         {'title': 'youtube url'})
    addon.add_video_item({'host': 'youtube.com', 'media_id': 'Q3VJOl_XeGs'},
                         {'title': 'youtube media id'})

elif mode == 'tv':
    browse = addon.queries.get('browse', False)
    if browse == 'alpha':
        letter = addon.queries.get('letter', False)
        if letter:
            url = 'http://tubeplus.me/browse/tv-shows/All_Genres/%s/' % letter
            html = net.http_GET(url).content
            r = '<div class="list_item.+?src="(.+?)".+?<a class="plot".+?' + \
                'href="(.+?)".+?<b>(.+?)<\/b>.+?<\/b>(.+?)<'
            regex = re.finditer(r, html, re.DOTALL)
            for s in regex:
                thumb, url, title, plot = s.groups()
                addon.add_directory({'mode': 'series',
                                     'url': base_url + url},
                                     {'title': title},
                                     img=base_url+thumb)

        else:
            addon.add_directory({'mode': 'tv',
                                 'browse': 'alpha',
                                 'letter': '-'}, {'title': '#'})
            for l in string.uppercase:
                addon.add_directory({'mode': 'tv',
                                     'browse': 'alpha',
                                     'letter': l}, {'title': l})

    else:
        addon.add_directory({'mode': 'tv', 'browse': 'alpha'}, {'title': 'A-Z'})
        
elif mode == 'movies':
    
    xbmc.executebuiltin("Container.SetViewMode(%s)" % 'movies' )
    xbmcplugin.setContent( int( sys.argv[ 1 ] ), 'movies') 
    
    browse = addon.queries.get('browse', False)
    if browse == 'alpha':
        letter = addon.queries.get('letter', False)
        if letter:
            url = 'http://tubeplus.me/browse/movies/All_Genres/%s/' % letter
            url = addon.queries.get('next_url', url)
            get_movie_page(url, True)
        else:
            addon.add_directory({'mode': 'movies',
                                 'browse': 'alpha',
                                 'letter': '-'}, {'title': '#'})
            for l in string.uppercase:
                addon.add_directory({'mode': 'movies',
                                     'browse': 'alpha',
                                     'letter': l}, {'title': l})
    elif browse == 'latest':
        print 'latest'
        url = 'http://www.tubeplus.me/browse/movies/Last/ALL/'
        get_movie_page(url)
        
    elif browse == 'popular':
        print 'popular'
        categoryurl = addon.queries.get('categoryurl', False)
        if categoryurl:
            get_movie_page(categoryurl, False)
        else:
            url = 'http://www.tubeplus.me'
            html = net.http_GET(url).content
            
            r = '<div id="popular">.+?<ul>(.+?)<\/ul>'
            regex = re.findall(r, html, re.DOTALL)
            
            r = 'href="(.+)">(.+?)</a>'
            regex = re.finditer(r, regex[0])
            
            for s in regex:
                url, title = s.groups()
                addon.add_directory({'mode': 'movies',
                                     'browse': 'popular',
                                     'categoryurl': base_url + url}, {'title': title})
    else:
        addon.add_directory({'mode': 'movies', 'browse': 'alpha'}, {'title': 'A-Z'})
        
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
        
elif mode == 'series':
    url = addon.queries['url']
    html = net.http_GET(url).content
    r = 'javascript:show_season\("(\d+?)","(.+?)"\)'
    regex = re.finditer(r, html, re.DOTALL)
    for s in regex:
        season, data = s.groups()
        episodes = data.split('||')
        for episode in episodes:
            params = episode.split('_')
            if len(params) == 5:
                ep_url = '%s/player/%s/' % (base_url, params[2])
                title = 'S%sE%s - %s (%s)' % (params[0], params[1],
                                              params[3], params[4])
                common.addon.log_debug('Episodes %s at %s' % (ep_url, title))
                addon.add_video_item({'url': ep_url}, {'title': title})

elif mode == 'movie':
    xbmc.executebuiltin("Container.SetViewMode(%s)" % 'movies' )
    
    url = addon.queries['url']
    html = net.http_GET(url).content
    
    r = "<h1>(.+?) \((\d+)\)</h1>.+<b>IMDB:</b>.+<span>tt(\d+)</span>"
    meta = re.findall(r, html, re.DOTALL)
    
    r = "<a.+?href=\"javascript:show\('(\w+?)','(.+?)', '(.+?)'.+?<b>(\d+)% said work.+?<\/b>"
    regex = re.finditer(r, html, re.DOTALL)
    for s in regex:
        id, title, host, quality = s.groups()
        addon.add_item({'host': host, 'media_id' : id},
                             {'title': u'%s (%s)' % (meta[0][0] , host),
                              'date': int(meta[0][1]),
                              'code': int(meta[0][2]),
                              'rating': float(quality),
                              'studio': host},
                              img=addon.queries['imageurl'],
                              is_playable=True,
                              is_folder=False,
                              item_type='video')
    xbmcplugin.setContent( int( sys.argv[ 1 ] ), 'movies') 
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_STUDIO )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )

elif mode == 'main':
    addon.show_small_popup('t0mm0 test addon', 'Is now loaded enjoy', 6000,
                           logo)
    addon.add_directory({'mode': 'test'}, {'title': '*test links*'})
    addon.add_directory({'mode': 'tv'}, {'title': 'tubeplus.me tv'})
    addon.add_directory({'mode': 'movies'}, {'title': 'tubeplus.me movies'})
    addon.add_directory({'mode': 'movies', 'browse': 'latest'}, {'title': 'tubeplus.me movies (latest releases)'})
    addon.add_directory({'mode': 'movies', 'browse': 'popular'}, {'title': 'tubeplus.me movies (popular categories)'})
    addon.add_directory({'mode': 'resolver_settings'}, {'title': 'resolver settings'}, is_folder=False)


if not play:
    addon.end_of_directory()

