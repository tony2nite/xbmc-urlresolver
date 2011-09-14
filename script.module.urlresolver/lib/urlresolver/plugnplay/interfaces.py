#    urlresolver XBMC Addon
#    Copyright (C) 2011 t0mm0
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
This module defines several interfaces that you can implement when writing 
your URL resolving plugin.

* :class:`UrlResolver`: Resolves URLs. All plugins should implement this.
* :class:`SiteAuth`: Handles logging in to the file hoster.
* :class:`PluginSettings`: Allows a plugin to save and retrieve settings.

Interfaces you wish to implement must be included in the inheritance list of
you class definition, as well as added to the ``implements`` attribute of your
class.

For example, if you want to implement all the available interfaces, your plugin 
should be defined as follows::

        class MyPluginResolver(Plugin, UrlResolver, SiteAuth, PluginSettings):
            implements = [UrlResolver, SiteAuth, PluginSettings]

'''

import urlresolver
from urlresolver import common
from urlresolver.plugnplay import Interface
import sys

def _function_id(obj, nFramesUp):
	'''Create a string naming the function n frames up on the stack.'''
	fr = sys._getframe(nFramesUp+1)
	co = fr.f_code
	return "%s.%s" % (obj.__class__, co.co_name)


def not_implemented(obj=None):
	'''Use this instead of ``pass`` for the body of abstract methods.'''
	raise Exception("Unimplemented abstract method: %s" % _function_id(obj, 1))

class UrlResolver(Interface):
    priority=100
    
    
class NewUrlResolver(Interface):
    '''
    Your plugin needs to implement the abstract methods in this interface if
    it wants to be able to resolve URLs (which is probably all plugins!)
    
    .. note:: 
    
        You **MUST** override :meth:`get_media_url` and :meth:`valid_url` as 
        well as :attr:`name`.
    
    There are also a couple of utlity methods which you should probably not 
    override.
    '''
    
    name = 'override_me'
    '''(str) A human readable name for your plugin.'''

    priority = 100
    '''
    (int) The order in which plugins will be tried. Lower numbers are tried 
    first.
    '''    
    
    
    def get_media_url(self, web_url):
        '''
        The part of your plugin that does the actual resolving. You must 
        implement this method.
        
        Ths method will be passed the URL ofa web page associated with a media
        file. It will only get called if your plugin's :meth:`valid_url` method
        has returned ``True`` so it will definitely be a URL for the file host
        (or hosts) your plugin is capable of resolving (assuming you implemented
        :meth:`valid_url` correctly!)
        
        The URL you return must be something that is playable by XBMC.
        
        If for any reason you cannot resolve the URL (eg. the file has been 
        removed) then return ``False`` instead.
        
        Args:
            web_url (str): A URL to a web page associated with a piece of media
            content.
            
        Returns:
            If the ``web_url`` could be resolved, a string containing the direct 
            URL to the media file, if not, returns ``False``.    
        '''
        not_implemented(self)
    

    def get_url(self, host, media_id):
        not_implemented(self)
        

    def get_host_and_id(self, url):
        not_implemented(self)


    def valid_url(self, web_url):
        '''
        Determine whether this plugin is capable of resolving this URL. You must 
        implement this method.
        
        The usual way of implementing this will be using a regular expression
        which returns ``True`` if the URL matches the pattern (or patterns)
        used by the file host your plugin can resolve URLs for. 

        Args:
            web_url (str): A URL to a web page associated with a piece of media
            content.
            
        Returns:
            ``True`` if this plugin thinks it can resolve the ``web_url``, 
            otherwise ``False``.
        '''
        not_implemented(self)
    

    def get_media_urls(self, web_urls):
        '''
        .. warning::
        
            Do not override this method!
            
        Calls :meth:`get_media_url` on each URL in a list. May not be very
        useful!
        
        Args:
            web_urls (str): A list of URLs to web pages associated with media
            content.
            
        Returns:
            A list of results - if the ``web_url`` could be resolved, a string 
            containing the direct URL to the media file, if not, returns 
            ``False``.    
        '''
        ret_val = []
        for web_url in web_urls:
            url = self.get_media_url(web_url)
            if url:
                ret_val.append(url)
        return ret_val
    

    def filter_urls(self, web_urls):
        '''
        .. warning::
        
            Do not override this method!
            
        Calls :meth:`get_media_url` on each URL in a list. May not be very
        useful!
        
        Args:
            web_urls (str): A list of URLs to web pages associated with media
            content.
            
        Returns:
            A list of results - ``True`` if this plugin thinks it can resolve 
            the ``web_url``, otherwise ``False``.
        '''
        ret_val = []
        for web_url in web_urls:
            valid = self.valid_url()
            if valid:
                ret_val.append(web_url)
        return



class SiteAuth(Interface):
    '''
    Your plugin should implement this interface if the file hoster you are 
    resolving URLs for requires authentication. You may also implement it if
    the file hoster supports authentication but doesn't require it.
    '''


    def login(self):
        '''
        This method should perform the login to the file host site. This will 
        normally involve posting credentials (stored in your plugin's settings)
        to a web page which will set cookies. 
        '''
        not_implemented(self)



class PluginSettings(Interface):
    '''
    Your plugin needs to implement this interface if your plugin needs to store
    settings. 
    
    Plugin settings are global. This means that the user only needs to set your 
    plugin settings (such as username and password) once and they will be 
    available when your plugin is called from any XBMC addon.
    
    Addons can display all :mod:`urlresolver` settings including those of all
    available plugins by calling :func:`urlresolver.show_settings`.
    
    If you only want a 'priority' setting for your plugin, all you need to do
    is add this interface to he classes your plugin inherits from and to the 
    ``implements`` attribute without overriding anything.
    
    To do this your class should begin::
    
        class MyPluginResolver(Plugin, UrlResolver, PluginSettings):
            implements = [UrlResolver, PluginSettings]
            name = "myplugin"

    If you want custom settings you mut override :meth:`get_settings_xml`.
    
    You should never override :meth:`get_setting`.
    '''
    
    def get_settings_xml(self):
        '''
        This method should return XML which describes the settings you would 
        like for your plugin. You should make sure that the ``id`` starts
        with your plugins class name (which can be found using 
        :attr:`self.__class__.__name__`) followed by an underscore.
        
        For example, the following is the code included in the default 
        implementation and adds a priority setting::
        
            xml = '<setting id="%s_priority" ' % self.__class__.__name__
            xml += 'type="number" label="Priority" default="100"/>\\n'
            return xml 
            
        Although of course you know the name of your plugin(!) so you can just 
        write::
        
            xml = '<setting id="MyPlugin_priority" '
            xml += 'type="number" label="Priority" default="100"/>\\n'
            return xml 

        The settings category will be your plugin's :attr:`UrlResolver.name`.
        
        I would link to some documentation of ``resources/settings.xml`` but
        I can't find any. Suggestions welcome!
        
        Override this method if you want your plugin to have more settings than
        just 'priority'. If you do and still want the priority setting you 
        should include the priority code as above in your method.
        
        Returns:
            A string containing XML which would be valid in 
            ``resources/settings.xml``
        '''
        xml = '<setting id="%s_priority" ' % self.__class__.__name__
        xml += 'type="number" label="Priority" default="100"/>\n'
        return xml 
        
    
    def get_setting(self, key):
        '''
        .. warning::
        
            Do not override this method!
            
        Gets a setting that you have previously defined by overriding the 
        :meth:`get_settings_xml` method.
        
        When requesting a setting using this method, you should not include
        the ``MyPlugin_`` prefix of the setting id you defined in 
        :meth:`get_settings_xml`.
        
        For example, if you defined a setting with an id of 
        ``MyPlugin_username``, you would get the setting from your plugin 
        using::
        
            self.get_setting('username')
            
        Args:
            key (str): The name of the setting to retrieve (without the prefix).
            
        Returns:
            A string containing the value stored for the requested setting.
        '''
        value = common.addon.get_setting('%s_%s' % 
                                                (self.__class__.__name__, key))
        return value
    
