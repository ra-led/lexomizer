import re
from razdel import sentenize, tokenize
from pytrovich.enums import NamePart, Gender, Case

class Transformer():

    def __init__(self, morph, alias_maker):
        self.morph = morph
        self.alias_maker = alias_maker
        
        self.SELF_NPRO_ALIAS = {
            'я': {'f': morph.parse('она')[0], 'm': morph.parse('он')[0]},
            'мы': {'f': morph.parse('они')[0], 'm': morph.parse('они')[0]}
        }
    
        self.PRIT_NPRO_ALIAS = {
            'мой': {'f': 'её', 'm': 'его'},
            'наш': {'f': 'их', 'm': 'их'}
        }
        
        self.ALIAS_CASE = {
            'gent': Case.GENITIVE,
            'datv': Case.DATIVE,
            'accs': Case.ACCUSATIVE,
            'ablt': Case.INSTRUMENTAL,
            'loct': Case.PREPOSITIONAL
        }
        self.ALIAS_GENDER = {
            'm': Gender.MALE,
            'f': Gender.FEMALE
        }

        
class Token():
    def __init__(self, word, morph_word, sentence_id, word_id, freeze=False):
        self.view = word
        self.orig = word
        self.lemma = morph_word.normal_form
        self.id_ = word_id
        self.morph_word = morph_word
        self.pos = morph_word.tag.POS
        self.case = morph_word.tag.case
        self.gender = morph_word.tag.gender
        self.person = morph_word.tag.person
        self.flags = set()
        self.freeze = freeze
        

class Person():
    def __init__(self, trf, orig_text, id_, gender,
                 first_name='', last_name='', middle_name='',
                 role=None):
        self.orig_text = orig_text
        self.morphed_text = parse_text(orig_text, trf)
        self.gender = gender
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        # инициалы
        try:
            if middle_name:
                self.short_name = f'{first_name[0].upper()}.{middle_name[0].upper()}.'
            else:
                self.short_name = f'{first_name[0].upper()}.'
        except IndexError:
            self.short_name = None
        
    def print_text(self, orig=False):
        if orig:
            print(self.orig_text)
        else:
            view_text = []
            for s in self.morphed_text:
                for token in s:
                    view = token.view if token.flags == set() else token.view + f' [{token.lemma}] '
                    view_text.append(view)
            print(' '.join(view_text))
            
    def postprocess(self):
        view_text = []
        for s in self.morphed_text:
            for token in s:
                view = token.view
                view_text.append(view)
        text = ' '.join(view_text)
        # декод замороженных инициалов
        text = re.sub(r'(« )([А-Я]) (\.) ([А-Я]) (\.) (» )', r'\2\3\4\5 ', text)
        # декод переноса строк
        text = text.replace(' < nl > ', '\n')
        return text
        

def parse_text(text, trf):
    # переносы строк
    text = text.replace('\n', '<nl>')
    # заморозка инициалов
    text = re.sub('([А-Я]\.[А-Я]\.)', r'«\1»', text)
    qoute = False
    morphed_text = []
    for s_id, s in enumerate(list(sentenize(text))):
        sentence = []
        for w_id, w in enumerate(list(tokenize(s.text))):
            if (not qoute) & (w.text == '«'):
                qoute = True
            if qoute & (w.text == '»'):
                qoute = False
            sentence.append(
                Token(w.text, trf.morph.parse(w.text)[0], s_id, w_id, freeze=qoute)
            )
        morphed_text.append(sentence)
    return morphed_text
        
        
def per_1_to_3(author, trf):
    for s in author.morphed_text:
        prefix = ('', '', False)
        for i, token in enumerate(s):
            # ОБРАБОТКА МЕСТОИМЕНИЙ
            # личные местоимения
            try:
                new_token = trf.SELF_NPRO_ALIAS[token.lemma][author.gender]
                # если перед местоимением стоит ненаречный предлог
                prefix_omonims = [x.tag.POS for x in trf.morph.parse(prefix[0])]
                if prefix[0].lower() == 'для':
                    # исключение "для"
                    prefix_omonims = []
                if (prefix[1] == 'PREP') & ('GRND' not in prefix_omonims):
                    # исключение "мне" в Предложном падеже
                    # если местоимение в дательном падеже, но предлоги на это не указывают
                    if (prefix[0].lower() not in ['ко', 'по']) & (token.case == 'datv'):
                        token.case = 'loct'
                    token.view = new_token.inflect({token.case, 'Af-p'}).word
                    token.flags.add(f'{token.orig} -> {token.view}') # DEBUG
                    # если необходимо, то исправить фрому предлога перед местоимением
                    if prefix[2]:
                        s[i-1].view = s[i-1].morph_word.normal_form
                        s[i-1].flags.add(f'{prefix[0]} -> {s[i-1].orig}') # DEBUG
                else:
                    token.view = new_token.inflect({token.case}).word
                    token.flags.add(f'{token.orig} -> {token.view}') # DEBUG
            except KeyError:
                pass
            # притяжательные местоимения
            try:
                new_token = trf.PRIT_NPRO_ALIAS[token.lemma][author.gender]
                token.view = new_token
                token.flags.add(f'{token.orig} -> {token.view}') # DEBUG
            except KeyError:
                pass
            # ОБРАБОТКА ОСТАЛЬНЫХ СЛОВ
            if token.person == '1per':
                new_w = token.morph_word.inflect({'3per'})
                if new_w:
                    token.view = new_w.word
                    token.flags.add(f'{token.orig} -> {token.view}') # DEBUG
            prefix = (token.view, token.pos, 'Vpre' in token.morph_word.tag)
            if token.freeze:
                token.view = token.orig
    return author
               


def give_alias(trf, author, case, temp_alias):
    # склонение фамилии
    if case in trf.ALIAS_CASE:
        alias = trf.alias_maker.make(
            NamePart.LASTNAME,
            trf.ALIAS_GENDER[author.gender],
            trf.ALIAS_CASE[case],
            author.last_name
        )
    else:
        alias = author.last_name
    # добавление инициалов, если есть
    if author.short_name:
        alias = alias + ' ' + author.short_name
    else:
        alias = temp_alias
    return alias


def postprocess_alias_1_to_3(author, trf, temp_alias='XXX'):
    for s in author.morphed_text:
        s_lemmas = [t.lemma for t in s]
        confuse = trf.SELF_NPRO_ALIAS['я'][author.gender].normal_form in s_lemmas
        for i, token in enumerate(s):
            if (token.lemma == 'я') & confuse:
                token.view = give_alias(trf, author, token.case, temp_alias)
    return author
