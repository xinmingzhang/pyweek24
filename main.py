#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import string
import json
from xml.etree import ElementTree
from kivy.uix.floatlayout import FloatLayout
from itertools import cycle
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.core.audio import SoundLoader
from kivy.properties import OptionProperty, StringProperty, ObjectProperty, NumericProperty, BooleanProperty, \
    ListProperty, DictProperty
from kivy.uix.scatter import Scatter

SOUND_LAUGH = SoundLoader.load('laughter.ogg')
SOUND_LAUGH.load()
SOUND_E = SoundLoader.load('Explosion.ogg')
SOUND_E.load()
SOUND_V = SoundLoader.load('victory.ogg')
SOUND_V.load()

BG_MUSIC = {'0' + str(i + 1): SoundLoader.load('0{}.ogg'.format(i + 1)) for i in range(8)}
COLOR_BLACK = (0, 0, 0, 1)
COLOR_DARK_BLUE = (0.2078, 0.8275, 0.4353, 1)
DIALOG_EN = '''
The terrorists were engaged in an orgy of destruction using car bomb around all the world. According to reliable sources, now these rioters have been approaching our territory. Time is urgent, you need to build forts and kill them. Remember, let them completely destroyed.
'''
DIALOG_CH = '''
恐怖分子利用汽车炸弹在世界各地进行恐怖袭击，据线人消息，这帮家伙正在逼近我们的阵地。时间紧迫，赶紧修筑塔防干他们，切记，一个也不能放进来。
'''
FAILURE_EN = '''
OK. All over, big explosion destroied everything here. It is you, you let this happen, you are the person 'behind everything'!
'''

FAILURE_CH = '''
卧槽，炸了，好吧，大爆炸毁灭了一切。你，拜你所赐，你就是那个‘幕后主使’！
'''

VICTORY_EN = '''
OK. you win ! you have protected our homeland! However, did you ever see the nicolas cage film 'Lord of war', still remember that line -- You know who's going to inherit the Earth? Arms dealers. Because everyone else is too busy killing each other.
'''
VICTORY_CH = '''
恭喜，你胜利啦！保家卫国成功了！不过你看过尼古拉斯凯奇的《战争之王》么？是否记得那句台词--你知道谁将主宰地球？军火商。因为其他人都在忙着自相残杀。
'''
TILES = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83,
         83, 8, 19, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 3, 14, 14, 14, 14, 14, 14, 14, 14, 14,
         14, 14, 14, 14, 14, 14, 14, 8, 19, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 3, 14, 14, 14,
         22, 22, 14, 14, 14, 14, 14, 14, 22, 22, 14, 14, 14, 8, 19, 14, 14, 22, 14, 22, 14, 14, 14, 14, 14, 22, 14, 22,
         14, 14, 3, 14, 14, 14, 22, 22, 14, 14, 14, 14, 14, 14, 22, 22, 14, 14, 14, 8, 19, 14, 14, 14, 14, 14, 14, 14,
         14, 14, 14, 14, 14, 14, 14, 14, 3, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 8, 19, 14,
         14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 3, 14, 14, 14, 14, 14, 14, 60, 14, 14, 60, 14, 14, 14,
         14, 14, 14, 8, 19, 14, 14, 14, 14, 14, 14, 60, 14, 60, 14, 14, 14, 14, 14, 14, 3, 14, 14, 14, 14, 14, 14, 14,
         60, 60, 14, 14, 14, 14, 14, 14, 14, 8, 19, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 3, 14,
         14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 8, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62, 62,
         62, 62, 62, 62, 62]

KV = '''

#:import window kivy.core.window.Window

<MyButton>:
    allow_stretch:True

<Blinker>:


<HintLabel>:
    Label:
        center:window.width/2,window.height/2
        text:'wave {}'.format(root.number) if app.language=='EN' else '第 {} 波'.format(root.number)
        font_size:'48sp'
        font_name:'kenvector_future.ttf' if app.language=='EN' else 'STHUPO.TTF'

<Tile>:
    size_hint:None,None
    allow_stretch:True
    keep_ratio:False
    size:window.width/16.0,window.height/12.0
    pos:(self.co_x*self.width-self.width/2,self.co_y*self.height*0.75-self.height/2) \
        if self.co_y%2==0 else (self.co_x*self.width,self.co_y*self.height*0.75-self.height/2)

<TiledMap>:
    do_rotation:False
    scale_min:1.0
    scale_max:2.0
    auto_bring_to_front:False

<TowerButton>:
    opacity:1 if self.touchable else 0.6
    canvas.before:
        Color:
            rgba:self.bg_color
        Ellipse:
            angle_start:0
            angle_end:360
            pos:self.pos
            size:self.size

<Bullet>:

<Bullet1>:
    harm:30
    size_hint:None,None
    size:(window.width/80.0,window.height/60.0)
    source:'flowerRed.png'

<Bullet2>:
    harm:10
    size_hint:None,None
    size:(window.width/80.0,window.height/60.0)
    source:'flowerBlue.png'

<Bullet3>:
    harm:3
    size_hint:None,None
    size:(window.width/80.0,window.height/60.0)
    source:'flowerWhite.png'

<Bullet4>:
    harm:200
    size_hint:None,None
    size:(window.width/80.0,window.height/60.0)
    source:'flowerGreen.png'

<Vehicle>:
    health:1.0
    max_health:1.0
    size_hint:None,None
    size:(window.width/16.0,window.height/12.0)
    canvas.before:
        Color:
            rgba:1,0,0,1
        Rectangle:
            pos:(self.pos[0],self.top)
            size:(self.size[0],2)
    canvas:
        Color:
            rgba:(0,1,0,1) if self.state == 'normal' else (0,1,1,1)
        Rectangle:
            pos:(self.pos[0],self.top)
            size:((self.health/self.max_health)*self.size[0],2)

<Ambulance>:
    speed:0.8
    value:200
    source:'ambulance_{}.png'.format(self.direction)
    health:200.0
    max_health:200.0

<Police>:
    speed:0.5
    source:'police_{}.png'.format(self.direction)
    health:10000.0
    max_health:10000.0

<Garbage>:
    speed:1
    value:200
    source:'garbage_{}.png'.format(self.direction)
    health:500.0
    max_health:500.0

<CarSilver>:
    speed:1
    value:100
    source:'carSilver_{}.png'.format(self.direction)
    health:100.0
    max_health:100.0

<CarGreen>:
    speed:0.8
    value:100
    source:'carGreen_{}.png'.format(self.direction)
    health:120.0
    max_health:120.0

<CarRed>:
    speed:1
    value:100
    source:'carRed_{}.png'.format(self.direction)
    health:110.0
    max_health:110.0

<CarBlack>:
    speed:0.8
    value:100
    source:'carBlack_{}.png'.format(self.direction)
    health:130.0
    max_health:130.0

<CarBlue>:
    speed:1
    value:100
    source:'carBlue_{}.png'.format(self.direction)
    health:100.0
    max_health:100.0

<Taxi>:
    speed:0.5
    source:'taxi_{}.png'.format(self.direction)
    value:100
    health:200.0
    max_health:200.0

<Building>:
    opacity: 1 if self.state == 'fixed' else 0.8
    size_hint:None,None
    size:(window.width/16.0,window.height/12.0)
    canvas.before:
        Color:
            rgba:self.shade_value
        Ellipse:
            angle_start:0
            angle_end:360
            pos:(self.x+self.size[0]/4.0,self.y)
            size:(self.size[0]/2.0,self.size[1]/2.0)

<Tower1>:
    frequency:1
    value:300
    source:'watertower.png'
<Tower2>:
    frequency:2
    value:500
    source:'tower.png'
<Tower3>:
    frequency:1
    value:800
    source:'skyscraper_wide.png'
<Tower4>:
    frequency:2
    value:1000
    source:'windmill_base.png'
<Tower5>:
    frequency:1/60.0
    value:1200
    source:'scifi_scraper2.png'
<Tower6>:
    frequency:2
    value:1500
    source:'skyscraper_glass.png'


<TowerButton1>:
    cost:300
    source:'watertower.png'

<TowerButton2>:
    cost:500
    source:'tower.png'

<TowerButton3>:
    cost:800
    source:'skyscraper_wide.png'

<TowerButton4>:
    cost:1000
    source:'windmill_base.png'

<TowerButton5>:
    cost:1200
    source:'scifi_scraper2.png'

<TowerButton6>:
    cost:1500
    source:'skyscraper_glass.png'

<GamePanel>:



<Splash>:
    name:'splash'

<Title>:
    name:'title'
    id:title
    canvas:
        Color:
            rgba:1,1,1,1
        Rectangle:
            size:self.size
            pos:self.pos
    TitleSettingPanel:
        size_hint:0.3,0.1
        y:title.y
    Widget:
        canvas:
            Color:
                rgba:1,0,0,1
            Ellipse:
                angle_start: 0
                angle_end: 360
                pos: window.width/2-window.height/4,window.height*3/8
                size: window.height/2,window.height/2
    Widget:
        canvas:
            Color:
                rgba:1,1,1,1
            Rectangle:
                pos: window.width*3/8,window.height*9/16
                size: window.width/4,window.height/8

    MyButton:
        source:'pyweek-new.png'
        size_hint:(0.15,0.15)
        pos_hint:{'center':(0.1,0.9)}
    Label:
        size_hint:(None,None)
        pos_hint:{'center_x': 0.5,'center_y':0.2}
        color:(0,0,0,1)
        text: '  No Entry' if app.language=='EN' else '禁止入内'
        font_size:'48sp'
        font_name:'kenvector_future.ttf' if app.language=='EN' else 'STHUPO.TTF'
    Blinker:
        size_hint:(None,None)
        pos_hint:{'center_x': 0.5,'center_y':0.1}
        color:(0,0,0,1)
        text: 'Tap to start game' if app.language=='EN' else '轻触屏幕开始游戏'
        font_size:'21sp'
        font_name:'kenvector_future.ttf' if app.language=='EN' else 'STHUPO.TTF'

<TitleSettingPanel@BoxLayout>:
    id:tsp
    MyButton:
        id:language_setting
        source:'Light10.png'
        on_press:app.switch_language()
        Label:
            color:(0.22,0.22,0.22,1)
            text: 'EN' if app.language=='EN' else '中'
            font_size:'14sp' if app.language=='EN' else '21sp'
            font_name:'kenvector_future.ttf' if app.language=='EN' else 'STHUPO.TTF'
            center:language_setting.center
    MyButton:
        source:'Light15.png'
        on_press:app.switch_music()
    MyButton:
        source:'Light11.png' if app.bg_music.state == 'play' else 'Light13.png'
        on_press:app.switch_music_status()
    MyButton:
        source:'Light16.png'
        on_press:app.root.current = 'thanks'


<Game>:
    name:'game'
    id:game
    panel:panel
    tile_map:tile_map
    TiledMap:
        id:tile_map
        game:game
        size:(window.width,window.height/10.0*8)
    GamePanel:
        id:panel
        size_hint:None,None
        size:window.width,window.height/12.0
        top:window.height
        canvas.before:
            Color:
                rgb:170/255.0,207/255.0,82/255.0
            Rectangle:
                pos:self.pos
                size:self.size
        Label:
            text:'$' + str(game.money)
            size_hint:0.3,0.8
            pos_hint:{'x':0.1,'y':0.1}
            font_size:'14sp'
            font_name:'kenvector_future.ttf'
        BoxLayout:
            size_hint:0.5,0.8
            pos_hint:{'right':0.98,'y':0.1}
            TowerButton1:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton2:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton3:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton4:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton5:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton6:
                game:game
                touchable:True if self.game.money>self.cost else False

<Subtitles>:

<Dialog>:
    name:'dialog'
    video:video
    subtitles:subtitles
    Video:
        id:video
        source:'carbomb.mkv'
    Subtitles:
        id:subtitles
        size_hint:None,None
        size:window.width,self.texture_size[1]
        text_size: window.width*19/20.0, None
        color:0.8,0.8,0.8,1
        font_size:'14sp' if app.language == 'EN' else '21sp'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        pos:window.width/20.0,window.height/10.0
    Blinker:
        size_hint:(None,None)
        pos_hint:{'center_x': 0.9,'center_y':0.05}
        color:(0.5,0.5,0.5,1)
        text: '>>>'
        font_size:'21sp'


<Failure>:
    name:'failure'
    subtitles:subtitles
    Subtitles:
        id:subtitles
        size_hint:None,None
        size:window.width,self.texture_size[1]
        text_size:window.width*3/4.0, None
        center:window.width/2.0, window.height/2.0
        color:0.8,0.8,0.8,1
        font_size:'21sp'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'

    Blinker:
        size_hint:(None,None)
        pos_hint:{'center_x': 0.9,'center_y':0.05}
        color:(0.5,0.5,0.5,1)
        text: 'play again?' if app.language == 'EN' else '重新游戏？'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'


<Victory>:
    name:'victory'
    subtitles:subtitles
    Subtitles:
        id:subtitles
        size_hint:None,None
        size:window.width,self.texture_size[1]
        text_size:window.width*3/4.0, None
        center:window.width/2.0, window.height/2.0
        color:0.8,0.8,0.8,1
        font_size:'21sp'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'

    Blinker:
        size_hint:(None,None)
        pos_hint:{'center_x': 0.9,'center_y':0.05}
        color:(0.5,0.5,0.5,1)
        text: 'play again?' if app.language == 'EN' else '重新游戏？'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'

<THX>:
    name:'thanks'
    canvas:
        Color:
            rgba:1,1,1,1
        Rectangle:
            size:self.size
            pos:self.pos
    Label:
        size_hint:None,None
        size:window.width,self.texture_size[1]
        text_size:window.width*3/4.0, None
        center:window.width/2.0, window.height/10.0
        color:0.22,0.22,0.22,1
        font_size:'14sp' if app.language == 'EN' else '21sp'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        text1:
            """
            Thanks for playing my game, hope you would enjoy it!

            Cheers!

            Surreptitiously,if you crazy tap the screen in game, you will get extra money :)

            Special thanks to /u/terminak, thank you as always :)

            Except my son's laughter, other resources are from web, video is from reddit,
            others are from Opengameart, images are from Kenney, music and sound from Level 27, bart.
            Licenses are CC0 and CC-BY 3.0,I do not know it in detail, just know it is OK :)
            """
        text2:
            """
            多谢赏光，希望还不至于太烂！
            祝贺！
            据说啊，不停的戳屏幕会有额外奖励 ^v^
            特别感谢 terminak，一如既往对我的帮助 ^v^
            除了我儿子的笑声，其它资源从网上下的，视频是reddit
            其他的在Opengameart，图片作者Kenny，音乐音效作者Level 27 和 bart
            版权协议是CC0和CC-BY 3.0 版权啥的我实在不懂，反正只知道可以用^v^
            """
        text:self.text1 if app.language == 'EN' else self.text2
    Blinker:
        size_hint:(None,None)
        pos_hint:{'center_x': 0.1,'center_y':0.05}
        color:(0.5,0.5,0.5,1)
        text: '<<<'
        font_size:'21sp'

<Help>:
    name:'help'
    id:game
    money:800
    panel:panel
    tile_map:tile_map
    TiledMap:
        id:tile_map
        game:game
        opacity:0.5
        size:(window.width,window.height/10.0*8)
    GamePanel:
        id:panel
        size_hint:None,None
        size:window.width,window.height/12.0
        top:window.height
        canvas.before:
            Color:
                rgb:170/255.0,207/255.0,82/255.0
            Rectangle:
                pos:self.pos
                size:self.size
        Label:
            text:'$' + str(game.money)
            size_hint:0.3,0.8
            pos_hint:{'x':0.1,'y':0.1}
            font_size:'14sp'
            font_name:'kenvector_future.ttf'
        BoxLayout:
            size_hint:0.5,0.8
            pos_hint:{'right':0.98,'y':0.1}
            TowerButton1:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton2:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton3:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton4:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton5:
                game:game
                touchable:True if self.game.money>self.cost else False
            TowerButton6:
                game:game
                touchable:True if self.game.money>self.cost else False
    Image:
        source:'tap.png'
        size_hint:0.3,0.3
        pos_hint:{'right':0.68,'y':0.78}
    Label:
        size_hint:0.3,0.3
        pos_hint:{'right':0.8,'y':0.7}
        text:'drag to build the tower' if app.language == 'EN' else '点击拖放建塔'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'carBlack_E.png'
        pos_hint:{'x':0.2,'y':0.2}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'police_E.png'
        pos_hint:{'x':0.2,'y':0.6}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'ambulance_E.png'
        pos_hint:{'x':0.2,'y':0.5}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'garbage_E.png'
        pos_hint:{'x':0.2,'y':0.4}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'taxi_E.png'
        pos_hint:{'x':0.2,'y':0.3}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'watertower.png'
        pos_hint:{'x':0.6,'y':0.1}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'tower.png'
        pos_hint:{'x':0.6,'y':0.2}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'skyscraper_wide.png'
        pos_hint:{'x':0.6,'y':0.3}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'windmill_base.png'
        pos_hint:{'x':0.6,'y':0.4}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'scifi_scraper2.png'
        pos_hint:{'x':0.6,'y':0.5}
    Image:
        size_hint:None,None
        allow_stretch:True
        keep_ratio:True
        size:window.width/16.0,window.height/12.0
        source:'skyscraper_glass.png'
        pos_hint:{'x':0.6,'y':0.6}
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.6,'y':0.6}
        text:'Towers' if app.language == 'EN' else '炮塔'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'21sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.2,'y':0.6}
        text:'Enemies' if app.language == 'EN' else '敌人'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'21sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.25,'y':0.5}
        text:'Destory buildings' if app.language == 'EN' else '摧毁建筑'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.25,'y':0.4}
        text:'Healing vehicles' if app.language == 'EN' else '俗称奶爸'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.25,'y':0.3}
        text:'deliver taxi' if app.language == 'EN' else '借尸还魂'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.25,'y':0.2}
        text:'speed is fast' if app.language == 'EN' else '日行千里'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.25,'y':0.1}
        text:'player bank' if app.language == 'EN' else '给人送钱'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.65,'y':0}
        text:'common attack' if app.language == 'EN' else '普通攻击'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.65,'y':0.1}
        text:'poison attack' if app.language == 'EN' else '减速攻击'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.65,'y':0.2}
        text:'Cleaving Attack' if app.language == 'EN' else '分裂攻击'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.65,'y':0.3}
        text:'Cleaving poison' if app.language == 'EN' else '分裂毒性'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.65,'y':0.4}
        text:'directional attack' if app.language == 'EN' else '定向打击'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Label:
        size_hint:0.3,0.3
        pos_hint:{'x':0.65,'y':0.5}
        text:'critical attack' if app.language == 'EN' else '致命一击'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'
    Blinker:
        size_hint:(None,None)
        pos_hint:{'center_x': 0.8,'center_y':0.05}
        color:(0.5,0.5,0.5,1)
        text: 'start game' if app.language == 'EN' else '进入游戏'
        font_name:'kenvector_future.ttf' if app.language == 'EN' else 'STHUPO.TTF'
        font_size:'14sp'


<StateMachine>:
    Splash:
    Title:
    Dialog:
    Help:
    Game:
    Failure:
    Victory:
    THX:



StateMachine:
    current:'splash'

'''


class MyButton(ButtonBehavior, Image):
    pass


class Blinker(Label):
    direction = OptionProperty('-', options=('-', '+'))

    def __init__(self, **kwargs):
        super(Blinker, self).__init__(**kwargs)
        Clock.schedule_interval(self.blink, 1 / 10.0)

    def blink(self, *args):
        if 0 < self.opacity < 1:
            if self.direction == '-':
                self.opacity -= 0.1
            elif self.direction == '+':
                self.opacity += 0.1
        elif self.opacity <= 0:
            self.opacity += 0.1
            self.direction = '+'
        elif self.opacity >= 1:
            self.opacity -= 0.1
            self.direction = '-'


class HintLabel(Scatter):
    number = NumericProperty(0)

    def __init__(self, number, **kwargs):
        super(HintLabel, self).__init__(**kwargs)
        self.number = number
        Clock.schedule_once(self.rotation_effect, 1)

    def rotation_effect(self, *args):
        if self.parent:
            ani = Animation(scale=5, duration=1)
            ani &= Animation(rotation=360, duration=1)
            ani.bind(on_complete=lambda *a: self.parent.remove_widget(self))
            ani.start(self)


class Subtitles(Label):
    t = StringProperty('')

    def start(self, *args):
        self.t = self.parent.t
        self.letter_index_max = len(self.t)
        self.letter_index = 0
        self.text = self.t[0:self.letter_index]
        self.show_subtitles = Clock.schedule_interval(self.update_subtitles, 1 / 20.0)

    def update_subtitles(self, *args):
        if self.letter_index == self.letter_index_max:
            self.show_subtitles.cancel()
        else:
            self.letter_index += 1
            self.text = self.t[0:self.letter_index]


class Tile(Image):
    # neighbours = ListProperty([])
    state = OptionProperty('empty', options=('empty', 'occupied', 'reserved'))
    co_x = NumericProperty(0)
    co_y = NumericProperty(0)

    def __init__(self, x, y, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.co_x = x
        self.co_y = y

    # def get_neighbours(self):
    #     self.neighbours.append(self.parent.tiles.get((self.co_x - 1, self.co_y)))
    #     self.neighbours.append(self.parent.tiles.get((self.co_x + 1, self.co_y)))
    #     self.neighbours.append(self.parent.tiles.get((self.co_x, self.co_y + 1)))
    #     self.neighbours.append(self.parent.tiles.get((self.co_x, self.co_y - 1)))
    #     if self.co_y % 2 == 1:
    #         self.neighbours.append(self.parent.tiles.get((self.co_x+1, self.co_y - 1)))
    #         self.neighbours.append(self.parent.tiles.get((self.co_x+1, self.co_y + 1)))
    #     elif self.co_y % 2 == 0:
    #         self.neighbours.append(self.parent.tiles.get((self.co_x-1,self.co_y+1)))
    #         self.neighbours.append(self.parent.tiles.get((self.co_x-1, self.co_y-1)))
    #     self.neighbours =[x for x in self.neighbours if x!= None]

    @property
    def neighbours(self):
        n = []
        n.append(self.parent.tiles.get((self.co_x - 1, self.co_y)))
        n.append(self.parent.tiles.get((self.co_x + 1, self.co_y)))
        n.append(self.parent.tiles.get((self.co_x, self.co_y + 1)))
        n.append(self.parent.tiles.get((self.co_x, self.co_y - 1)))
        if self.co_y % 2 == 1:
            n.append(self.parent.tiles.get((self.co_x + 1, self.co_y - 1)))
            n.append(self.parent.tiles.get((self.co_x + 1, self.co_y + 1)))
        elif self.co_y % 2 == 0:
            n.append(self.parent.tiles.get((self.co_x - 1, self.co_y + 1)))
            n.append(self.parent.tiles.get((self.co_x - 1, self.co_y - 1)))
        n = [x for x in n if x != None]
        n = [x for x in n if x.state != 'occupied']
        return n

    def h_distance(self, cls):
        return (cls.x - self.x) ** 2 + (cls.y - self.y) ** 2

        # def on_touch_down(self, touch):
        #     if self.collide_point(*touch.pos):
        #         print(self.co_x, self.co_y)


class TiledMap(Scatter):
    game = ObjectProperty(None)
    tiles = DictProperty({})
    state = OptionProperty('normal', options=('normal', 'explosion'))

    def on_state(self, *args):
        if self.state == 'normal':
            self.on_parent()
        elif self.state == 'explosion':
            self.explosion()

    def on_touch_down(self, touch):
        if touch.is_triple_tap:
            self.game.money += 1000
        else:
            return super(TiledMap, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        super(TiledMap, self).on_touch_move(touch)
        if self.bbox[0][0] > 0 or self.bbox[0][1] > 0:
            self.apply_transform(self.transform_inv)
        elif self.bbox[0][0] + self.bbox[1][0] < Window.size[0] or self.bbox[0][1] + self.bbox[1][1] < Window.size[1]:
            self.apply_transform(self.transform_inv)

    def on_parent(self, *args):
        self.tiles = {}
        tiles = TILES
        # with open('map.json', 'r') as f:
        #     data = json.load(f)
        # tiles = data['layers'][0]['data']
        # tile_data = ElementTree.parse('map.tmx').getroot().find('layer/data').text
        # tiles = map(int, ''.join(line.strip() for line in tile_data.strip()).split(','))
        n_tiles = []
        for i in range(17):
            n_tiles += tiles[17 * (16 - i):17 * (17 - i)]
        for i in range(17):
            for j in range(17):
                k = j * 17 + i
                self.tiles[(i, j)] = Tile(i, j, source='atlas://hexagonTerrain_sheet/{}'.format(n_tiles[k]))
                self.add_widget(self.tiles[(i, j)])
                if j in (0, 15):
                    self.tiles[(i, j)].state = 'occupied'
                elif i == 16 and j % 2 == 0:
                    self.tiles[(i, j)].state = 'reserved'
                elif i == 0 and j % 2 == 0:
                    self.tiles[(i, j)].state = 'reserved'
                elif i == 16 and j % 2 == 1:
                    self.tiles[(i, j)].state = 'empty'
                    # for tile in self.tiles.values():
                    #     tile.get_neighbours()

    def get_path(self, origin, target, *args):
        path = []
        visited = []
        current = self.tiles[origin]
        while not current == self.tiles[target] and len(path) < 150:
            path.append(current)
            visited.append(current)
            neighbours = current.neighbours
            for tile in neighbours:
                if tile in visited:
                    neighbours.remove(tile)
            if len(neighbours) == 0:
                return path
            distances = [tile for tile in neighbours]
            distances.sort(lambda x, y: cmp(x.h_distance(self.tiles[target]), y.h_distance(self.tiles[target])))
            next_tile = distances[0]
            visited.append(next_tile)
            current = next_tile
        path.append(self.tiles[target])
        return path

    def explosion(self, *args):
        SOUND_E.play()
        for i in range(17):
            for j in range(17):
                ani = Animation(pos=(random.randint(0, Window.width), random.randint(0, Window.height)))
                ani &= Animation(opacity=0)
                ani.start(self.tiles[(i, j)])


class TowerButton(Image):
    game = ObjectProperty(None)
    touchable = BooleanProperty(True)
    bg_color = ListProperty([0.5, 1, 0.5, 0.6])


class TowerButton1(TowerButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.touchable:
            self.game.new_building = Tower1(game=self.game, pos=touch.pos, state='unfixed')
            self.game.add_widget(self.game.new_building)
            touch.grab(self.game.new_building)
            return True


class TowerButton2(TowerButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.touchable:
            self.game.new_building = Tower2(game=self.game, pos=touch.pos, state='unfixed')
            self.game.add_widget(self.game.new_building)
            touch.grab(self.game.new_building)
            return True


class TowerButton3(TowerButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.touchable:
            self.game.new_building = Tower3(game=self.game, pos=touch.pos, state='unfixed')
            self.game.add_widget(self.game.new_building)
            touch.grab(self.game.new_building)
            return True


class TowerButton4(TowerButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.touchable:
            self.game.new_building = Tower4(game=self.game, pos=touch.pos, state='unfixed')
            self.game.add_widget(self.game.new_building)
            touch.grab(self.game.new_building)
            return True


class TowerButton5(TowerButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.touchable:
            self.game.new_building = Tower5(game=self.game, pos=touch.pos, state='unfixed')
            self.game.add_widget(self.game.new_building)
            touch.grab(self.game.new_building)
            return True


class TowerButton6(TowerButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.touchable:
            self.game.new_building = Tower6(game=self.game, pos=touch.pos, state='unfixed')
            self.game.add_widget(self.game.new_building)
            touch.grab(self.game.new_building)
            return True


class Building(Image):
    shade_value = ListProperty([0.5, 1.0, 0.5, 1])
    state = OptionProperty('unfixed', options=('unfixed', 'fixed'))
    neighbours = ListProperty([])
    co_x = NumericProperty(0)
    co_y = NumericProperty(0)
    frequency = NumericProperty(1)
    value = NumericProperty(0)

    def __init__(self, game, **kwargs):
        super(Building, self).__init__(**kwargs)
        self.game = game

    def shade(self, *args):
        self.shade_value = [0.5, 0, 0.5, 1]

    def un_shade(self, *args):
        self.shade_value = [0, 0, 0, 0]

    def on_state(self, *args):
        if self.state == 'fixed':
            self.un_shade()
            Clock.schedule_interval(self.shoot_enemy, self.frequency)
        elif self.state == 'unfixed':
            self.shade()

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.check_build()
            return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            for tile in self.game.tile_map.tiles:
                if self.game.tile_map.tiles[tile].collide_point(*touch.pos):
                    self.center = self.game.tile_map.tiles[tile].center

    def check_build(self):
        if self.game.panel.collide_point(*self.center):
            if self.game.new_building:
                self.game.remove_widget(self.game.new_building)
                self.game.new_building = None
        else:
            for tile in self.game.tile_map.tiles:
                if self.game.tile_map.tiles[tile].collide_point(*self.center):
                    if self.game.tile_map.tiles[tile].state == 'empty':
                        self.state = 'fixed'
                        # self.neighbours = self.game.tile_map.tiles[tile].neighbours
                        self.game.remove_widget(self.game.new_building)
                        self.game.tile_map.add_widget(self.game.new_building)
                        self.game.buildings.append(self.game.new_building)
                        self.co_x = self.game.tile_map.tiles[tile].co_x
                        self.co_y = self.game.tile_map.tiles[tile].co_y
                        self.game.new_building = None
                        self.game.tile_map.tiles[tile].state = 'occupied'
                        self.game.money -= self.value
                        return
                    elif self.game.tile_map.tiles[tile].state in ('occupied', 'reserved'):
                        if self.game.new_building:
                            self.game.remove_widget(self.game.new_building)
                            self.game.new_building = None
                            return


class Bullet(Image):
    def __init__(self, game, **kwargs):
        super(Bullet, self).__init__(**kwargs)
        self.game = game
        Clock.schedule_interval(self.check_collision, 1 / 60.0)

    def check_collision(self, *args):
        for enemy in self.game.enemies:
            if self.parent and self.collide_widget(enemy):
                enemy.get_harm(self)
                return

    def kill(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


class Bullet1(Bullet):
    pass


class Bullet2(Bullet):
    def check_collision(self, *args):
        for enemy in self.game.enemies:
            if self.parent and self.collide_widget(enemy):
                enemy.get_harm(self)
                enemy.state = 'toxic'
                return


class Bullet3(Bullet):
    pass


class Bullet4(Bullet):
    def check_collision(self, *args):
        for enemy in self.game.enemies:
            if self.parent and self.collide_widget(enemy):
                enemy.get_harm(self)
                enemy.state = 'toxic'
                return


class Tower1(Building):
    def shoot_enemy(self, *args):
        if self.parent:
            for enemy in self.game.enemies:
                if abs(enemy.co_x - self.co_x) <= 2 and abs(enemy.co_y - self.co_y) <= 2:
                    bullet = Bullet1(self.game)
                    self.game.add_widget(bullet)
                    bullet.center = self.center
                    ani = Animation(pos=enemy.center, d=0.5)
                    ani.bind(on_complete=bullet.kill)
                    ani.start(bullet)
                    return


class Tower2(Building):
    def shoot_enemy(self, *args):
        if self.parent:
            for enemy in self.game.enemies:
                if abs(enemy.co_x - self.co_x) <= 4 and abs(enemy.co_y - self.co_y) <= 4 and enemy.state != 'toxic':
                    bullet = Bullet2(self.game)
                    self.game.add_widget(bullet)
                    bullet.center = self.center
                    ani = Animation(pos=enemy.center)
                    ani.bind(on_complete=bullet.kill)
                    ani.start(bullet)
                    return


class Tower3(Building):
    def shoot_enemy(self, *args):
        if self.parent:
            for enemy in self.game.enemies:
                if abs(enemy.co_x - self.co_x) <= 3 and abs(enemy.co_y - self.co_y) <= 3:
                    bullet = Bullet1(self.game)
                    self.game.add_widget(bullet)
                    bullet.center = self.center
                    ani = Animation(pos=enemy.center)
                    ani.bind(on_complete=bullet.kill)
                    ani.start(bullet)


class Tower4(Building):
    def shoot_enemy(self, *args):
        if self.parent:
            for enemy in self.game.enemies:
                if abs(enemy.co_x - self.co_x) <= 4 and abs(enemy.co_y - self.co_y) <= 4 and enemy.state != 'toxic':
                    bullet = Bullet2(self.game)
                    self.game.add_widget(bullet)
                    bullet.center = self.center
                    ani = Animation(pos=enemy.center)
                    ani.bind(on_complete=bullet.kill)
                    ani.start(bullet)


class Tower5(Building):
    def shoot_enemy(self, *args):
        if self.parent:
            for enemy in self.game.enemies:
                if abs(enemy.co_x - self.co_x) <= 3 and abs(enemy.co_y - self.co_y) <= 3:
                    bullet = Bullet3(self.game)
                    self.game.add_widget(bullet)
                    bullet.center = self.center
                    ani = Animation(pos=enemy.center)
                    ani.bind(on_complete=bullet.kill)
                    ani.start(bullet)
                    return


class Tower6(Building):
    def shoot_enemy(self, *args):
        if self.parent:
            for enemy in self.game.enemies:
                if abs(enemy.co_x - self.co_x) <= 5 and abs(enemy.co_y - self.co_y) <= 5:
                    bullet = Bullet4(self.game)
                    self.game.add_widget(bullet)
                    bullet.center = self.center
                    ani = Animation(pos=enemy.center)
                    ani.bind(on_complete=bullet.kill)
                    ani.start(bullet)
                    return


class GamePanel(FloatLayout):
    pass


class Vehicle(Image):
    health = NumericProperty(0)
    direction = OptionProperty('E', options=('E', 'NE', 'SE', 'W', 'NW', 'SW'))
    co_x = NumericProperty(0)
    co_y = NumericProperty(0)
    state = OptionProperty('normal', options=('normal', 'toxic'))
    speed_a = OptionProperty(1, options=(1, 1.5))
    value = NumericProperty(0)

    def __init__(self, game, co_x, co_y, **kwargs):
        super(Vehicle, self).__init__(**kwargs)
        self.game = game
        self.co_x = co_x
        self.co_y = co_y
        self.path = []

    def on_health(self, *args):
        if self.health <= 0 and self.parent:
            self.parent.remove_widget(self)
            self.game.enemies.remove(self)
            self.game.money += self.value

    def get_harm(self, bullet, *args):
        self.health -= bullet.harm
        bullet.parent.remove_widget(bullet)

    def on_state(self, *args):
        if self.state == 'normal':
            self.speed_a = 1
        elif self.state == 'toxic':
            self.speed_a = 1.5

    def change_direction(self, target):
        delta_co = (target.co_x - self.co_x, target.co_y - self.co_y)
        if delta_co == (1, 0):
            self.direction = 'E'
        elif delta_co == (-1, 0):
            self.direction = 'W'
        elif delta_co == (0, 1):
            if self.co_y % 2 == 0:
                self.direction = 'NE'
            elif self.co_y % 2 == 1:
                self.direction = 'NW'
        elif delta_co == (1, 1):
            self.direction = 'NE'
        elif delta_co == (-1, 1):
            self.direction = 'NW'
        elif delta_co == (0, -1):
            if self.co_y % 2 == 1:
                self.direction = 'SW'
            elif self.co_y % 2 == 0:
                self.direction = 'SE'
        elif delta_co == (-1, -1):
            self.direction = 'SW'
        elif delta_co == (1, -1):
            self.direction = 'SE'
        else:
            # print(delta_co)
            pass

    def update_co_pos(self, target):
        self.co_x = target.co_x
        self.co_y = target.co_y


class CarSilver(Vehicle):
    def on_parent(self, *args):
        if self.parent:
            self.center = self.game.tile_map.tiles[(self.co_x, self.co_y)].center
            p = self.game.tile_map.get_path((self.co_x, self.co_y), (16, self.co_y - 1))
            self.path = p[:]
            self.move()

    def move(self, *args):
        if len(self.path) != 0:
            tile = self.path.pop(0)
            ani = Animation(center=tile.center, d=self.speed * self.speed_a)
            ani.bind(on_start=lambda *args: self.change_direction(tile))
            ani.bind(on_complete=lambda *args: self.move(self))
            ani.bind(on_complete=lambda *args: self.update_co_pos(tile))
            ani.start(self)


class CarGreen(CarSilver):
    def on_parent(self, *args):
        if self.parent:
            self.center = self.game.tile_map.tiles[(self.co_x, self.co_y)].center
            p = self.game.tile_map.get_path((self.co_x, self.co_y), (16, 7))
            self.path = p[:]
            self.move()


class CarRed(CarSilver):
    pass


class CarBlack(CarSilver):
    def on_parent(self, *args):
        if self.parent:
            self.center = self.game.tile_map.tiles[(self.co_x, self.co_y)].center
            p = self.game.tile_map.get_path((self.co_x, self.co_y), (16, 9))
            self.path = p[:]
            self.move()


class CarBlue(CarSilver):
    pass


class Ambulance(Vehicle):
    def on_parent(self, *args):
        if self.parent:
            self.center = self.game.tile_map.tiles[(self.co_x, self.co_y)].center
            p = self.game.tile_map.get_path((self.co_x, self.co_y), (16, 15 - self.co_y))
            self.path = p[:]
            self.move()
            self.check = Clock.schedule_interval(self.check_state, 1 / 60.0)

    def move(self, *args):
        if len(self.path) != 0:
            tile = self.path.pop(0)
            ani = Animation(center=tile.center, d=self.speed * self.speed_a)
            ani.bind(on_start=lambda *args: self.change_direction(tile))
            ani.bind(on_complete=lambda *args: self.move(self))
            ani.bind(on_complete=lambda *args: self.update_co_pos(tile))
            ani.start(self)

    def check_state(self, *args):
        if not self.parent and self.health <= 0:
            for enemy in self.game.enemies:
                if abs(enemy.co_x - self.co_x) <= 3 and abs(enemy.co_y - self.co_y) <= 3:
                    enemy.health = enemy.max_health
                    self.check.cancel()


class Police(Vehicle):
    def on_parent(self, *args):
        if self.parent:
            self.center = self.game.tile_map.tiles[(self.co_x, self.co_y)].center
            p = [self.game.tile_map.tiles[(i, self.co_y)] for i in range(1, 17)]
            self.path = p[:]
            self.move()
            self.check = Clock.schedule_interval(self.check_state, 1 / 60.0)

    def move(self, *args):
        if len(self.path) != 0:
            tile = self.path.pop(0)
            ani = Animation(center=tile.center, d=self.speed * self.speed_a)
            ani.bind(on_start=lambda *args: self.change_direction(tile))
            ani.bind(on_complete=lambda *args: self.move(self))
            ani.bind(on_complete=lambda *args: self.update_co_pos(tile))
            ani.start(self)

    def check_state(self, *args):
        for building in self.game.buildings:
            if self.collide_point(*building.center) and building.parent:
                building.parent.remove_widget(building)
                self.game.tile_map.tiles[(building.co_x, building.co_y)].state = 'empty'
        if self.co_x == 16:
            self.check.cancel()
            self.parent.remove_widget(self)
            self.game.enemies.remove(self)


class Garbage(Vehicle):
    def on_parent(self, *args):
        if self.parent:
            self.center = self.game.tile_map.tiles[(self.co_x, self.co_y)].center
            p = self.game.tile_map.get_path((self.co_x, self.co_y), (16, 15 - self.co_y))
            self.path = p[:]
            self.move()
            self.check = Clock.schedule_interval(self.check_state, 1 / 60.0)

    def move(self, *args):
        if len(self.path) != 0:
            tile = self.path.pop(0)
            ani = Animation(center=tile.center, d=self.speed * self.speed_a)
            ani.bind(on_start=lambda *args: self.change_direction(tile))
            ani.bind(on_complete=lambda *args: self.move(self))
            ani.bind(on_complete=lambda *args: self.update_co_pos(tile))
            ani.start(self)

    def check_state(self, *args):
        if not self.parent and self.health <= 0:
            self.game.add_enemy(Taxi(self.game, self.co_x, self.co_y))
            self.check.cancel()
            return


class Taxi(CarSilver):
    pass


class Splash(Screen):
    def __init__(self, **kwargs):
        super(Splash, self).__init__(**kwargs)
        self.bg_colors = cycle([COLOR_BLACK, COLOR_DARK_BLUE])
        with self.canvas:
            self.bg_color = Color(*COLOR_BLACK)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_rect)

    def on_enter(self, *args):
        SOUND_LAUGH.play()
        Clock.schedule_once(self.burst_pyweek)
        self.effect_1 = Clock.schedule_interval(self.burst, 1 / 60.0)
        self.effect_2 = Clock.schedule_interval(self.blink, 1 / 15.0)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def burst(self, *args):
        l = Label(text=random.choice(string.punctuation + string.ascii_letters + string.digits),
                  font_size=5,
                  color=COLOR_DARK_BLUE,
                  center=(Window.width / 2.0, Window.height / 2.0)
                  )
        ani = Animation(center=(random.uniform(0, Window.width), random.uniform(0, Window.height)), duration=1)
        ani &= Animation(font_size=50)
        ani.bind(on_start=lambda *args: self.add_widget(l))
        ani.bind(on_complete=lambda *args: self.remove_widget(l))
        ani.start(l)

    def blink(self, *args):
        self.bg_color.rgba = next(self.bg_colors)

    def burst_pyweek(self, *args):
        text = 'PyWeek #24'
        label_list = [Label(text=i, font_size=5, color=COLOR_DARK_BLUE,
                            center=(0, 0)) for i in text]
        length = len(text)
        gap = Window.width / 20.0
        ani_list = [None for i in text]
        for i in range(len(text)):
            ani_list[i] = Animation(d=i / 5.0)
            ani_0 = Animation(font_size=50)
            ani_0 &= Animation(center=(Window.width / 2.0 + (i - length // 2) * gap, Window.height / 2.0))
            ani_list[i] += ani_0
            ani_list[i].bind(on_start=lambda *args: self.add_widget(label_list[i]))
        ani_list[-1].bind(on_complete=self.clear_effect)
        for i in range(len(text)):
            ani_list[i].start(label_list[i])

    def show_next_screen(self, *args):
        root = App.get_running_app().root
        root.current = 'title'

    # def on_touch_up(self, touch):
    #     self.on_leave()

    def clear_effect(self, *args):
        SOUND_LAUGH.unload()
        self.effect_1.cancel()
        self.effect_2.cancel()
        self.bg_color.rgba = COLOR_BLACK
        Clock.schedule_once(self.show_next_screen, 1)


class Title(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        app.bg_music.play()

    def on_touch_down(self, touch):
        for child in self.children[:]:
            if child.dispatch('on_touch_down', touch):
                return True
        root = App.get_running_app().root
        root.current = 'dialog'


class Dialog(Screen):
    t = StringProperty('')

    def on_enter(self, *args):
        self.video.play = True

        app = App.get_running_app()
        if app.language == 'EN':
            self.t = DIALOG_EN
        elif app.language == 'CH':
            self.t = DIALOG_CH

        self.subtitles.start()

    def on_touch_down(self, touch):
        if self.subtitles.letter_index != self.subtitles.letter_index_max:
            self.subtitles.show_subtitles.cancel()
            self.subtitles.letter_index = self.subtitles.letter_index_max
            self.subtitles.text = self.subtitles.t
            return True
        else:
            self.video.play = False
            root = App.get_running_app().root
            root.current = 'help'


class Game(Screen):
    tile_map = ObjectProperty(None)
    panel = ObjectProperty(None)
    new_building = ObjectProperty(None, allownone=True)
    money = NumericProperty(1000)
    enemies = ListProperty([])
    buildings = ListProperty([])
    events = ListProperty([])

    def on_enter(self, *args):
        self.tile_map.state = 'normal'
        self.panel.opacity = 1
        self.money = 1000
        append = self.events.append
        append(Clock.schedule_once(self.spawn_1))
        append(Clock.schedule_once(self.spawn_2, 45))
        append(Clock.schedule_once(self.spawn_3, 80))
        append(Clock.schedule_once(self.spawn_4, 110))
        append(Clock.schedule_once(self.spawn_5, 140))
        append(Clock.schedule_once(lambda *args: self.remove_enemies(), 168))
        append(Clock.schedule_once(lambda *args: self.remove_buildings(), 169))
        append(Clock.schedule_once(self.show_victory_screen, 170))
        self.check = Clock.schedule_interval(self.check_falure, 1 / 60.0)

    def on_touch_down(self, touch):

        if self.panel.collide_point(*touch.pos):
            self.panel.on_touch_down(touch)
        else:
            self.tile_map.on_touch_down(touch)

    def spawn_1(self, *args):
        self.add_widget(HintLabel(1))
        append = self.events.append
        for i in range(10):
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarSilver(self, 0, 6)), i * 4 + 3))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlue(self, 0, 8)), i * 4 + 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarRed(self, 0, 10)), i * 4 + 1))

    def spawn_2(self, *args):
        self.add_widget(HintLabel(2))
        append = self.events.append
        for i in range(10):
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlack(self, 0, 4)), i * 3 + 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarSilver(self, 0, 6)), i * 3 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlue(self, 0, 8)), i * 3 + 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarRed(self, 0, 10)), i * 3 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarGreen(self, 0, 12)), i * 3 + 2))

    def spawn_3(self, *args):
        self.add_widget(HintLabel(3))
        append = self.events.append
        for i in range(10):
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlack(self, 0, 2)), i * 2 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlack(self, 0, 4)), i * 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarSilver(self, 0, 6)), i * 2 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlue(self, 0, 8)), i * 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarRed(self, 0, 10)), i * 2 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarGreen(self, 0, 12)), i * 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlack(self, 0, 14)), i * 2 + 1))
        for i in range(2):
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 6)), i * 10))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 8)), i * 10))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 10)), i * 10))

    def spawn_4(self, *args):
        self.add_widget(HintLabel(4))
        append = self.events.append
        for i in range(10):
            append(Clock.schedule_once(lambda *a: self.add_enemy(Taxi(self, 0, 2)), i * 2 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Taxi(self, 0, 4)), i * 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Taxi(self, 0, 6)), i * 2 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Garbage(self, 0, 8)), i * 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Taxi(self, 0, 10)), i * 2 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Taxi(self, 0, 12)), i * 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Taxi(self, 0, 14)), i * 2 + 1))
        for i in range(2):
            append(Clock.schedule_once(lambda *a: self.add_enemy(Ambulance(self, 0, 4)), i * 9))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Garbage(self, 0, 8)), i * 9))

    def spawn_5(self, *args):
        self.add_widget(HintLabel(5))
        append = self.events.append
        for i in range(20):
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlack(self, 0, 2)), i + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlack(self, 0, 4)), i))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarSilver(self, 0, 6)), i + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlue(self, 0, 8)), i))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarRed(self, 0, 10)), i + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarGreen(self, 0, 12)), i))
            append(Clock.schedule_once(lambda *a: self.add_enemy(CarBlack(self, 0, 14)), i + 1))
        for i in range(1):
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 6)), i * 10 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 8)), i * 10 + 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 10)), i * 10 + 3))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 4)), i * 10 + 4))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Police(self, 0, 12)), i * 10 + 5))
        for i in range(4):
            append(Clock.schedule_once(lambda *a: self.add_enemy(Ambulance(self, 0, 4)), i * 4 + 1))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Garbage(self, 0, 6)), i * 4 + 2))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Ambulance(self, 0, 8)), i * 4 + 3))
            append(Clock.schedule_once(lambda *a: self.add_enemy(Garbage(self, 0, 10)), i * 4))

    def add_enemy(self, enemy, *args):
        self.enemies.append(enemy)
        self.tile_map.add_widget(enemy)

    def cancel_events(self, *args):
        for event in self.events:
            event.cancel()

    def check_falure(self, *args):
        for enemy in self.enemies:
            if enemy.co_x == 16 and enemy.co_y % 2 == 1:
                self.check.cancel()
                self.panel_hide()
                self.tile_map.state = 'explosion'
                return

    def remove_enemies(self, *args):
        for enemy in self.enemies:
            if enemy.parent:
                enemy.parent.remove_widget(enemy)
        self.enemies = []

    def remove_buildings(self, *args):
        for building in self.buildings:
            if building.parent:
                building.parent.remove_widget(building)
        self.buildings = []

    def panel_hide(self, *args):
        ani = Animation(opacity=0)
        ani.bind(on_complete=self.remove_enemies)
        ani.bind(on_complete=self.remove_buildings)
        ani.bind(on_complete=self.cancel_events)
        ani.bind(on_complete=self.show_failure_screen)
        ani.start(self.panel)

    def show_failure_screen(self, *args):
        root = App.get_running_app().root
        root.current = 'failure'

    def show_victory_screen(self, *args):
        root = App.get_running_app().root
        root.current = 'victory'


        # def add_enemy(self, *args):
        #     ambulance = Ambulance(self)
        #     self.tile_map.add_widget(ambulance)
        #     self.enemies.append(ambulance)


class Help(Screen):
    def on_touch_down(self, touch):
        root = App.get_running_app().root
        root.current = 'game'


class Failure(Screen):
    t = StringProperty('')

    def on_enter(self, *args):
        app = App.get_running_app()
        if app.language == 'EN':
            self.t = FAILURE_EN
        elif app.language == 'CH':
            self.t = FAILURE_CH
        self.subtitles.start()

    def on_touch_down(self, touch):
        if self.subtitles.letter_index != self.subtitles.letter_index_max:
            self.subtitles.show_subtitles.cancel()
            self.subtitles.letter_index = self.subtitles.letter_index_max
            self.subtitles.text = self.subtitles.t
            return True
        else:
            root = App.get_running_app().root
            root.current = 'help'


class Victory(Screen):
    t = StringProperty('')

    def on_enter(self, *args):
        SOUND_V.play()
        app = App.get_running_app()
        if app.language == 'EN':
            self.t = VICTORY_EN
        elif app.language == 'CH':
            self.t = VICTORY_CH
        self.subtitles.start()

    def on_touch_down(self, touch):
        if self.subtitles.letter_index != self.subtitles.letter_index_max:
            self.subtitles.show_subtitles.cancel()
            self.subtitles.letter_index = self.subtitles.letter_index_max
            self.subtitles.text = self.subtitles.t
            return True
        else:
            root = App.get_running_app().root
            root.current = 'title'


class THX(Screen):
    def on_touch_down(self, touch):
        root = App.get_running_app().root
        root.current = 'title'


class StateMachine(ScreenManager):
    def __init__(self, **kwargs):
        super(StateMachine, self).__init__(transition=WipeTransition(), **kwargs)


class MyGameApp(App):
    language = OptionProperty('EN', options=('EN', 'CH'))
    music_file = OptionProperty('01', options=('01', '02', '03', '04', '05', '06', '07', '08'))
    bg_music = ObjectProperty(None)

    def build(self):
        self.bg_music = BG_MUSIC[self.music_file]
        self.bg_music.loop = True
        return Builder.load_string(KV)

    def switch_language(self, *args):
        if self.language == 'EN':
            self.language = 'CH'
        elif self.language == 'CH':
            self.language = 'EN'
        else:
            pass

    def switch_music(self, *args):
        self.bg_music.stop()
        i = random.choice(MyGameApp.music_file.options)
        self.bg_music = BG_MUSIC[i]
        self.bg_music.play()

    def switch_music_status(self, *args):
        if self.bg_music.state == 'play':
            self.bg_music.stop()
        elif self.bg_music.state == 'stop':
            self.bg_music.play()


if __name__ == '__main__':
    game = MyGameApp()
    game.run()
