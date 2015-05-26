import re
import codecs

def read_file(name):
    f = codecs.open(name, u'r', u'utf-8')
    text = f.read()#.replace(u'\r\n', u' ')
    f.close()
    return text

def save_file(name, text):
    f = codecs.open(name, u'w', u'utf-8')
    f.write(text)
    f.close()
    return 'Done!'

# разбивка текста на предложения с обработкой сокращений
def splitter(text):
    MARKS_RE = ur'([\.!?]{1,}) '
    abbrs = [u' шт', u' гб', u' ч', u' г', u' гг', u' лат', u' фр', u' нов',\
             u' англ', u' в', u' вв', u' см', u' ср', u' перен', u' напр',\
             u' с', u' стр']
    
    result = re.split(MARKS_RE, text)
        
    for i in range(len(result)):
        for abbr in abbrs:
            if result[i].endswith(abbr):
                result[i] += u'. ' + result[i+2] + result[i+3]
    
    for i in result:
        if any(abbr + u'.' in i for abbr in abbrs):
            result = result[:result.index(i)] + [i] + result[result.index(i)+4:]

    for i in range(len(result)):
        try:
            if len(result[i]) < 4:
                result[i-1] += result[i]
                result.remove(result[i])
        except:
            pass
    
    return result

# обработка предложений по точке с запятой
def punct_semicolon(text):
    existence = re.findall(u';', text)
    if len(existence) > 0:
        splitted = text.split(u';')
        for n in xrange(len(splitted) - 1):
            if len(splitted[n]) != 0:
                if float(len(splitted[n + 1]))/len(splitted[n]) > 0.8 and\
                   splitted[n + 1][-1] == u'.' and n == 0:
                    result = splitted[n] + u'. ' + splitted[n+1][1].upper() + splitted[n+1][2:]
                else:
                    result = text
            else:
                result = text
    else:
        result = text
    return result

# обработка предложений по скобкам
def punct_brackets(text):
    result = text
    existence = re.findall(u'\(.+?\)', text)
    if len(existence) > 0:
        for each in existence:
            # проверка, русский ли комментарий в скобках
            if_rus = re.findall(u'[А-Яа-яЁё]', each)
            if not if_rus:
                continue
            # проверка, аббревиатура или нет
            if_abbr = re.findall(u'[а-яё\?!\.,]', each)
            if not if_abbr:
                continue
            # проверка первого слова
            if each.startswith(u'(кроме ') or each.startswith(u'(исключая '):
                continue
            else:
                result = result.replace(each, '')
    return result

# обработка предложений по тире и дефисам
def punct_dash(text):
    existence = re.findall(u' - .+? -', text)
    result = text
    if existence:
        for each in existence:
            result = result.replace(each, '')
    return result

# all_in
def all_in(name):
    all_adapted_text = ''
    text = read_file(name)

    paragraphs = text.split('\r\n')
    for paragraph in paragraphs:
        sent_array = splitter(paragraph)
        for sentence in sent_array:
            sentence = punct_semicolon(sentence)
            sentence = punct_brackets(sentence)
            sentence = punct_dash(sentence)
            all_adapted_text += sentence + ' '
        all_adapted_text += '\r\n'
    return save_file(u'adapted_text.txt', all_adapted_text)

name = raw_input('Input name of the file: ')
print all_in(name)
