# -*- coding: utf-8 -*-
import random
from conf import settings

def xcaptcha_challenge():
    alphabets = ['A','B','C','D','E','F','G','H','J','K','L','M',
                 'N','P','Q','R','S','T','U','V','W','X','Y','Z']
    characters = random.sample(alphabets,5)
    
    character_coordinates = {}
    for i in range(5):
        m = random.randrange(50)+25
        n = random.randrange(25)+5
        character_coordinates[characters[i]] = str((m+(i*100)+10)*100 + n+50)
    
    
    numbers = ['1','2','3','4','5','6','7','8','9'] 
    print_order = random.sample(numbers,5)
    map_order = random.sample(print_order,5)
    
    mapping = {}
    for i in range(5):
        mapping[characters[i]]=map_order[i]

    text= ''
    for x in characters:
        text += x
        text += '-'
        text += mapping[x]
        text += '-'
        text += character_coordinates[x]
        text += '|'

    answer = ''
    for x in characters:
        answer += mapping[x]
    
    return text[0:len(text)-1], answer
