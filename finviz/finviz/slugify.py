import re
from unicodedata import normalize

# code adapted from http://stackoverflow.com/questions/9042515
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
def slugify(text, delim=u'_'):
    """Generates an slightly worse ASCII-only slug."""
    result = []

    # special case to toss out date specific strings
    if '(' in text and any([month in text.lower() for month in months]):
        text = text[:text.index('(')]

    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    result = unicode(delim.join(result))
    if not result[0].isalpha(): # add _ if name starts with nu
        result = '_' + result
    return result
