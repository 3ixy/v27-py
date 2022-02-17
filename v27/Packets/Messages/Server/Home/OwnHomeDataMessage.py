from Files.CsvLogic.Characters import Characters
from Files.CsvLogic.Skins import Skins
from Files.CsvLogic.Cards import Cards
from datetime import datetime
import random

from Utils.Writer import Writer
from Database.DatabaseManager import DataBase

from Logic.Shop import Shop
from Logic.EventSlots import EventSlots


class OwnHomeDataMessage(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 24101
        self.player = player

    def encode(self):
        DataBase.loadAccount(self)

        self.writeVint(0)
        self.writeVint(int(datetime.timestamp(datetime.now())))  # Timestamp
        
        self.writeVint(self.player.trophies)  # trophies
        self.writeVint(self.player.highest_trophies)

        self.writeVint(0)
        self.writeVint(99)  # reward for trophy road

        self.writeVint(self.player.player_experience)

        self.writeScId(28, self.player.profile_icon)
        self.writeScId(43, self.player.name_color)

        self.writeVint(0)
        
        self.writeVint(len(self.player.brawlers_skins))
        for brawler_id in self.player.brawlers_skins:
            self.writeVint(29)
            self.writeVint(self.player.brawlers_skins[brawler_id])  # skinID

        # Unlocked Skins array
        self.writeVint(len(self.player.skins_id))
        for skin_id in self.player.skins_id:
            self.writeScId(29, skin_id)
            
        self.writeVint(0) # array
        
        self.writeVint(1) # ?
        self.writeVint(1) # ?
        self.writeVint(1) # ?
        
        self.writeBoolean(True) # token limt reached
        self.writeVint(1) # ?
        self.writeBoolean(True) # ?
        
        self.writeVint(self.player.tokensdoubler)
        self.writeVint(6) # season end timer
        self.writeVint(1)
        self.writeVint(1)
        
        self.writeVint(200)
        self.writeVint(5)
        self.writeVint(93)
        
        self.writeVint(206)
        
        self.writeVint(456)
        self.writeVint(1001)
        self.writeVint(2264)
        
        self.writeVint(4)
        self.writeVint(2)
        
        self.writeVint(2)
        self.writeVint(2)
        self.writeVint(1)
        self.writeVint(1)
        count = len(Shop.offers)

        self.writeVint(count)
        for i in range(count):
            item = Shop.offers[i]

            self.writeVint(1)

            self.writeVint(item['ID'])
            self.writeVint(item['Multiplier'])
            self.writeVint(0)
            self.writeVint(item['SkinID'])
            self.writeVint(item['ShopType'])  # [0 = Offer, 2 = Skins 3 = Star Shop]

            self.writeVint(item['Cost'])  # Cost
            self.writeVint(item['Timer'])

            self.writeVint(1)
            self.writeVint(100)
            self.writeBoolean(False)  # is Offer Purchased

            self.writeBoolean(False)
            self.writeVint(item['ShopDisplay'])  # [0 = Normal, 1 = Daily Deals]
            self.writeBoolean(False)
            self.writeVint(0)

            self.writeInt(0)

            self.write_string_reference(item['OfferTitle'])

            self.writeBoolean(False)
            self.writeString()
            self.writeVint(0)
            self.writeBoolean(False)
        self.writeVint(1)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        
        self.writeVint(200)
        self.writeVint(-1)
        self.writeVint(0)
        
        self.writeVint(100008)
        self.writeVint(0)
        
        self.writeScId(16, self.player.brawler_id)
        
        self.writeString("RU")  # location
        self.writeString(self.player.content_creator)
        
        self.writeVint(2) # Animation array (count) 
        self.writeInt(4) # [3 = Tokens, 4 = Trophies, 8 = Star Points, 10 = Power Points]
        self.writeInt(self.player.trophyanimation)
        self.writeInt(3) # [3 = Tokens, 4 = Trophies, 8 = Star Points, 10 = Power Points]
        self.writeInt(self.player.tokenanimation)
        self.writeVint(0) # array
        self.writeVint(1) # season array
        self.writeVint(0)
        
        self.writeVint(self.player.brawl_pass_tokens)  # brawl pass tokens
        self.writeVint(self.player.brawl_pass_tokens)  # premium pass progress
        self.writeVint(self.player.free_pass_level)  # free pass progress
        self.writeVint(self.player.brawl_pass_unlocked)  # premium pass unlocked boolean
        
        self.writeVint(1)
        self.writeVint(0)
         # Brawl Pass End??
        self.writeVint(1) # array
        self.writeVint(0)
        self.writeVint(1)
        
        self.writeVint(0)
        self.writeVint(2020141)
        
        self.writeVint(100)
        self.writeVint(10)

        for item in Shop.boxes:
            self.writeVint(item['Cost'])
            self.writeVint(item['Multiplier'])

        self.writeVint(Shop.token_doubler['Cost'])
        self.writeVint(Shop.token_doubler['Amount'])

        self.writeVint(500)
        self.writeVint(50)
        self.writeVint(999900)
        
        self.writeVint(0)  # array

        self.writeVint(8)  # array

        for i in range(8):
            self.writeVint(i)

        count = len(EventSlots.maps)
        self.writeVint(count)

        for map in EventSlots.maps:

            self.writeVint(EventSlots.maps.index(map) + 1)
            self.writeVint(EventSlots.maps.index(map) + 1)
            self.writeVint(map['Ended'])  # IsActive | 0 = Active, 1 = Disabled
            self.writeVint(EventSlots.Timer)  # Timer

            self.writeVint(0)
            self.writeScId(15, map['ID'])

            self.writeVint(map['Status'])

            self.writeString()
            self.writeVint(0)
            self.writeVint(0)  # Powerplay game played
            self.writeVint(0)  # Powerplay game left maximum

            if map['Modifier'] > 0:
                self.writeBoolean(True)  # Gamemodifier boolean
                self.writeVint(1)  # ModifierID
            else:
                self.writeBoolean(False)

            self.writeVint(0)
            self.writeVint(0)

        self.writeVint(0)  # array
    # Shop array
        self.writeVint(8)
        for i in [20, 35, 75, 140, 290, 480, 800, 1250]:
            self.writeVint(i)

        self.writeVint(8)
        for i in [1, 2, 3, 4, 5, 10, 15, 20]:
            self.writeVint(i)

        self.writeVint(3)
        for i in [10, 30, 80]:  # Tickets price
            self.writeVint(i)

        self.writeVint(3)
        for i in [6, 20, 60]:  # Tickets amount
            self.writeVint(i)

        self.writeVint(len(Shop.gold))
        for item in Shop.gold:
            self.writeVint(item['Cost'])

        self.writeVint(len(Shop.gold))
        for item in Shop.gold:
            self.writeVint(item['Amount'])

        self.writeVint(2)  # array
        self.writeVint(200)  # Max Tokens
        self.writeVint(20)  # Plus Tokens

        self.writeVint(8640)
        self.writeVint(10)
        self.writeVint(5)

        self.writeVint(6)

        self.writeVint(50)
        self.writeVint(604800)

        self.writeBoolean(True)  # Box boolean

        self.writeVint(0)  # array

        self.writeVint(1)  # Menu Theme
        self.writeInt(1)
        self.writeInt(41000000) # Theme ID

        self.writeVint(0)  # array

        self.writeInt(0)
        self.writeInt(self.player.low_id)

        self.writeVint(0)

        self.writeVint(1)

        self.writeBoolean(True)

        self.writeVint(0)
        self.writeVint(0)

        self.writeVint(self.player.high_id)  # High Id
        self.writeVint(self.player.low_id)  # Low Id

        self.writeVint(0)
        self.writeVint(0)

        self.writeVint(0)
        self.writeVint(0)

        if self.player.name == "Guest":
            self.writeString("Guest") # player name
            self.writeVint(0)
            DataBase.createAccount(self) # create new account
        else:
            self.writeString(self.player.name) # player name
            self.writeVint(1)

        self.writeInt(0)
        self.writeVint(8)
 # unlocked brawlers array
        self.writeVint(len(self.player.card_unlock_id) + 4)  # count

        index = 0
        for unlock_id in self.player.card_unlock_id:
            self.writeVint(23)
            self.writeVint(unlock_id)
            try:
                self.writeVint(self.player.BrawlersUnlockedState[str(index)])
            except:
                self.writeVint(1)

            if index == 34:
                index += 3
            elif index == 32:
                index += 2
            else:
                index += 1

        # Array
        self.writeVint(5)  # csv id
        self.writeVint(1)  # resource id
        self.writeVint(self.player.brawl_boxes)  # resource amount

        self.writeVint(5)  # csv id
        self.writeVint(8)  # resource id
        self.writeVint(self.player.gold)  # resource amount

        self.writeVint(5)  # csv id
        self.writeVint(9)  # resource id
        self.writeVint(self.player.big_boxes)  # resource amount

        self.writeVint(5)  # csv id
        self.writeVint(10)  # resource id
        self.writeVint(self.player.star_points)  # resource amount
        
        # Brawlers Trophies array
        self.writeVint(len(self.player.brawlers_id))  # brawlers count

        for brawler_id in self.player.brawlers_id:
            self.writeScId(16, brawler_id)
            self.writeVint(self.player.brawlers_trophies[str(brawler_id)])

        # Brawlers Trophies for Rank array
        self.writeVint(len(self.player.brawlers_id))  # brawlers count

        for brawler_id in self.player.brawlers_id:
            self.writeScId(16, brawler_id)
            self.writeVint(self.player.brawlers_trophies_in_rank[str(brawler_id)])

        self.writeVint(0)  # array

        # Brawlers Upgrade Points array
        self.writeVint(len(self.player.brawlers_id))  # brawlers count

        for brawler_id in self.player.brawlers_id:
            self.writeScId(16, brawler_id)
            self.writeVint(self.player.brawlers_upgradium[str(brawler_id)])

        # Brawlers Power Level array
        self.writeVint(len(self.player.brawlers_id))  # brawlers count

        for brawler_id in self.player.brawlers_id:
            self.writeScId(16, brawler_id)
            self.writeVint(self.player.Brawler_level[str(brawler_id)])

        # Gadgets and Star Powers array
        spgList = []
        for id, level in self.player.Brawler_level.items():
            if level == 8:
                spg = Cards.get_unlocked_spg(self, int(id))
                for i in range(len(spg)):
                    spgList.append(spg[i])
        self.writeVint(len(self.player.card_skills_id))  # count

        for skill_id in self.player.card_skills_id:
            self.writeVint(23)
            self.writeVint(skill_id)
            if skill_id in spgList:
                self.writeVint(1)
            else:
                self.writeVint(0)

        # "new" Brawler Tag array
        self.writeVint(37)
        for x in range(37):
            self.writeScId(16, x)
            self.writeVint(1)
        # Unknown
        self.writeVint(self.player.gems)  # gems
        self.writeVint(self.player.gems) # Fre Gems
        self.writeVint(self.player.player_experience)
        self.writeVint(100)
        self.writeVint(0)
        self.writeVint(1)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(2)
        self.writeVint(1589967120)
        self.writeInt(65535)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(-33)
        self.writeVint(-49)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(2)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeInt(65535)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(-50)
        self.writeVint(9)
        self.writeVint(0)
        self.writeVint(9)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(2)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeInt(65535)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(2)
        print("[INFO] Message RomashkaHomeData has been sent.")