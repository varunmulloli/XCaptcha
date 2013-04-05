from cStringIO import StringIO
from models import CaptchaStore
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from conf import settings
import re, random

try:
    import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

def co_ordinate(x1,y1,x2,y2):
    x = random.randrange(x2-x1)+x1
    y = random.randrange(y2-y1)+y1
    return x,y

def XY(p):
    if p == 1:
        return co_ordinate(10,95,90,120)
    elif p == 2:
        return co_ordinate(110,95,190,120)
    elif p == 3:
        return co_ordinate(210,95,290,120)
    elif p == 4:
        return co_ordinate(310,95,390,120)
    elif p == 5:
        return co_ordinate(410,95,490,120)
    elif p == 6:
        return co_ordinate(10,140,90,155)
    elif p == 7:
        return co_ordinate(110,140,190,155)
    elif p == 8:
        return co_ordinate(210,140,290,155)
    elif p == 9:
        return co_ordinate(310,140,390,155)
    elif p == 10:
        return co_ordinate(410,140,490,155)

def generate_image(image,characters,mapping,character_coordinates,font):

    draw = ImageDraw.Draw(image)
    
    box_flag = [0,0,0,0,0,0,0,0,0,0,0]
    numbers = ['-','-','-','-','-']
    numbers_flag = 0
    pq =[]

    for i in range(5):
        if i == 0: 
            j = characters[i] 
        elif i == 1:
            j = characters[4]
        else :
            j = characters[i-1]
        x = character_coordinates[j]
        m = x//100
        m = m-5
        n = x % 100
        
        intermediate_points = random.randrange(2) + 1

        p1, p2 = 0,0
        p1x , p1y = 0,0
        p2x , p2y = 0,0
        possible_box =[]
        
        if intermediate_points == 0:
            pq.append(m*1000 +n)
            if i == 0:
                p2 = 1
            elif i == 1:
                p2 =5
            else:
                p2 = i
        elif intermediate_points == 1:
            if i == 0:
                if box_flag[1] == 0:
                    possible_box.append(1)
                if box_flag[2] == 0:
                    possible_box.append(2)
                if box_flag[7] == 0:
                    possible_box.append(7)
                if box_flag[6] == 0:
                    possible_box.append(6)
            elif i == 1:
                if box_flag[4] == 0:
                    possible_box.append(4)
                if box_flag[5] == 0:
                    possible_box.append(5)
                if box_flag[9] == 0:
                    possible_box.append(9)
                if box_flag[10] == 0:
                    possible_box.append(10)
            else :
                if box_flag[i-1] == 0:
                    possible_box.append(i-1)
                if box_flag[i] == 0:
                    possible_box.append(i)
                if box_flag[i+1] == 0:
                    possible_box.append(i+1)
                if box_flag[i+4] == 0:
                    possible_box.append(i+4)
                if box_flag[i+5] == 0:
                    possible_box.append(i+5)
                if box_flag[i+6] == 0:
                    possible_box.append(i+6)
            
            p2 = random.sample(possible_box,1)
            p2 = p2[0]
            box_flag[p2] = 1
            p1x,p1y = XY(p2)
            draw.line([(m,n),(p1x,p1y)],'#FFFFFF', 3)
            pq.append(p1x*1000+p1y)
        
        elif intermediate_points == 2 :
            if i == 0:
                if box_flag[1] == 0:
                    possible_box.append(1)
                if box_flag[2] == 0:
                    possible_box.append(2)
                if box_flag[7] == 0:
                    possible_box.append(7)
                if box_flag[6] == 0:
                    possible_box.append(6)
            elif i == 1:
                if box_flag[4] == 0:
                    possible_box.append(4)
                if box_flag[5] == 0:
                    possible_box.append(5)
                if box_flag[9] == 0:
                    possible_box.append(9)
                if box_flag[10] == 0:
                    possible_box.append(10)
            elif i == 2 :
                if box_flag[i-1] == 0:
                    possible_box.append(i-1)
                if box_flag[i] == 0:
                    possible_box.append(i)
                if box_flag[i+1] == 0:
                    possible_box.append(i+1)
                if box_flag[i+4] == 0:
                    possible_box.append(i+4)
                if box_flag[i+5] == 0:
                    possible_box.append(i+5)
                if box_flag[i+6] == 0:
                    possible_box.append(i+6)
                if box_flag[1] == box_flag[6] == 0 and possible_box.count(1) == possible_box.count(6) == 1:
                    possible_box.remove(6)
                if box_flag[8] == 0:
                    possible_box.remove(8)
                if box_flag[3] == 0:
                    possible_box.remove(3)
                if box_flag[1] == box_flag[6] == 1:
                    if box_flag[8] == 0:
                        possible_box.append(8)
                    if box_flag[3] == 0:
                        possible_box.append(3)
                    if len(possible_box) == 2 and box_flag[3] == box_flag[8] == 0:
                        possible_box.remove(8)
            elif i == 3:
                for b in range(1,11):
                    if box_flag[b] == 0:
                        possible_box.append(b)
                if box_flag[1] == box_flag[6] == 0 and possible_box.count(1) == possible_box.count(6) == 1:
                    possible_box.remove(6)
                if box_flag[5] == box_flag[10] == 0 and possible_box.count(5) == possible_box.count(10) == 1:
                    possible_box.remove(10)
                if box_flag[8] == 0:
                    possible_box.remove(8)
                if box_flag[3] == 0:
                    possible_box.remove(3)
                if box_flag[1] == box_flag[6] == box_flag[5] == box_flag[10] == 1:
                    if box_flag[8] == 0:
                        possible_box.append(8)
                    if box_flag[3] == 0:
                        possible_box.append(3)
            elif i == 4 :
                if box_flag[i-1] == 0:
                    possible_box.append(i-1)
                if box_flag[i] == 0:
                    possible_box.append(i)
                if box_flag[i+1] == 0:
                    possible_box.append(i+1)
                if box_flag[i+4] == 0:
                    possible_box.append(i+4)
                if box_flag[i+5] == 0:
                    possible_box.append(i+5)
                if box_flag[i+6] == 0:
                    possible_box.append(i+6)
                if box_flag[5] == box_flag[10] == 0 and possible_box.count(5) == possible_box.count(10) == 1:
                    possible_box.remove(10)
                if box_flag[8] == 0:
                    possible_box.remove(8)
                if box_flag[3] == 0:
                    possible_box.remove(3)
                if box_flag[5] == box_flag[10] == 1:
                    if box_flag[8] == 0:
                        possible_box.append(8)
                    if box_flag[3] == 0:
                        possible_box.append(3)
                    if len(possible_box) == 2 and box_flag[3] == box_flag[8] == 0:
                        possible_box.remove(8)
            p1 = random.sample(possible_box,1)
            p1 = p1[0]
            box_flag[p1] = 1
            p1x,p1y = XY(p1)
            draw.line([(m,n),(p1x,p1y)],'#FFFFFF', 3)
            
            possible_box = []
            if p1 == 1:
                if box_flag[6] == 0:
                    possible_box.append(6)
                if box_flag[7] == 0:
                    possible_box.append(7)
                if box_flag[2] == 0:
                    possible_box.append(2)
                if box_flag[2] == box_flag[6] == box_flag[7] == 1:
                    if box_flag[3] == 0:
                        possible_box.append(3)
                    if box_flag[8] == 0:
                        possible_box.append(8)
            elif p1 == 6:
                if box_flag[7] == 0:
                    possible_box.append(7)
                if box_flag[2] == 0:
                    possible_box.append(2)
                if box_flag[7] == box_flag[2] == 1:
                    if box_flag[3] == 0:
                        possible_box.append(3)
                    if box_flag[8] == 0:
                        possible_box.append(8)
            elif p1 == 2:
                if box_flag[1] == box_flag[7] == 1:
                    possible_box.append(6)
                elif box_flag[6] == box_flag[7] == 1:
                    possible_box.append(1)
                else:
                    if box_flag[7] == 0:
                        possible_box.append(7)
                    if box_flag[1] == 0:
                        possible_box.append(1)
                    if box_flag[6] == 0:
                        possible_box.append(6)
            elif p1 == 7:
                if box_flag[1] == box_flag[2] == 1:
                    possible_box.append(6)
                elif box_flag[6] == box_flag[2] == 1:
                    possible_box.append(1)
                else:
                    if box_flag[1] == 0:
                        possible_box.append(1)
                    if box_flag[6] == 0:
                        possible_box.append(6)
                    if box_flag[1] == box_flag[6] == 1:
                        if box_flag[3] == 0:
                            possible_box.append(3)
                        if box_flag[8] == 0:
                            possible_box.append(8)
            elif p1 == 3:
                if box_flag[8] == 0:
                    possible_box.append(8)
                if box_flag[7] == 0:
                    possible_box.append(7)
                if box_flag[2] == 0:
                    possible_box.append(2)
                if box_flag[4] == 0:
                    possible_box.append(4)
                if box_flag[9] == 0:
                    possible_box.append(9)
            elif p1 == 8:
                if box_flag[4] == 0:
                    possible_box.append(4)
                if box_flag[7] == 0:
                    possible_box.append(7)
                if box_flag[2] == 0:
                    possible_box.append(2)
                if box_flag[9] == 0:
                    possible_box.append(9)
            elif p1 == 4:
                if box_flag[5] == box_flag[9] == 1:
                    possible_box.append(10)
                elif box_flag[9] == box_flag[10] == 1:
                    possible_box.append(5)
                else:
                    if box_flag[9] == 0:
                        possible_box.append(9)
                    if box_flag[10] == 0:
                        possible_box.append(10)
                    if box_flag[5] == 0:
                        possible_box.append(5)
            elif p1 == 9:
                if box_flag[4] == box_flag[5] == 1:
                    possible_box.append(10)
                elif box_flag[4] == box_flag[10] == 1:
                    possible_box.append(5)
                else:
                    if box_flag[5] == 0:
                        possible_box.append(5)
                    if box_flag[10] == 0:
                        possible_box.append(10)
                    if box_flag[5] == box_flag[10] == 1:
                        if box_flag[3] == 0:
                            possible_box.append(3)
                        if box_flag[8] == 0:
                            possible_box.append(8)
            if p1 == 5:
                if box_flag[4] == 0:
                    possible_box.append(4)
                if box_flag[9] == 0:
                    possible_box.append(9)
                if box_flag[10] == 0:
                    possible_box.append(10)
                if box_flag[4] == box_flag[9] == box_flag[10] == 1:
                    if box_flag[3] == 0:
                        possible_box.append(3)
                    if box_flag[8] == 0:
                        possible_box.append(8)
            elif p1 == 10:
                if box_flag[4] == 0:
                    possible_box.append(4)
                if box_flag[9] == 0:
                    possible_box.append(9)
                if box_flag[4] == box_flag[9] == 1:
                    if box_flag[3] == 0:
                        possible_box.append(3)
                    if box_flag[8] == 0:
                        possible_box.append(8)
            
            p2 = random.sample(possible_box,1)
            p2 = p2[0]
            box_flag[p2] = 1
            p2x, p2y = XY(p2)
            pq.append(p2x*1000+p2y)
            draw.line([(p1x,p1y),(p2x,p2y)],'#FFFFFF', 3)
        
        possible_box = []
        numbers_flag += 1
        if numbers_flag < 4:
            if p2 == 1 or p2 == 6:
                if numbers[0] == '-':
                    possible_box.append(0)
                if numbers[1] == '-':
                    possible_box.append(1)
            elif p2 == 2 or p2 == 7:
                if numbers[0] == '-':
                    possible_box.append(0)
                if numbers[1] == '-':
                    possible_box.append(1)
                if numbers[2] == '-':
                    possible_box.append(2)
            elif p2 == 3 or p2 == 8:
                if numbers[1] == '-':
                    possible_box.append(1)
                if numbers[2] == '-':
                    possible_box.append(2)
                if numbers[3] == '-':
                    possible_box.append(3)
            elif p2 == 4 or p2 == 9:
                if numbers[2] == '-':
                    possible_box.append(2)
                if numbers[3] == '-':
                    possible_box.append(3)
                if numbers[4] == '-':
                    possible_box.append(4)
            elif p2 == 5 or p2 == 10:
                if numbers[3] == '-':
                    possible_box.append(3)
                if numbers[4] == '-':
                    possible_box.append(4)
        else:
            for b in range(5):
                if numbers[b] == '-':
                    possible_box.append(b)
        n = random.sample(possible_box,1)
        n = n[0]
        possible_box = []
        numbers[n] = mapping[j]
    
    integer_coordinates = {}
    for i in range(5):
        j = characters[i]
        m = random.randrange(50)+25
        n = random.randrange(25)
        integer_coordinates[numbers[i]] = (m+(i*100)+10)*100 + n
    
    for i in range(5):
        if i == 0: 
            j = characters[i] 
        elif i == 1:
            j = characters[4]
        else :
            j = characters[i-1]
        p = pq[i] // 1000
        q = pq[i] % 1000
        y = integer_coordinates[mapping[j]]
        r = y // 100
        s = y %100 + 180
        draw.line([(p,q),(r,s)],'#FFFFFF', 3)
    del draw
    
    image = image.filter(ImageFilter.BLUR)
    image = image.filter(ImageFilter.SMOOTH_MORE)
    draw = ImageDraw.Draw(image)    
    
    for i in range(5):
        j = characters[i] 
        x = character_coordinates[j]
        m = x//100
        n = x % 100
        y = integer_coordinates[mapping[j]]
        p = y // 100
        q = y %100 + 180
        draw.text((m-20,n-40),j,'#00C00B', font)
        draw.text((p-20,q+10),mapping[j],'#00C00B', font)
    
    del draw
    return image




def captcha_image(request,key):
    store = get_object_or_404(CaptchaStore,hashkey=key)
    text = store.challenge
    
    mapping = {}
    character_coordinates = {}
    characters = []
    
    text = text.split('|')
    for i in text:
        a = i.split('-')
        characters.append(a[0])
        mapping[a[0]] = a[1]
        character_coordinates[a[0]] = int(a[2])
    
    font = ImageFont.truetype(settings.CAPTCHA_FONT_PATH,settings.CAPTCHA_FONT_SIZE)
    image = Image.new('RGB', (500,250), settings.CAPTCHA_BACKGROUND_COLOR)
    
    image = generate_image(image,characters,mapping,character_coordinates,font)
    
    out = StringIO()
    image.save(out,"PNG")
    out.seek(0)
    
    response = HttpResponse()
    response['Content-Type'] = 'image/png'
    response.write(out.read())
    
    return response
