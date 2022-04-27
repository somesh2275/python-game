# -*- coding: utf-8 -*-
"""
Author: Somesh Bawane (100339355)

This is a Final Game script file.
"""

import json
import time
import sys
import questionary
from numpy import random

UserDataMemory = []
player_attack = []
computer_attack = []
player_balance = []
computer_balance = []
clan_house = ''

#Setup Game started
def setup_game(UserData):
    global clan_house

    typetext(f"\nWelcome to the adventure { UserData['username'].upper() } \n",0.03)
    
    #if username present then start the game
    typetext("With which Clan House you would like to continue the adventure?",0.03)
    print(">>Dragon House (D)")
    print(">>Witch House (W)")
    print(">>Mixed House (M)")
    clan_house = input("") 
    
    if clan_house == "D":
        house = "Dragon House"
    elif clan_house == "W":
        house = "Witch House"
    elif clan_house == "M":
        house = "Mixed House"
    else:
        typetext("Sorry I didn't understand your choice you are placed in Mixed House",0.02)
        house = "Mixed House"

    typetext(f"\nWelcome to {house}. Now you can customise your town hall",0.03)
    typetext("What's your town hall name?",0.02)
    town_hall = input("")
    typetext(f"\n{town_hall} sounds great.",0.03)
    
    th_color = questionary.select(
    "What is the color of town hall?",
    choices=[
        'Green',
        'Red',
        'Black',
        'White'
    ]).ask() 
    
    th_dimension = questionary.select(
    "What is the dimension of town hall?",
    choices=[
        '100X100',
        '200X200'
    ]).ask() 
    
    th_surrounding = questionary.select(
    "What is the surrounding of town hall?",
    choices=[
        'forest',
        'dessert',
        'mountain'
    ]).ask() 
    
    typetext(f"\nYour town hall is {town_hall} of {th_color} color, {th_dimension} dimension surrounded by {th_surrounding}.",0.03)
    save = questionary.select(
    "Whould you like to save the game progress?",
    choices=[
        'yes',
        'no'
    ]).ask()
    
    if "yes" in save:
        Game_progress = {"username": UserData['username'], "gender" : UserData['gender'], "year" : UserData['year'], "clan_house" : house, "town_hall" : town_hall, "town_hall_color" : th_color, "town_hall_surrounding" : th_surrounding, "town_hall_dimension" : th_dimension}

        filename = UserData['username'].lower() + ".json"

        with open(filename, 'w+') as file:
            file.write(json.dumps(Game_progress))

        file.close()

        typetext("\n Your game progress is saved.",0.03)
        play_game(UserData['username'])
    else:
        typetext("\n Your game progress is not saved.",0.03)
        play_game(UserData['username'])
            
    
def play_game(username):
    typetext("\nGame setup is completed now.",0.02)
    typetext("\nGame Instruction:1) Play will be given 100 points to select maximum 10 troop members",0.02)
    typetext("\n2) You can select from PEKKA 25 points (100HP), Dragon 20 points (75HP), Witch 10 Points (50HP), Wizard 5 points (30HP), Archer 2 points (5HP)",0.02)
    typetext("\n3) After selecting troops you have to choose attack or defense based on coin toss",0.02)
    typetext("\n4) While attacking or defencing select troop member to perform action",0.02)
    typetext("\n5) You can save your progress",0.02)
    
    troop = questionary.select(
        "Select Troop of following troop members",
        choices=[
            '10 Witches',
            '5 Dragons',
            '4 Pekka',
            '2 Pekka, 5 Witches',
            '2 Dragon, 4 Witches, 4 wizards',
            '2 Pekka, 2 Witches, 6 wizards',
            'custom'
        ]).ask()

    pekka = dragon = witch = wizard = archer = 0

    if troop == 'custom':
        pekka = questionary.select(
            "How many Pekka you want in your troop?",
            choices=[
                '0', '1', '2', '3', '4'
            ]).ask()
        pekka_points = calculate_troop(pekka,'Pekka')
        msg = get_message(pekka, pekka_points, 100,10)

        dragon = questionary.select(
            "How many Dragon you want in your troop?",
            choices =[
                '0', '1', '2', '3', '4', '5'
            ]).ask()

        dragon_points = calculate_troop(dragon,'Dragon')
        msg1 = get_message(dragon, dragon_points, msg['points'],msg['troops'])

        if msg['points'] <= 0:
            typetext("Troop selection is completed")
            troopDict = {'Pekka':pekka}
            start_game(troopDict,house)
        else:
            witch = questionary.select(
                "How many Witch you want in your troop?",
                choices =[
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'
                ]).ask()

            witch_points = calculate_troop(witch,'Witch')
            msg2 = get_message(witch, witch_points, msg1['points'], msg1['troops'])

        if msg1['points'] <= 0:
            typetext("Troop selection is completed")
            troopDict = {'Pekka':pekka, 'Dragon': dragon}
            start_game(troopDict,house)
        else:
            wizard = questionary.select(
                "How many Wizard you want in your troop?",
                choices =[
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'
                ]).ask()

            wizard_points = calculate_troop(wizard,'Wizard')
            msg3 = get_message(wizard, wizard_points, msg2['points'],msg2['troops'])

        if msg2['points'] <= 0:
            typetext("Troop selection is completed")
            troopDict = {'Pekka':pekka, 'Dragon': dragon, 'Witch':witch}
            start_game(troopDict,house)
        else:
            archer = questionary.select(
                "How many Archer you want in your troop?",
                choices =[
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'
                ]).ask()

            archer_points = calculate_troop(archer,'Archer')
            msg4 = get_message(archer, archer_points, msg3['points'],msg3['troops'])

        if msg3['points'] <= 0:
            typetext("Troop selection is completed")
            troopDict = {'Pekka':pekka, 'Dragon': dragon, 'Witch':witch, 'Wizard': wizard}
            start_game(troopDict)
        else:
            typetext(f"Selected Troops are {pekka} - PEKKA, {dragon} - Dragon, {witch} - Witch, {wizard} - Wizard, {archer} - Archer",0.02)
            troopDict = {'Pekka':pekka, 'Dragon': dragon, 'Witch':witch, 'Wizard': wizard, 'Archer': archer}
            start_game(troopDict)

    else:
        typetext(f"Selected Troops are {troop}",0.02)
        start_game(troop)


def calculate_troop(troop,member):
    if member == 'Pekka':
        number = int(troop) * int(25)
    elif member == 'Dragon':
        number = int(troop) * int(20)
    elif member == 'Witch':
        number = int(troop) * int(10)
    elif member == 'Wizard':
        number = int(troop) * int(5)
    else:
        number = int(troop) * int(2)

    return number

def get_message(troop,point,max_troop_points, max_troops):
    if max_troop_points >= 0 or max_troops >= 0:
        total_remaining = int(max_troop_points) - int(point)
        total_troops = int(max_troops) - int(troop)

        msg = typetext(f"Remaining points to select {total_troops} troop are {total_remaining}", 0.01)
        total = {"msg": msg, "troops": total_troops, "points": total_remaining}

    else:
        msg =typetext(f"Troops selection is completed. You are out of points or you have selected 10 members", 0.01)
        total = {"msg": msg, "troops": total_troops, "points": total_remaining}

    return total

def toss_time():
    typetext("What is your selection in coin toss Head (H) / Tail (T)",0.04)
    toss = input("")
    if toss == 'H' or toss == 'h' or toss == 'head' or toss == 'Head':
        typetext('You wins the toss choose attack (A) or defense (D)',0.01)
        winner = input("")
    elif toss == 'T' or toss == 't' or toss == 'Tail' or toss == 'tail':
        winner = 0
        typetext('You loss the toss computer choose to attack',0.01)
    else:
        typetext("Kindly choose proper input.",0.01)
        toss_time()

    return winner

def start_game(troop):
    toss = toss_time()
    if toss == 0:
        attack(troop)
    elif toss == "A" or toss == "a":
        attack(troop)
    elif toss == "D" or toss == "d":
        defense(troop)
    else:
        defense(troop)

def selected_clan(house):
    if house == 'D':
        troop = {'Dragon':5}
    elif house == 'W':
        troop = {'Witch':10}
    else:
        troop = {'Pekka':2, 'Dragon':1, 'Witch': 1, 'Wizard': 2, 'Archer': 5}

    return troop

def typetext(text, delay):
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

def attack(troop):
    selected_troop = troop_selection(troop)
    computer_troop = selected_clan(clan_house)
    print(f"Your selected troop are {selected_troop}")
    print(f"Computer's selected troop are {computer_troop}")

    player_attack.insert(0,random.randint(50)) 
    bal = 100 - player_attack[0]
    player_balance.insert(0,bal)
    typetext("You attacked on computer and points left are " + str(player_balance[0]) , 0.005)

    computer_attack.insert(0,random.randint(50))
    bal = 100 - computer_attack[0]
    computer_balance.insert(0,bal)
    typetext("Computer attacked and your points left are " + str(computer_balance[0]), 0.005)
    quest = ask()
    if quest == 0:
        for i in range(1,10):
            j = i - 1
            player_attack.insert(i,random.randint(50))
            bal = player_balance[j] - player_attack[i]
            player_balance.insert(i,bal)
            typetext("You attacked on computer and points left are " + str(player_balance[i]), 0.005)

            computer_attack.insert(i,random.randint(50))
            bal = computer_balance[j] - computer_attack[i]
            computer_balance.insert(i,bal)
            print("computer attacked and your points left are " + str(computer_balance[i]), 0.005)
            
            if player_balance[i] <= 0:
                typetext("Congratulations!! You win the battle.",0.02)
                break
            elif computer_balance[i] <= 0:
                typetext("Hard luck. Computer wins the match.",0.02)
                break
            else:
                quest = ask()
                if quest == 0:
                    typetext("Your attack continues.",0.02)
                    continue
                else:
                    typetext("Hard luck.You withdrawn your troops hence computer wins the match.",0.02)
                    break
    else:
        typetext("Hard luck.You withdrawn your troops hence computer wins the match.",0.02)


def defense(troop):
    selected_troop = troop_selection(troop)
    computer_troop = selected_clan(clan_house)
    print(f"Computer's selected troop are {computer_troop}")
    print(f"Your selected troop are {selected_troop}")
    
    computer_attack.insert(0,random.randint(50))
    bal = 100 - computer_attack[0]
    computer_balance.insert(0,bal)
    typetext("Computer attacked and your points left are " + str(computer_balance[0]),0.005)

    player_attack.insert(0,random.randint(50)) 
    bal = 100 - player_attack[0]
    player_balance.insert(0,bal)
    typetext("You attacked on computer and points left are " + str(player_balance[0]) ,0.005)

    quest = ask()
    if quest == 0:
        for i in range(1,10):
            j = i - 1

            computer_attack.insert(i,random.randint(50))
            bal = computer_balance[j] - computer_attack[i]
            computer_balance.insert(i,bal)
            print("computer attacked and your points left are " + str(computer_balance[i]),0.005)
            
            player_attack.insert(i,random.randint(50))
            bal = player_balance[j] - player_attack[i]
            player_balance.insert(i,bal)
            typetext("You attacked on computer and points left are " + str({player_balance[i]}),0.005)
            
            if computer_balance[i] <= 0:
                typetext("Congratulations!! You win the battle.",0.02)
                break
            elif player_balance[i] <= 0:
                typetext("Hard luck. Computer wins the match.",0.02)
                break
            else:
                quest = ask()
                if quest == 0:
                    typetext("Your attack continues.",0.02)
                    continue
                else:
                    typetext("Hard luck.You withdrawn your troops hence computer wins the match.",0.02)
                    break
    else:
        typetext("Hard luck.You withdrawn your troops hence computer wins the match.",0.02)


def troop_selection(troop):
    if troop == '10 Witches':
        troop = {'Witch':10}
    elif troop == '5 Dragons':
        troop = {'Dragon':5}
    elif troop == '4 Pekka':
        troop = {'Pekka':4}
    elif troop == '2 Pekka, 5 Witches':
        troop = {'Pekka':2, 'Witch': 5}
    elif troop == '2 Dragon, 4 Witches, 4 wizards':
        troop = {'Dragon':2, 'Witch': 4, 'Wizard': 4}
    elif troop == '2 Pekka, 2 Witches, 6 wizards':
        troop = {'Pekka':2, 'Witch': 2, 'Wizard': 6}
    else:
        troop = troop
    
    return troop

#Starting function to ask user weather to sign-in or sign-up
def start():
    typetext("\nWelcome to Clash of Clan text adventure game. Kindly add your details to start enjoying the game",0.03)
    
    typetext("What is your name:",0.04)
    username = input("")
    typetext("Who are you male or female (M/F):",0.04)
    gender = input("")
    typetext("In which year you were born (YYYY):",0.04)
    year = input("")
    
    aDict = {"username":username.lower(), "gender":gender.lower(), "year":year}
    UserDataMemory = aDict

    setup_game(UserDataMemory)

def ask():
    typetext("Do you wish to continue attack Y / N",0.01)
    quest = input("")

    if quest == 'Y' or quest == 'y':
        return 0
    else:
        return 1

start()