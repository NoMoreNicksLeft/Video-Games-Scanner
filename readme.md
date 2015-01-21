Video Games Scanner for Plex
----------------------------------

Nothing fancy, just a plugin for [Plex Media Server](https://plex.tv/).

This scanner allows Plex to scan through a library looking for video game files (usually roms, but also disk images and others) and to add them to its database. It works in conjunction with my other project, the [TheGamesDB Metadata Agent](https://github.com/NoMoreNicksLeft/TheGamesDB.bundle) to give Plex some video games functionality.

This is a work in progress, I need any file extensions that you may know for roms or disk images. Google's not helping too much on that task. I've been trying to disconnect this from the agent plugin for two reasons: the scanner shouldn't make assumptions about which agent plugin will be used, but also because the database my agent plugin uses leaves alot to be desired.

Before this could be ready for the masses, I have to rethink it's entire architecture. Currently it only uses the filename itself (Some Game.zip) for scanning... the file extension lets me make guesses about the plaform, and many roms I've seen include a publisher for disambigutation (Nintendo has two Pac Man titles, one by Namco, the other by Tengen). It recurses down into subdirectories to find them, which means you can arrange the filesystem however you like. This is mostly a good choice, but means that it won't work for arcade games, which can have several different types of files that are all necessary. The roms themselves (always zipped up), but also sample audio files, and CHD disk images. Plex solves this problem for movies by suggesting you put the video files into a directory named after the movie, meaning you can dump subtitle files in the same and it recognizes which movie they belong to (and lately, even extras like "behind the scenes" videos can be dumped in the same folder, if named correctly).

Requests for you, the user:

1. If you know of a rom file extension that's not picked up by the scanner, send me a message. I'll get it included.
2. If you find a game that isn't picked up by the scanner, send me a message. I'll try to debug.
3. If you can make the code better, help me out. This is the first thing I've ever written in Python.