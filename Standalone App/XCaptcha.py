#!/usr/bin/python2.7

import random, sys
from PyQt4 import QtGui, QtCore
from PIL import Image, ImageFont, ImageDraw, ImageFilter

VERSION = '0.1'

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
    

class captcha():
    
    def __init__(self):
        
        self.mapping = {}
        self.character_coordinates = {}
        self.integer_coordinates = {}
        self.characters = []
        self.font = ImageFont.truetype('font.ttf',40)
            
    def generate_data(self):
        
        #Generating Characters
        alphabets = ['A','B','C','D','E','F','G','H','J','K','L','M',
                     'N','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.characters = random.sample(alphabets,5)
        print 'Domain : ', self.characters
        for i in range(5):
            m = random.randrange(50)+25
            n = random.randrange(25)+5
            self.character_coordinates[self.characters[i]] = (m+(i*100)+10)*100 + n+50 
           
        #Generating Numbers
        numbers = ['1','2','3','4','5','6','7','8','9'] 
        self.print_order = random.sample(numbers,5)
        print 'Range : ', self.print_order
                                    
        #Mapping Characters to Numbers
        self.map_order = random.sample(self.print_order,5)
        for i in range(5):
            self.mapping[self.characters[i]]=self.map_order[i]
        print 'Relation : ', self.mapping
        return self.mapping
        
    def generate_image(self):
        
        image = Image.new('RGB',(500,250),'#000000')
        draw = ImageDraw.Draw(image)
        
        box_flag = [0,0,0,0,0,0,0,0,0,0,0]
        numbers = ['-','-','-','-','-']
        numbers_flag = 0
        pq =[]
        
        for i in range(5):
            if i == 0: 
                j = self.characters[i] 
            elif i == 1:
                j = self.characters[4]
            else :
                j = self.characters[i-1]
            x = self.character_coordinates[j]
            m = x//100
            m = m-5
            n = x % 100
            
            print 'Line ',i,' :'
            
            intermediate_points = random.randrange(2) + 1
            
            print 'Bends :',intermediate_points
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
                print 'Bend : ', possible_box, p2
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
                print 'First bend : ', possible_box, p1
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
                print 'Second bend : ', possible_box, p2
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
            print 'Number position :', possible_box, n
            possible_box = []
            numbers[n] = self.mapping[j]
        
        for i in range(5):
            m = random.randrange(50)+25
            n = random.randrange(25)+180
            self.integer_coordinates[numbers[i]] = (m+(i*100)+10)*100 + n-180
            
        for i in range(5):
            if i == 0: 
                j = self.characters[i] 
            elif i == 1:
                j = self.characters[4]
            else :
                j = self.characters[i-1]
            p = pq[i] // 1000
            q = pq[i] % 1000
            y = self.integer_coordinates[self.mapping[j]]
            r = y // 100
            s = y %100 + 180
            draw.line([(p,q),(r,s)],'#FFFFFF', 3)

        image = image.filter(ImageFilter.BLUR)
        image = image.filter(ImageFilter.SMOOTH_MORE)
        draw = ImageDraw.Draw(image)
        
        for i in range(5):
            j = self.characters[i] 
            x = self.character_coordinates[j]
            m = x//100
            n = x % 100
            y = self.integer_coordinates[self.mapping[j]]
            p = y // 100
            q = y %100 + 180
            draw.text((m-20,n-40),j,'#00C00B', self.font)
            draw.text((p-20,q+10),self.mapping[j],'#00C00B', self.font)
        
        del draw
        img = QtGui.QImage(image.tostring(),500,250,QtGui.QImage.Format_RGB888)
        del image
        return img

class GUI(QtGui.QWidget):
    
    def __init__(self):
    
        super(GUI, self).__init__()
        self.initUI()
    
    def initUI(self):

        self.label1 = QtGui.QLabel(self)

        self.label3 = QtGui.QLabel(self)

        self.label2 = QtGui.QLabel(self)
        self.answer = QtGui.QLineEdit(self)
        
        self.button1 = QtGui.QPushButton("Generate New Image", self)
        self.connect(self.button1,QtCore.SIGNAL('clicked()'),self.NewImage)
        self.button2 = QtGui.QPushButton("Validate", self)
        self.connect(self.button2,QtCore.SIGNAL('clicked()'),self.checkAnswer)
        self.button2.setDefault(1)
        button3 = QtGui.QPushButton('About',self)
        self.connect(button3,QtCore.SIGNAL('clicked()'),self.about)
        
        layout = QtGui.QGridLayout(self)
        layout.setSpacing(10)
        layout.addWidget(self.label1,1,1,1,4)
        layout.addWidget(self.label3,2,1,2,4)
        layout.addWidget(self.label2,4,1,4,4)
        layout.addWidget(self.answer,8,1)
        layout.addWidget(self.button2,8,2)
        layout.addWidget(self.button1,8,3)
        layout.addWidget(button3,8,4)
        self.setLayout(layout)
        self.setWindowTitle('XCaptcha '+VERSION)
        self.NewImage()
    
    def NewImage(self):
        print 'DEBUG INFORMATION'
        img = captcha()
        self.mapping = img.generate_data()
        image = img.generate_image()
        self.label3.setPixmap(QtGui.QPixmap(image))
        self.button2.setEnabled(True)
        text = 'Please type in the corresponding numbers of '
        for i in self.mapping:
            text = text + i + ' '
        text += ' :'
        self.label2.setText(text)
        self.label1.setText('As you see, this image maps characters to numbers.')
        self.button1.setText('Generate New Image')
        
    def checkAnswer(self):
        text = ''
        for i in self.mapping:
            text += self.mapping[i]
        if text == self.answer.text():
            self.label1.setText('<font color="GREEN">That\'s right! Access Granted</font>')
        else:
            self.label1.setText('<font color="RED">That\'s Wrong. Access Denied</font>')
        self.answer.clear()
        self.label2.setText('You may quit this application, or try again.')
        image = QtGui.QImage(Image.new('RGB',(500,250),'#000000').tostring(),500,250,QtGui.QImage.Format_RGB888)
        self.label3.setPixmap(QtGui.QPixmap(image))
        self.button1.setText('Try Again')
        self.button2.setEnabled(False)
    
    def about(self):
        heading = '<center><h3>XCaptcha '+VERSION+'</h3></center>'
        line1 = 'Based on the paper by :'
        dev0 = '<ul><li><a href="mailto:arvind.einstein101@gmail.com">Arvind S.A</a> (S8 PE)</li></ul>'
        line2 = 'Developed by :'
        dev1 = '<a href="mailto:shahanamamutty@gmail.com">Shahana Hamza Mammutty</a> (S6 CSE)'
        dev2 = '<a href="mailto:sruthikampurath@gmail.com">Sruthy K</a> (S6 CSE)'
        dev3 = '<a href="mailto:mulloli@me.com">Varun M</a> (S6 CSE)'
        line3 = '<ul><li>'+dev1+'</li><li>'+dev2+'</li><li>'+dev3+'</li></ul>'
        QtGui.QMessageBox.information(self, "Information",heading+line1+dev0+line2+line3)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())

if __name__=='__main__' :
    main()