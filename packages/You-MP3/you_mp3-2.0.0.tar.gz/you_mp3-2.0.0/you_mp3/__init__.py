"""Library for downloading music and adding metadata
The library is an automation and abstraction layer of YoutubeDL
It can be used via the command line with the command \"you-mp3\""""

# Library information

__description__ = "Library for downloading music and adding metadata"

__status__ = "Educational"
__license__ = "Unlicense"
__version__ = "2.0.0"

__author__ = "RuanMiguel-DRD"
__maintainer__ = __author__
__credits__ = __author__

__url__ = "https://github.com/RuanMiguel-DRD/You-MP3"
__email__ = "ruanmigueldrd@outlook.com"

__keywords__ = [
    "conversion", "download", "metadata", "music", "youtube"
]

# Imports

# Defines what will be imported when executing "import you_mp3"

from .downloader import Setting, download_music, extract_playlist
from .metadata import add_metadata, create_cover

# Defines what will be imported when running "from you_mp3 import *"

__all__ = [
    "Setting", "download_music", "extract_playlist",
    "add_metadata", "create_cover"
]
