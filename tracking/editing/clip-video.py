
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

ffmpeg_extract_subclip('../videos/adis_karl_1.mp4', 
                       0, 30, 
                       targetname="../videos/adis_karl_1_short.mp4")