from io import BytesIO
from PIL import Image
import os
import random
from time import sleep
from entities.data_scrapper import DataScrapper
from entities.match_data import MatchData


class CreateThumbnail:
    def __init__(self, data_scrapper: DataScrapper, data: MatchData) -> None:
        self.scrapper = data_scrapper
        self.lol_data = data
        self.__thumb_path = os.path.abspath(r'.\media\thumb\thumb.png')

    def create_thumbnail(self):
        print('Creating thumbnail...')
        champion = self.lol_data['mvp']['champion'].replace(
            "'", "").capitalize().replace(
            " ", "")
        # champion = self.lol_data['mvp']['champion']
        print(champion)
        if champion=="KaiSa":
            champion=="Kaisa"
        rank=self.lol_data['mvp']['rank']
        ranks= {
            "Iron": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/1.png",
            "Bronze": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/2.png",
            "Silver": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/3.png",
            "Gold": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/4.png",
            "Platinum": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/5.png",
            "Diamond": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/6.png",
            "Master": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/7.png",
            "GrandMaster": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/8.png",
            "Challenger": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        }
        rankIcon=ranks.get(rank)
        if(rankIcon is None):
            rankIcon="https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        spellImgs=os.listdir("assets/img/spell")
        
        spellImg=random.sample(spellImgs, 3)
        spellImgNew=self.lol_data['mvp']['spell']
        spellImgNew=[s+'.png' for s in spellImgNew]
        spellImg=spellImgNew
        print(spellImg)
        
        loser=self.lol_data['loser']
        self.__create_html(
            kda=self.lol_data['mvp']['kda'].split("/"),
            imgUrl=f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_0.jpg',
            mvp=self.lol_data['mvp']['name'],
            vs=self.lol_data['loser'],
            rank=rank.upper(),
            patch=self.lol_data['patch'],
            rankIcon=rankIcon,
            spellImg=spellImg,
            opponentIcon=f'https://opgg-static.akamaized.net/meta/images/lol/champion/{champion.replace(" ","")}.png'
        )
        html_path = os.path.abspath('assets/thumbnail.html')
        self.scrapper.driver.get('file://' + html_path)
        sleep(10)
        self.scrapper.driver.set_window_size(1280, 805)
        screenshot = self.scrapper.driver.get_screenshot_as_png()
        with Image.open(BytesIO(screenshot)) as img:
            img = img.convert('RGB')
            img.save(self.__thumb_path, quality=70)
        print('Thumbnail created!')
        self.scrapper.driver.quit()

    def __create_html(self, kda: str, mvp: str, vs: str, rank: str, patch: str, imgUrl: str,rankIcon:str,spellImg:list,opponentIcon:str):
        none_vars = []
        if kda is None:
            none_vars.append('kda')
        if mvp is None:
            none_vars.append('mvp')
        if vs is None:
            none_vars.append('vs')
        if rank is None:
            none_vars.append('rank')
        if patch is None:
            none_vars.append('patch')
        if imgUrl is None:
            none_vars.append('imgUrl')
        if rankIcon is None:
            none_vars.append('rankIcon')
        if spellImg is None:
            none_vars.append('spellImg')
        if none_vars:
            print(f"One or more arguments are None: {', '.join(none_vars)}")
            return
        HTML = """<!DOCTYPE html>
<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Nanum Gothic', sans-serif;
        }
        .container {
            background-image: url('"""+imgUrl.replace("'","")+"""');
            background-size: cover;
            width: 1280px;
            height: 720px;
            display: flex;
            align-items: center;
            position: relative; /* Add position relative to container */
        }
        .frame {
            width: 500px;
            height: 650px;
            margin-left: 50px;
            background-color: rgba(0, 0, 0, .6);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            font-weight: 800;
        }
        .kda {
            margin-top: 2rem;
            color: white;
            font-size: 2.5rem;
            display: flex;
            justify-content: center;
            background-color: rgba(0, 0, 0, .5);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            border-radius:50%;
            width:4rem;
            height:4rem;
            align-items: center;
            border: 2px solid white;
            margin: 0px 7px 5px 18px;
        }
        .match {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: white;
        }
        .mvp {
            font-size: 3.5rem; /* set the font size to 10% of the viewport width */
            position: absolute;
            bottom: 150px;
            white-space: nowrap;
        }
        .vs {
            font-size: 2rem;
        }
        .region {
            background-color: aquamarine;
            color: #444;
            padding: .5rem 1.5rem;
            border-radius: 2rem;
            font-size: 2rem;
        }
        .patch {
            color: white;
            font-size: 3rem;
            position: absolute; /* Add position absolute to patch div */
            top: 0; /* Position it at the top */
            right: 0; /* Position it at the right */
            margin: 3rem; /* Add margin to create some space */
            background-color: rgba(0, 0, 0, .4);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            font-weight: bold;
        }
        .kdatext{
            font-size: 3rem;
            padding: .5rem 1.5rem;
            background-color: white;
            color:black;
            width:10rem;
            font-weight: bold;
            border-radius:2rem;
            text-align-last: end;
            align-self: self-end;
        }
        .line {
            border: none;
            border-top: 5px solid white;
            margin: 1rem 2rem;
            padding:2px;
            width:450px;
            color:white;
            position: absolute;
            bottom: 110px;
          }
          .players{
            width:70px;
            height:70px;
            border-radius:50px;
            background-color: rgba(255, 255, 255, .1);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            border: 3px solid white;
          }
          .players1{
            width:167px;
            height:167px;
            border-radius:50%;
            background-color: rgba(255, 255, 255, .1);
            filter: drop-shadow(0px 20px 10px rgba(0, 0, 0, 0.3));
            border: 5px solid white;
          }
          .playerlist{
            position: absolute;
            bottom: 234px;
          }
          .mainplayers{
            position: absolute;
            bottom: 420px;
          }
          .challenger{
            display: flex;
            flex-direction: column;
            align-items: center;
            color: white;
            font-size: 3rem;
            position: absolute;
            bottom: 335px;
            }
            .bottom{
                position: absolute;
                bottom: 31px;
            }
    </style>
</head>
<body>
    <div class="container">
        <div class="frame">
            <div class="mainplayers">
                <img class="players1" src='"""+rankIcon+"""'>
                <img class="players1" src='"""+opponentIcon+"""'/>
            </div>
            <div class="challenger">
                <p>"""+rank+"""</p>
            </div>
            <div class="playerlist">
                <img class="players" src='../assets/img/kr.png'/>
                <img class="players" src='"""+spellImg[0]+"""'/>
                <img class="players" src='../assets/img/spell/"""+spellImg[1]+"""'/>
                <img class="players" src='../assets/img/spell/"""+spellImg[2]+"""'/>
            </div>
            <div class="match">
                <p class="mvp">"""+mvp+"""</p>
            </div>
            <hr class="line"/>
            <div class="bottom" style='display:flex'>
                <p class="kdatext">KDA</p>
                <p >
                    <p class="kda">"""+kda[0]+"""</p>
                    <p class="kda">"""+kda[1]+"""</p>
                    <p class="kda">"""+kda[2]+"""</p>
                </p>
            </div>
        </div>
        <div class="patch">
            <p>"""+patch+"""</p>
        </div>


    </div>
</body>
</html>
"""
        with open("./assets/thumbnail.html", "w",encoding='utf-8') as f:
            f.write(HTML)
