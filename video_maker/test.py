from usecases.data import load
from entities.match_data import MatchData
from entities.data_scrapper import DataScrapper
from usecases.scrap_lol_data import ScrapLolData
from usecases.create_thumbnail import CreateThumbnail
from usecases.record_video import RecordVideo
from usecases.upload_youtube import UploadYoutube
import os

if not os.path.exists("media/replays"):
    os.makedirs("media/replays")
if not os.path.exists("media/thumb"):
    os.makedirs("media/thumb")
if not os.path.exists("media/uploaded"):
    os.makedirs("media/uploaded")
if not os.path.exists("media/Videos"):
    os.makedirs("media/Videos")
if not os.path.exists("media/AllThumbs"):
    os.makedirs("media/AllThumbs")
try:
    lol_data: MatchData = load()
    thumb_creator = CreateThumbnail(data_scrapper=DataScrapper(), data=lol_data)
    result = thumb_creator.create_thumbnail()
    if(not result):
        raise Exception("Server issue")
except Exception as e:
    print(e)
