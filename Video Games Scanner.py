########################################################################################################################
#                                                                                                                      #
# This is a demo games/roms scanner. Video games, emulators, roms, etc. are not a feature Plex currently offers. The   #
# only thing you will see with this is a fancy listing for your games, they won't be playable. I do not think that     #
# Plex Inc. should offer it as a feaure in the future, but authors of emulators could include support in their         #
# products so that they could download roms (and upload saved games) back to a Plex Media Server.  John O.             #
#                                                                                                                      #
########################################################################################################################

import re, os, os.path, datetime, titlecase, unicodedata, sys, zipfile
import Media, VideoFiles, Stack, Utils, Filter, logging, time

logging.basicConfig(filename='/Users/john/plex_games.log',level=logging.DEBUG)

game_exts_x = {
  #"3DO":"3DO", 
  "AMIG": ['uae', 'adf'],
  #"AMST":"Amstrad", 
  "ANDR": ['apk'], 
  "ARCD": ['chd'], 
  "A26K": ['a26'], 
  "A52K": ['a52'],
  "A78K": ['a78'], 
  "JAG": ['jag', 'j64'], 
  "LYNX": ['lnx'],
  "AXL": ['xex','atr'], 
  "CV": ['col'],
  "C64": ['d64','g64','t64'],
  #"FAIR":"Fairchild", 
  #"IV":"Intellivision", 
  #"IOS":"iOS", 
  #"MAC":"Mac", 
  #"O2":"Odyssey 2", 
  #"XBOX":"Xbox", 
  #"X360":"Xbox 360", 
  #"XONE":"Xbox One", 
  "NEOP": ['ngp'],
  #"NEOC":"NeoGeo PC", 
  #"NEOG":"NeoGeo", 
  #"3DS":"3DS", 
  "N64": ['n64','v64','z64'],
  "DS": ['nds'], 
  "NES": ['nes','nez'],
  "GB": ['gb'],
  "GBA": ['gba','sgb'],
  "GBC": ['gbc'], 
  #"NGC":"GameCube", 
  "VB": ['vb'], 
  #"WII":"Wii", 
  #"WIIU":"Wii U", 
  #"OUYA":"Ouya", 
  "PC": ['exe'],
  #"CDI":"CD-i", 
  "33": ['32x'], 
  #"21":"Sega CD", 
  #"DREM":"Dreamcast", 
  "GG": ['gg'], 
  "SGEN": ['smd'], 
  #"SMS":"SMS", 
  #"36":"Mega Drive", 
  #"SATN":"Saturn", 
  "ZX": ['szx'],
  #"PS1":"PS1", 
  #"PS2":"PS2", 
  #"PS3":"PS3", 
  #"PS4":"PS4", 
  #"VITA":"Vita", 
  #"PSP":"PSP", 
  "SNES": ['smc','sfc'], 
  "TG16": ['pce'],
  "WS": ['ws'], 
  "WSC": ['wsc'],
  "Indeterminate": ['rom','bin','iso','cas']
}

paren_match = '\((.+?)\)'
paren_del = '^(.+?) ?\(.+?\)$'

# Look for episodes.
def Scan(path, files, mediaList, subdirs, language=None, root=None, **kwargs):

    # Let's try to scan the files. Getting the name is fairly straight forward
    for f in files:
        # We'll split the file name and extension.
        name, ext = os.path.splitext(os.path.basename(f))
        # We need to strip the dot off the front of the extension (if there is one).
        ext = ext[1:]
        # Now we'll check if the extension is our dictionary.
        platform_id = [k for k, v in game_exts_x.iteritems() if ext in v]
        # We need to see if there is a publisher/developer embedded in the filename.
        publisher = re.search(paren_match, name)
        if publisher:
            remove_publisher = re.search(paren_del, name)
            name = remove_publisher.group(1)

        # This could be a rom zipped up, or it could be a random zip file.
        if ext == 'zip':
            # We should actually check inside the zip itself.
            zzz = zipfile.ZipFile(f)
            for z in zzz.namelist():
                zname, zext = os.path.splitext(z)
                zext = zext[1:]
                platform_id = platform_id + [k for k, v in game_exts_x.iteritems() if zext in v]

        # Create the game (movie) object.
        game = Media.Movie(name, None)
        game.parts.append(f)

        # Do we have a platform?
        if platform_id:
            game.source = platform_id[0] 
            # Does the name have an embedded publisher? Some titles were released by several, we'll need to send
            # that to the agent plugin.
            if publisher:
                game.source = game.source + ';' + publisher.group(1)
            mediaList.append(game)
          
    # Let's recurse! 
    for s in subdirs:
        nested_subdirs = []
        nested_files = []
        for z in os.listdir(s):
            if os.path.isdir(os.path.join(s, z)):
                nested_subdirs.append(os.path.join(s, z))
            elif os.path.isfile(os.path.join(s, z)):
                nested_files.append(os.path.join(s, z))
        # This should be safe, since we're not following symlinks or anything that might cause a loop.
        Scan(s, nested_files, mediaList, nested_subdirs, root)

    if files:
        logging.debug("=======================================================\n")
        logging.debug(time.strftime("%c"))
        logging.debug("recvieved following parameters :")
        logging.debug("path parameter      : ")
        logging.debug(str(path))
        logging.debug("files parameter     : ")
        logging.debug(str(files))
        logging.debug("mediaList parameter : ")
        logging.debug(str(mediaList))
        logging.debug("subdirs parameter   : ")
        logging.debug(str(subdirs))
        logging.debug("language parameter  : ")
        logging.debug(str(language))
        logging.debug("root parameter      : ")
        logging.debug(str(root))
        logging.debug("kwargs parameter    : ")
        logging.debug(str(kwargs))
        logging.debug("========================================================\n")
        logging.debug("               START PROCESSING FILES SECTION          \n ")
