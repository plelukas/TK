
import os
import sys
import re
import codecs

_CONTENT_PATTERN = r'(?<=content=")(.+?)(?=")'


def get_author(content):
    meta_author_pattern = r'<meta (.*)name="autor"(.*?)>'
    r = re.compile(meta_author_pattern, re.IGNORECASE)
    m = r.search(content)
    r = re.compile(_CONTENT_PATTERN, re.I)
    author = r.search(m.group())
    return author.group()


def get_dzial(content):
    meta_dzial_pattern = r'<meta (.*)name="dzial"(.*?)>'
    r = re.compile(meta_dzial_pattern, re.I)
    m = r.search(content)
    r = re.compile(_CONTENT_PATTERN, re.I)
    dzial = r.search(m.group())
    return dzial.group()


def get_key_words(content):
    meta_kw_pattern = r'<meta (.*)name="kluczowe_(\d+)"(.*?)>'
    m = re.findall(meta_kw_pattern, content, re.I)
    r = re.compile(_CONTENT_PATTERN, re.I)
    key_words = []
    for kw in re.findall(meta_kw_pattern, content, re.I):
        key_word = r.search(kw[2])
        if key_word:
            key_words.append(key_word.group())
    return key_words


def count_contractions(text):
    pattern = r'\W[a-zA-Z]{1,3}\.'
    contractions = re.compile(pattern).findall(text)
    contraction_set = set()
    for i in contractions:
        contraction_set.add(i)
    return len(contraction_set)


def count_sentences(text):
    pattern = r'(.*?)\s[a-zA-ZęóąśłżźćńĘÓĄŚŁŻŹĆŃ]{4,}(?=([\.?!]+|(<(.*)>)?$))'
    ret = re.compile(pattern, re.MULTILINE).findall(text)
    print(ret)
    return len(ret)


def count_mails(text):
    mails_r = re.compile(r'(?<=\s)(\w)+@(\w)+(\.(\w)+)+(?=\s)')
    mails_set = set()
    for mail in mails_r.finditer(text):
        print(mail.group())
        mails_set.add(mail.group())
    return len(mails_set)


def count_ints(text):
    patterns = [r'[0-9]{1,4}', r'[0-3][0-2][0-7][0-6][0-7]', r'0', r'-32768']
    pattern = r'''((?<=/|\^|\*|\+|-|<|>|=|,|"|'|\s)(0*)(%s|%s|%s|%s)(?=/|\^|\*|\+|-|<|>|=|,|"|'|\s))''' % tuple(patterns)

    int_r = re.compile(pattern)
    int_set = set()
    for i in int_r.finditer(text):
        int_set.add(i.group())
    return len(int_set)


def count_floats(text):
    pattern_left = r'((\d)+\.(\d)*)'
    pattern_right = r'((\d)*\.(\d)+)'
    pattern_center = r'((\d)+\.(\d)+)'
    pattern = r'''(/|\^|\*|\+|-|<|>|=|,|"|'|\s''' + pattern_left + r'|' + pattern_center + r'|' + pattern_right + r'''((e[+-]?(\d)+)?)[/\^\*\+<>=,"'\s]'''
    tmp = re.compile(pattern)
    float_set = set()
    for i in tmp.finditer(text):
        float_set.add(i.group())
    print ("flołty: ", float_set)
    return len(float_set)


def count_dates(content):
    days_months = [
        # dd: 01-29; mm: 01-12;
        r'(0[1-9]|[1-2][0-9])', r'(0[1-9]|1[0-2])',
        # dd: 30; mm: 01-12 \ 02  (except february)
        r'(30)', r'(01|0[3-9]|1[[0-2])',
        # dd: 31;
        r'(31)', r'(01|03|05|07|08|10|12)'
    ]
    years = r'([0-9]{4})'

    params_list = days_months[:] + [years]
    dates_patterns_with_minus = r'(?<!\d)((%s-%s)|(%s-%s)|(%s-%s))-%s(?!\d)' % tuple(params_list)
    dates_patterns_with_dot = r'(?<!\d)((%s\.%s)|(%s\.%s)|(%s\.%s))\.%s(?!\d)' % tuple(params_list)
    dates_patterns_with_slash = r'(?<!\d)((%s/%s)|(%s/%s)|(%s/%s))/%s(?!\d)' % tuple(params_list)

    params_list2 = [years] + days_months[:]
    dates_patterns2_with_minus = r'%s-((%s-%s)|(%s-%s)|(%s-%s))' % tuple(params_list2)
    dates_patterns2_with_dot = r'%s\.((%s\.%s)|(%s\.%s)|(%s\.%s))' % tuple(params_list2)
    dates_patterns2_with_slash = r'%s/((%s/%s)|(%s/%s)|(%s/%s))' % tuple(params_list2)

    dates_patterns = r'(%s)|(%s)|(%s)|(%s)|(%s)|(%s)' % (
        dates_patterns2_with_dot, dates_patterns2_with_minus, dates_patterns2_with_slash,
        dates_patterns_with_dot, dates_patterns_with_minus, dates_patterns_with_slash
    )

    date_match = r'^[\d]{4}'
    date_r = re.compile(date_match)
    r = re.compile(dates_patterns)
    dates = set()
    for date in r.finditer(content):
        date = date.group()
        if date_r.match(date):
            # rrrr`dd`mm format
            year = int(date[0:4])
            day = int(date[5:7])
            month = int(date[8:10])
        else:
            # dd`mm`rrrr
            day = int(date[0:2])
            month = int(date[3:5])
            year = int(date[6:10])

        date_str = str(day) + str(month) + str(year)
        dates.add(date_str)

    return len(dates)


def get_text(content):
    text_pattern = r'<p[ >](.*?)(?=<meta (.*?)>)'
    r = re.compile(text_pattern, re.I | re.DOTALL)
    m = r.search(content)
    return m.group()

def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()
    fp.close()

    author = get_author(content)
    dzial = get_dzial(content)
    key_words = get_key_words(content)

    search_text = get_text(content)
    dates_count = count_dates(search_text)
    sentences_count = count_sentences(search_text)
    ints_count = count_ints(search_text)
    floats_count = count_floats(search_text)
    mails_count = count_mails(search_text)

    print("nazwa pliku:", filepath)
    print("autor:", author)
    print("dzial:", dzial)
    print("slowa kluczowe:", key_words)
    print("liczba zdan:", sentences_count)
    print("liczba skrotow:")
    print("liczba liczb calkowitych z zakresu int:", ints_count)
    print("liczba liczb zmiennoprzecinkowych:", floats_count)
    print("liczba dat:", dates_count)
    print("liczba adresow email:", mails_count)
    print("\n")


try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)


