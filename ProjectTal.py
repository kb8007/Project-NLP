# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:08:32 2018

@author: kb800
"""
import nltk
import nltk.stem.isri as isri
import xml.etree.ElementTree as Et
import requests
from bs4 import BeautifulSoup
import re
import random
import glob
import urllib.request
import time
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5 import*
from PyQt5.QtWidgets import*
from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])
global result_Quran
global result_Bukhari
global result_periods
result_Quran = []
result_Bukhari = []
result_periods = []

def getContent(file_path,file_encodding):
    if file_path == 'historic_dictionary.xml':
        try:
            d = open(file_path,encoding = file_encodding)
        except:
            creat_historic_dictionary()
            d = open(file_path,encoding = file_encodding)
        content = d.read()
        d.close()
    else:
        d = open(file_path,encoding = file_encodding)
        content = d.read()
        d.close()
    return content

def showPeriodWordRepeat(nb_repeat):
    main_interface.L_period_repeat.setText('عدد التكرارات :  ' + str(nb_repeat))

def getWords(type_word): 
    tree = Et.fromstring(getContent('corpus/قاموس الوسيط.xml','utf-8'))
    words = tree.findall(type_word)
    list_particles = []
    for word in words:
        means = word.findall('mean')
        description = ''
        for mean in means:
            description += str(mean.get('desc'))
            description += '\n'
        list_particles.append((str(word.get('vow')),str(word.get('unv')),description))
    return list_particles

def getHadiths():
    tree = Et.fromstring(getContent('corpus/البخاري.xml','utf-8'))
    books = tree.findall('book')
    list_book_hadith = []
    for book in books:
        hadiths = book.findall('hadith')
        for hadith in hadiths:
            list_book_hadith.append((str(book.get('name')),hadith.get('sectionindex'),str(hadith.get('text'))))
    return list_book_hadith

def showHadiths():
    tree = Et.fromstring(getContent('corpus/البخاري.xml','utf-8'))
    books = tree.findall('book')
    main_interface.T_S_hadith.addItem('')
    hadith_number = 0
    for book in books:
        hadiths = book.findall('hadith')
        for hadith in hadiths:
            hadith_number += 1
            main_interface.T_S_hadith.addItem(str(hadith_number))

def getHadithView():
    tree = Et.fromstring(getContent('corpus/البخاري.xml','utf-8'))
    books = tree.findall('book')
    hadith_number_t = 0
    main_interface.T_S_hadith_content.clear()
    main_interface.T_S_book.setText('اسم الكتاب :   -')
    main_interface.T_S_hadith_number.setText('ترقيم الحديث :  - ')
    if(main_interface.T_S_hadith.currentIndex() != 0):
        for book in books:
            hadiths = book.findall('hadith')
            for hadith in hadiths:
                hadith_number_t += 1
                if(hadith_number_t == main_interface.T_S_hadith.currentIndex()):
                    main_interface.T_S_hadith_content.insertPlainText(str(hadith.get('text')))
                    main_interface.T_S_book.setText('اسم الكتاب :  ' + str(book.get('name')))
                    main_interface.T_S_hadith_number.setText('ترقيم الحديث : ' + hadith.get('sectionindex'))
                    break
            if(hadith_number_t == main_interface.T_S_hadith.currentIndex()):
                break

def showChapters(): 
    tree = Et.fromstring(getContent('corpus/القران الكريم.xml','utf-8'))
    chapters = tree.findall('Chapter')
    main_interface.T_S_surah.addItem('')
    for chapter in chapters:
        main_interface.T_S_surah.addItem(str(chapter.get('ChapterName')))

def getChapters(): 
    tree = Et.fromstring(getContent('corpus/القران الكريم.xml','utf-8'))
    chapters = tree.findall('Chapter')
    list_chapters = []
    main_interface.T_S_surah.addItem('')
    for chapter in chapters:
        list_chapters.append(str(chapter.get('ChapterName')))
    return list_chapters


def getChapterView():
    tree = Et.fromstring(getContent('corpus/القران الكريم.xml','utf-8'))
    chapters = tree.findall('Chapter')
    chapter_content = ''
    main_interface.T_S_surah_content.clear()
    main_interface.T_S_surah_number.setText('رقم السورة :  -')
    main_interface.T_S_ayah_number.setText('عدد الايات :   -')
    if(main_interface.T_S_surah.currentIndex() != 0):
        for chapter in chapters:
            if(str(chapter.get('ChapterID')) == str(main_interface.T_S_surah.currentIndex())):
                verses = chapter.findall('Verse')
                verse_number = 0
                for verse in verses:
                    verse_number += 1
                    chapter_content += verse.text
                    chapter_content += ' |'
                    chapter_content += str(verse.get('VerseID'))
                    chapter_content += '| '
                main_interface.T_S_surah_content.insertPlainText(chapter_content)
                main_interface.T_S_surah_number.setText('رقم السورة :  ' + str(main_interface.T_S_surah.currentIndex()))
                main_interface.T_S_ayah_number.setText('عدد الايات :  ' + str(verse_number))
                break

def getFilesPoeme():
    return [file for file in glob.glob('corpus/الشعر/*.xml')]

def showPeriods():
    list_file_period = getFilesPoeme()
    main_interface.T_S_period.clear()
    main_interface.T_S_elcha3ir.clear()
    main_interface.T_S_kasida.clear()
    main_interface.T_S_poeme_content.clear()
    main_interface.T_S_period.addItem('')
    for file in list_file_period:
        main_interface.T_S_period.addItem(file.replace('corpus/الشعر//','').replace('.xml',''))

def showAutors():
    if(main_interface.T_S_period.currentIndex() != 0):
        main_interface.T_S_elcha3ir.clear()
        main_interface.T_S_kasida.clear()
        main_interface.T_S_poeme_content.clear()
        main_interface.T_S_elcha3ir.addItem('')
        tree = Et.fromstring(getContent(getFilesPoeme()[main_interface.T_S_period.currentIndex() - 1],'utf-8'))
        L_kasida = tree.findall('kasida')
        for kasida in L_kasida:
            if(main_interface.T_S_elcha3ir.findText(str(kasida.get('elcha3ir'))) == -1):
                main_interface.T_S_elcha3ir.addItem(str(kasida.get('elcha3ir')))

def showKasidas():
    if(main_interface.T_S_elcha3ir.currentIndex() != 0):
        main_interface.T_S_kasida.clear()
        main_interface.T_S_poeme_content.clear()
        main_interface.T_S_kasida.addItem('')
        tree = Et.fromstring(getContent(getFilesPoeme()[main_interface.T_S_period.currentIndex() - 1],'utf-8'))
        L_kasida = tree.findall('kasida')
        for kasida in L_kasida:
            if(str(kasida.get('elcha3ir')) == main_interface.T_S_elcha3ir.currentText()):
                main_interface.T_S_kasida.addItem(str(kasida.get('name')))

def showKasida():
    if(main_interface.T_S_kasida.currentIndex() != 0):
        main_interface.T_S_poeme_content.clear()
        tree = Et.fromstring(getContent(getFilesPoeme()[main_interface.T_S_period.currentIndex() - 1],'utf-8'))
        L_kasida = tree.findall('kasida')
        for kasida in L_kasida:
            if((kasida.get('elcha3ir') == main_interface.T_S_elcha3ir.currentText()) and (kasida.get('name') == main_interface.T_S_kasida.currentText())):
                main_interface.T_S_poeme_content.insertPlainText(kasida.text)
                break

def getChapterProcess(ChapterID):
    tree = Et.fromstring(getContent('corpus/القران الكريم.xml','utf-8'))
    chapters = tree.findall('Chapter')
    chapter_content = []
    for chapter in chapters:
        if(str(chapter.get('ChapterID')) == str(ChapterID)):
            verses = chapter.findall('Verse')
            for verse in verses:
                chapter_content.append(verse.text)
    return chapter_content

def getWord():
    return main_interface.TF_search.text()

def getStemm(word):
    stemmer_arabic = isri.ISRIStemmer() 
    tokens= nltk.word_tokenize(word)
    tokens_normaliser=[stemmer_arabic.norm(w) for w in tokens] 
    tokens_stemming =[stemmer_arabic.stem(w) for w in tokens_normaliser]
    return tokens_stemming
   
def switchResult():
    global result_Quran
    global result_Bukhari
    global result_periods
    main_interface.TA_result.clear()
    index = main_interface.C_period.currentIndex()
    if(index == 0):
        print('Quran : ',len(result_Quran),'\n')
        showPeriodWordRepeat(len(result_Quran))
        if(len(result_Quran) == 0):
            main_interface.TA_result.insertPlainText('لم تذكر هاته الكلمة في ' + main_interface.C_period.currentText())
        for result_str in result_Quran:
            main_interface.TA_result.insertPlainText(result_str)
    if(index == 1):
        print('Bukhari : ',len(result_Bukhari),'\n')
        showPeriodWordRepeat(len(result_Bukhari))
        if(len(result_Bukhari) == 0):
            main_interface.TA_result.insertPlainText('لم تذكر هاته الكلمة في ' + main_interface.C_period.currentText())
        for result_str in result_Bukhari:
            main_interface.TA_result.insertPlainText(result_str)
    if(index > 1):
        print('switch all : ',len(result_periods),'\n')
        period = result_periods[index-2]
        showPeriodWordRepeat(len(period))
        if(len(period) == 0):
            main_interface.TA_result.insertPlainText('لم تذكر هاته الكلمة في ' + main_interface.C_period.currentText())
        for result_str in period:
            main_interface.TA_result.insertPlainText(result_str)

def setResult():
    main_interface.RB_auto.setAutoExclusive(False)
    main_interface.RB_auto.setChecked(False)
    main_interface.RB_auto.setAutoExclusive(True)
    main_interface.RB_man.setAutoExclusive(False)
    main_interface.RB_man.setChecked(False)
    main_interface.RB_man.setAutoExclusive(True)
    main_interface.TA_result.clear()
    stem_word_search = getStemm(getWord())
    chapters = getChapters()
    items = ['القران الكريم','كتاب البخاري']
    list_period = getFilesPoeme()
    for period in list_period:
        items.append(period.replace('corpus/الشعر','').replace('.xml',''))
    main_interface.C_period.clear()
    main_interface.C_period.addItems(items)
    main_interface.C_period.setEnabled(True)
    global result_Quran
    global result_Bukhari
    global result_periods
    result_Quran = []
    result_Bukhari = []
    result_periods = []
    for i in range(1,115):
        numVerse = 0
        for verse in getChapterProcess(i):
            numVerse += 1
            for word in verse.split(' '):
                if getStemm(word) == stem_word_search:
                    result_str = ''
                    result_str += '\n\n'
                    result_str += word +'\n'
                    result_str += '--------------------------------------------------\n'
                    result_str += verse + '[' + chapters[i-1] + ' - ' + str(numVerse) + ']' +'\n'
                    main_interface.TA_result.insertPlainText(result_str)
                    result_Quran.append(result_str)
    showPeriodWordRepeat(len(result_Quran))
    if(len(result_Quran) == 0):
        main_interface.TA_result.insertPlainText('لم تذكر هاته الكلمة في ' + main_interface.C_period.currentText())
        
    print('Quran 11: ',len(result_Quran),'\n')
    L_book_hadith = getHadiths()
    for book_hadith in L_book_hadith:
        hadith_words = book_hadith[2].split(' ')
        for hadith_word in hadith_words:
            if getStemm(hadith_word) == stem_word_search:
                result_str = ''
                result_str +='\n\n'
                result_str += hadith_word + '\n'
                result_str += '--------------------------------------------------\n'
                result_str += book_hadith[2] + '[' + book_hadith[0] + ' - ' + str(book_hadith[1]) + ']' +'\n'
                result_Bukhari.append(result_str)
                break
    print('Bukhari 11: ',len(result_Bukhari),'\n')
    
    for file in list_period:
        result_period = []
        tree = Et.fromstring(getContent(file,'utf-8'))
        L_kasida = tree.findall('kasida')
        for kasida in L_kasida:
            lines_kasida = kasida.text.split('\n')
            for line_kasida in lines_kasida:
                words_kasida = line_kasida.split(' ')
                for word_kasida in words_kasida:
                    if getStemm(word_kasida) == stem_word_search:
                        result_str = ''
                        result_str +='\n\n'
                        result_str += word_kasida + '\n'
                        result_str += '--------------------------------------------------\n'
                        result_str += line_kasida + '\n' + '[' + kasida.get('elcha3ir') + '  -  ' + kasida.get('name') + ']' +'\n'
                        result_period.append(result_str)
        result_periods.append(result_period)
        print('one  : ' , len(result_period),'\n')
        print('all  : ' , len(result_periods),'\n')
                    

def showAutoInteface():
    if main_interface.RB_auto.isChecked():
        autodefinition.show()

def showManInteface():
    if main_interface.RB_man.isChecked():
        mandefinition.show()

def uncheckedAutoMan():
    main_interface.RB_auto.setAutoExclusive(False)
    main_interface.RB_auto.setChecked(False)
    main_interface.RB_auto.setAutoExclusive(True)
    main_interface.RB_man.setAutoExclusive(False)
    main_interface.RB_man.setChecked(False)
    main_interface.RB_man.setAutoExclusive(True)

def initAutoDefinition():
    autodefinition.RB_local.setAutoExclusive(False)
    autodefinition.RB_local.setChecked(False)
    autodefinition.RB_local.setAutoExclusive(True)
    autodefinition.RB_notlocal.setAutoExclusive(False)
    autodefinition.RB_notlocal.setChecked(False)
    autodefinition.RB_notlocal.setAutoExclusive(True)
    autodefinition.TA_result.clear()

def hideAutoInterface():
    autodefinition.hide()
    initAutoDefinition()
    uncheckedAutoMan()

def iniManDefinition():
    mandefinition.TA_definition.clear()

def hideManInterface():
    mandefinition.hide()
    iniManDefinition()
    uncheckedAutoMan()

def getLocalDefinition(type_word):
    stemmer_arabic = isri.ISRIStemmer() 
    word_normaliser = stemmer_arabic.norm(getWord())
    print(word_normaliser)
    words_desc_ArDict = getWords(type_word)
    for word_desc_ArDict in words_desc_ArDict:
        print(word_desc_ArDict[1],'\n')
        if word_desc_ArDict[1] == word_normaliser:
            autodefinition.TA_result.insertPlainText(word_desc_ArDict[2]+'\n\n')

def localAutoDefinition():
    if autodefinition.RB_local.isChecked():
        autodefinition.TA_result.clear()
        getLocalDefinition('particle')
        getLocalDefinition('verb')
        getLocalDefinition('noun')

def just_arabic(str):
    return re.sub(r'[a-zA-Z?]||[0-9]||[\\<>/!;,;]', '',str)

def arabic_traduction(arabic_word,dict_name):
    try:
        traduction=""
        traduction_list=[]
        url= 'https://www.almaany.com/ar/dict/ar-ar/'+str(arabic_word)+'/'+str(dict_name)
        source_code=None
        source_code=requests.get(url,'UTF-8')
        soup=BeautifulSoup(source_code.text,'lxml')
        traduction_list=soup.find(class_ ="panel-body").find('ul').find_all('li')
        for word in traduction_list:
            traduction+="\n"+str(word.text)
    
        return just_arabic(traduction)
    except: 
        QMessageBox.about(autodefinition,'مشكلة','تحقق من وجود اتصال')
        
def WebAutoDefinition():
    if autodefinition.RB_notlocal.isChecked():
        autodefinition.TA_result.clear()
        stemmer_arabic = isri.ISRIStemmer() 
        word_normaliser = stemmer_arabic.norm(getWord())
        autodefinition.TA_result.insertPlainText(arabic_traduction(word_normaliser,''))

def word_existence(word)->bool:
    word = word.replace(" ","")
    try:
        word = "word= '" + word
        f = open("historic_dictionary.xml",encoding="utf-8")
        temp = f.read()
        f.close()
        if word in temp:
            return True
        return False
    except:
        return False

def creat_historic_dictionary():
    f=open("historic_dictionary.xml","w+")
    f.write('<?xml version="1.0" encoding="utf-8"?>'+"\n")
    f.write("<Historic_Dictionary>"+"\n")
    f.write(" </Historic_Dictionary>"+"\n")
    f.close()

def add_to_historic_dictionary(word,definition,validation):
    word=word.replace(" ","")
    validation=validation.replace(" ","")
    try:
        f=open("historic_dictionary.xml",encoding="utf-8")
    except:
        creat_historic_dictionary()
        f=open("historic_dictionary.xml",encoding="utf-8")
    temp=f.read()
    f.close()
    f=open("historic_dictionary.xml","w+",encoding='utf-8')
    temp=temp.replace("</Historic_Dictionary>","")
    new="<WORD word= "+"'"+str(word)+"' definition= '" +str(definition)+ "'  validation= '" +str(validation)+"'   />"+"\n"
    temp+=new
    temp+="\n"+ "</Historic_Dictionary>"+"\n"
    f.write(temp)
    f.close()

def addAutoDefinitionYes():
    if word_existence(getWord()):
        QMessageBox.about(autodefinition,'خطأ','الكلمة معرفة مسبفا')
    else:
        if autodefinition.TA_result.toPlainText() != '':
            add_to_historic_dictionary(getWord(),autodefinition.TA_result.toPlainText(),'yes')
            QMessageBox.about(autodefinition,'رسالة','تم اضافة الكلمة بنجاح')
            initAutoDefinition()
            SwitchShowHistoricDictionaryWords()
            main_interface.V_TA_word_definition.clear()
        else:
            QMessageBox.about(autodefinition,'خطأ','خانة ادخال التعريف فارغة')

def addAutoDefinitionNo():
    if word_existence(getWord()):
        QMessageBox.about(autodefinition,'خطأ','الكلمة معرفة مسبفا')
    else:
        if autodefinition.TA_result.toPlainText() != '':
            add_to_historic_dictionary(getWord(),autodefinition.TA_result.toPlainText(),'no')
            QMessageBox.about(autodefinition,'رسالة','تم اضافة الكلمة بنجاح')
            initAutoDefinition()
            SwitchShowHistoricDictionaryWords()
            main_interface.V_TA_word_definition.clear()
        else:
            QMessageBox.about(autodefinition,'خطأ','خانة ادخال التعريف فارغة')

def addManDefinitionYes():
    if word_existence(getWord()):
        QMessageBox.about(mandefinition,'خطأ','الكلمة معرفة مسبفا')
    else:
        if mandefinition.TA_definition.toPlainText() != '':
            add_to_historic_dictionary(getWord(),mandefinition.TA_definition.toPlainText(),'yes')
            QMessageBox.about(mandefinition,'رسالة','تم اضافة الكلمة بنجاح')
            iniManDefinition()
            SwitchShowHistoricDictionaryWords()
            main_interface.V_TA_word_definition.clear()
        else:
            QMessageBox.about(mandefinition,'خطأ','خانة ادخال التعريف فارغة')

def addManDefinitionNo():
    if word_existence(getWord()):
        QMessageBox.about(mandefinition,'خطأ','الكلمة معرفة مسبفا')
    else:
        if mandefinition.TA_definition.toPlainText() != '':
            add_to_historic_dictionary(getWord(),mandefinition.TA_definition.toPlainText(),'no')
            QMessageBox.about(mandefinition,'رسالة','تم اضافة الكلمة بنجاح')
            iniManDefinition()
            SwitchShowHistoricDictionaryWords()
            main_interface.V_TA_word_definition.clear()
        else:
            QMessageBox.about(mandefinition,'خطأ','خانة ادخال التعريف فارغة')

def showHistoricDictionaryWords():
    main_interface.V_LW_word.clear()
    main_interface.V_B_modify_2.setEnabled(False)
    tree = Et.fromstring(getContent('historic_dictionary.xml','utf-8'))
    words = tree.findall('WORD')
    main_interface.V_C_words.addItem('الكل')
    main_interface.V_C_words.addItem('المؤكدة')
    main_interface.V_C_words.addItem('الغير المؤكدة')
    nb_words = 0
    for word in words:
        nb_words += 1
        main_interface.V_LW_word.addItem(word.get('word'))
    main_interface.V_L_words.setText('عدد الكلمات :  ' + str(nb_words))

def showHistoricDictionary():
    main_interface.V_TA_word_definition.clear()
    tree = Et.fromstring(getContent('historic_dictionary.xml','utf-8'))
    words = tree.findall('WORD')
    for word in words:
        if word.get('word') == main_interface.V_LW_word.currentItem().text():
            main_interface.V_TA_word_definition.insertPlainText(str(word.get('definition')))
            break

def SwitchShowHistoricDictionaryWords():
    main_interface.V_LW_word.clear()
    main_interface.V_TA_word_definition.clear()
    tree = Et.fromstring(getContent('historic_dictionary.xml','utf-8'))
    words = tree.findall('WORD')
    nb_words = 0
    for word in words:
        if(main_interface.V_C_words.currentIndex() == 0):
            main_interface.V_LW_word.addItem(word.get('word'))
            nb_words += 1
            main_interface.V_B_modify_2.setEnabled(False)
        else:
            main_interface.V_B_modify_2.setEnabled(True)
            if((main_interface.V_C_words.currentIndex() == 1) and (word.get('validation') == 'yes')):
                main_interface.V_LW_word.addItem(word.get('word'))
                nb_words += 1
            elif((main_interface.V_C_words.currentIndex() == 2) and (word.get('validation') == 'no')):
                main_interface.V_LW_word.addItem(word.get('word'))
                nb_words += 1
    main_interface.V_L_words.setText('عدد الكلمات :  ' + str(nb_words))

def modify_historic_dictionary(word,definition,validation):
    word=word.replace(" ","")
    new = ""
    validation=validation.replace(" ","")
    try:
        f = open("historic_dictionary.xml",encoding="utf-8")
    except:
        creat_historic_dictionary()
        f = open("historic_dictionary.xml",encoding="utf-8")
    temp = f.read()
    f.close()
    f = open("historic_dictionary.xml","w+",encoding="utf-8")
    temp = temp.replace("</Historic_Dictionary>","")
    temp = temp.replace("\n\n","\n")
    temp = re.sub(r'<W.+{}(.+\n*)+?\>'.format(word),"",temp)
    if definition != '':
        new += "<WORD word= " + "'" + str(word) + "' definition= '" + str(definition) + "'  validation= '" + str(validation) + "'   />" + "\n"
    temp += new
    temp = temp.replace("\n\n","\n")
    temp += "\n"+ "</Historic_Dictionary>" + "\n"
    f.write(temp)   
    f.close()

def deleteWord():
    if main_interface.V_LW_word.currentRow() >= 0:
        modify_historic_dictionary(main_interface.V_LW_word.currentItem().text(),'','')
        main_interface.V_TA_word_definition.clear()
        QMessageBox.about(main_interface,'رسالة','تم حذف الكلمة بنجاح')
        itemDeleted = main_interface.V_LW_word.takeItem(main_interface.V_LW_word.currentRow())
        itemDeleted = None
    else:
        QMessageBox.about(main_interface,'خطأ','حدد كلمة من اجل الحذف')

def modifyWord():
    content = main_interface.V_TA_word_definition.toPlainText()
    if content != '':
        if main_interface.V_LW_word.currentRow() >= 0:
            modify_historic_dictionary(main_interface.V_LW_word.currentItem().text(),content,'yes')
            QMessageBox.about(main_interface,'رسالة','تم تعديل الكلمة بنجاح')
        else:
            QMessageBox.about(main_interface,'خطأ','حدد كلمة من اجل التعديل')
    else:
        QMessageBox.about(main_interface,'خطأ','خانة ادخال التعريف فارغة')

def getDefinition(word_search):
    tree = Et.fromstring(getContent('historic_dictionary.xml','utf-8'))
    words = tree.findall('WORD')
    for word in words:
        if word.get('word') == word_search:
            return word.get('definition')

def ChangeValidation():
    if main_interface.V_LW_word.currentRow() >= 0:
        word = main_interface.V_LW_word.currentItem().text()
        
        if(main_interface.V_C_words.currentIndex() == 1):
            modify_historic_dictionary(word,getDefinition(word),'no')
        if(main_interface.V_C_words.currentIndex() == 2):
            modify_historic_dictionary(word,getDefinition(word),'yes')
        
        main_interface.V_TA_word_definition.clear()
        item = main_interface.V_LW_word.takeItem(main_interface.V_LW_word.currentRow())
        item = None
        QMessageBox.about(main_interface,'رسالة','تم تغيير تأكيد الكلمة بنجاح')
    else:
        QMessageBox.about(main_interface,'خطأ','حدد كلمة من اجل التعديل')

def Download_corpus()->list:
    kasida=""
    el3aser=""
    elcha3ir=""
    name_kasida=""
    kasida=""
    test = 0
    abyate_list=[]
    while(test == 0):
        try:
            nbr=random.choice(range(22,27000))
            url='https://www.aldiwan.net/poem{}.html'.format(nbr)
            print(url,'\n')
            source_code=requests.get(url)
            test = 1
        except requests.exceptions.ConnectionError as e:
            # Tell the user their URL was bad and try a different one
            main_interface.T_S_nb_poeme.clear()
            main_interface.T_S_progress_bar.setValue(0)
            return e
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            pass
    source_code.encoding="windoiws-1256" 
    soup=BeautifulSoup(source_code.content,'lxml')
    abyate_list=soup.find(class_ ="s-menu1 padding-50").find_all('h3')

    temp=soup.find(class_="col-xs-12 relative").find_all('a')
    el3aser=just_arabic(temp[1].text)
    elcha3ir=just_arabic(temp[2].text)
    name_kasida=just_arabic(soup.find(class_="col-xs-12 relative").find(class_="h2").text)   
    
    for bayte in abyate_list:
        kasida+=(just_arabic(bayte.text)) 
    return [el3aser,elcha3ir,name_kasida,kasida]
   
def creat_el3aser(el3aser):
    f=open("corpus/الشعر{}.xml".format(el3aser),"w+",encoding="utf-8")
    f.write('<?xml version="1.0" encoding="utf-8"?>'+"\n")
    el3aser = el3aser.replace(' ','_')
    f.write("<{}>".format(el3aser)+"\n")
    f.write("</{}>".format(el3aser)+"\n")
    f.close()

def kasida_exictenss(name,period,elcha3ir):
    try:
        tree = Et.fromstring(getContent("corpus/الشعر{}.xml".format(period),'utf-8'))
        L_kasida = tree.findall('kasida')
        for kasida in L_kasida:
            if((kasida.get('name') == name) and (kasida.get('elcha3ir') == elcha3ir)):
                return True
        return False
    except:
        return False

def isBlank (myString):
    if myString and myString.strip():
        return False
    return True

def add_to_el3aser(el3aser,elcha3ir,name_kasida,kasida):
    if((kasida_exictenss(name_kasida,el3aser,elcha3ir)) or (isBlank(kasida))):
        pass
    else:
        try:
            f=open("corpus/الشعر/{}.xml".format(el3aser),encoding="utf-8")
        except:
            creat_el3aser(el3aser)
            f=open("corpus/الشعر/{}.xml".format(el3aser),encoding="utf-8")
        new=""
        temp=f.read()
        f.close()
        f=open("corpus/الشعر/{}.xml".format(el3aser),"w+",encoding="utf-8")
        el3aser = el3aser.replace(' ','_')
        temp=temp.replace("</{}>".format(el3aser),"")
        new="<kasida name= "+"'"+str(name_kasida)+"' elcha3ir= '"+str(elcha3ir)+"' >"+"\n"
        new+=str(kasida)
        new+="\n</kasida>"+"\n"
        temp+=new
        temp+="\n</{}>".format(el3aser)
        f.write(temp)
        f.close()

def updatePoeme():
    try:
        nb_poeme= int(main_interface.T_S_nb_poeme.text())
        main_interface.T_S_progress_bar.setValue(random.choice(range(20,50)))
        for i in range(1,nb_poeme):
            download_content = Download_corpus()
            add_to_el3aser(download_content[0],download_content[1],download_content[2],download_content[3])
            
        main_interface.T_S_progress_bar.setValue(100)
        
        message = 'تمت اضاقة '
        message += str(nb_poeme)
        message += ' قصيدة بنجاح'
        QMessageBox.about(main_interface,'رسالة',message)
        showPeriods()
        main_interface.T_S_nb_poeme.clear()
        main_interface.T_S_progress_bar.setValue(0)
    except:
        QMessageBox.about(main_interface,'مشكلة','تحقق من وجود اتصال')

def isWordExist(word_search):
    tree = Et.fromstring(getContent('historic_dictionary.xml','utf-8'))
    words = tree.findall('WORD')
    for word in words:
        if word.get('word') == word_search:
            return True
    return False

def openFileNameDialog():
    try:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        pathFile, _ = QFileDialog.getOpenFileName(main_interface,"QFileDialog.getOpenFileName()", "","Xml Files (*.xml)", options=options)
    
        tree = Et.fromstring(getContent(pathFile,'utf-8'))
        words = tree.findall('WORD')
        nb_add_words = 0
        for word in words:
            if(isWordExist(word.get('word')) == False):
                add_to_historic_dictionary(word.get('word'),word.get('definition'),word.get('validation'))
                nb_add_words += 1
        
        message = 'تم إدماج القاموس بنجاح '
        message += '('+'اضافة ' + str(nb_add_words) + ' كلمة)'
        QMessageBox.about(main_interface,'رسالة',message)
        SwitchShowHistoricDictionaryWords()
    except:
        pass

main_interface = uic.loadUi("projectTal.ui")
autodefinition = uic.loadUi("autoDefinition.ui")
mandefinition = uic.loadUi("mandefinition.ui")
    
main_interface.B_search.clicked.connect(setResult)
main_interface.C_period.activated.connect(switchResult)
main_interface.RB_auto.clicked.connect(showAutoInteface)
main_interface.RB_man.clicked.connect(showManInteface)
main_interface.V_LW_word.clicked.connect(showHistoricDictionary)
main_interface.V_B_delete.clicked.connect(deleteWord)
main_interface.V_B_modify.clicked.connect(modifyWord)
main_interface.V_B_modify_2.clicked.connect(ChangeValidation)
main_interface.T_S_surah.activated.connect(getChapterView)
main_interface.T_S_hadith.activated.connect(getHadithView)
main_interface.T_S_period.activated.connect(showAutors)
main_interface.T_S_elcha3ir.activated.connect(showKasidas)
main_interface.T_S_kasida.activated.connect(showKasida)
main_interface.T_S_add_poeme.clicked.connect(updatePoeme)
main_interface.V_C_words.activated.connect(SwitchShowHistoricDictionaryWords)
main_interface.V_B_merge_dict.clicked.connect(openFileNameDialog)

autodefinition.B_cancel.clicked.connect(hideAutoInterface)
autodefinition.RB_local.clicked.connect(localAutoDefinition)
autodefinition.RB_notlocal.clicked.connect(WebAutoDefinition)
autodefinition.B_approve.clicked.connect(addAutoDefinitionYes)
autodefinition.B_approve_2.clicked.connect(addAutoDefinitionNo)

mandefinition.B_approve.clicked.connect(addManDefinitionYes)
mandefinition.B_approve_2.clicked.connect(addManDefinitionNo)
mandefinition.B_cancel.clicked.connect(hideManInterface)

showHistoricDictionaryWords()
showChapters()
showHadiths()
showPeriods()

main_interface.tabWidget.setCurrentIndex(0)
main_interface.tabWidget_2.setCurrentIndex(0)
main_interface.T_S_progress_bar.setValue(0)

main_interface.T_Processus.setStyleSheet("#T_Processus { border-image: url(background color.jpg) 0 0 0 0 stretch stretch; }")
main_interface.T_S_bukhari.setStyleSheet("#T_S_bukhari { border-image: url(background color.jpg) 0 0 0 0 stretch stretch; }")

main_interface.T_S_poeme.setStyleSheet("#T_S_poeme { border-image: url(background color.jpg) 0 0 0 0 stretch stretch; }")
main_interface.T_S_quran.setStyleSheet("#T_S_quran { border-image: url(background color.jpg) 0 0 0 0 stretch stretch; }")

main_interface.T_view.setStyleSheet("#T_view { border-image: url(background color.jpg) 0 0 0 0 stretch stretch; }")
#main_interface.T_sources.setStyleSheet("border-image: url(background color 1.jpg) 0 0 0 0 stretch stretch; ")
main_interface.show()

app.exec()