import re
from jacowvalidator.docutils.styles import check_style_detail

NON_BREAKING_SPACE = '\u00A0'
LINE_TERMINATOR_CHARS = ['\u000A', '\u000B', '\u000C', '\u000D', '\u0085', '\u2028', '\u2029', '\n', '\\n']
# line terminator chars respectively:
# line feed, vertical tab, form feed, carriage return,
# next line, line separator, paragraph separator

STYLES = {
    'normal': {
       'type': 'Author List',
       'styles': {
           'jacow': 'JACoW_Author List',
           'normal': 'Author List',
       },
       'alignment': 'CENTER',
       'font_size': 12.0,
       'space_before': 9.0,
       'space_after': 12.0,
       'bold': None,
       'italic': None,
   }
}
EXTRA_RULES = ['Case: UPPER and lowercase']
HELP_INFO = 'SCEAuthors'


def get_author_details(p):
    superscript_removed_text = ''  # remove superscript footnotes
    for r in p.runs:
        superscript_removed_text += r.text if not r.font.superscript else ''
    author_detail = {
        'text': superscript_removed_text,
        'original_text': p.text,
    }
    return author_detail


def get_author_summary(paragraphs):
    style_compare = STYLES['normal']
    author_details = []
    for p in paragraphs:
        if p.text.strip():
            detail = get_author_details(p)
            detail.update(check_style_detail(p, style_compare))
            title_style_ok = p.style.name == style_compare['styles']['jacow']
            detail.update({'title_style_ok': title_style_ok, 'style': p.style.name})
            author_details.append(detail)

    return {
        'details': author_details,
        'rules': STYLES,
        'extra_rules': EXTRA_RULES,
        'help_info': HELP_INFO,
        'title': 'Author',
        'ok': all([tick['style_ok'] for tick in author_details]),
        'message': 'Author issues',
        'anchor': 'author'
    }


def get_author_summary_latex(part):
    if part and part.string:
        text = part.string
        return {'text': text, 'title': 'Author', 'ok': True, 'extra_info': f'Author: {text}'}

    return {'text': '', 'title': 'Author', 'ok': False, 'extra_info': f'No Author found'}


def get_author_list(text):
    """function to extract authors from some text that will also include
    associations

    example input:

    `J. C. Jan†, F. Y. Lin, Y. L. Chu, C. Y. Kuo, C. C. Chang, J. C. Huang and C. S. Hwang,
National Synchrotron Radiation Research Center, Hsinchu, Taiwan, R.O.C`

    or

    `M.B. Behtouei, M. Migliorati, L. Palumbo, B. Spataro, L. Faillace`

    assumptions:

    - if you split by ', ' and the second character of a token is a '.' period
        then its probably a valid token (an author) but this is not guaranteed
        (see above example that ends in 'R.O.C')

    - There can be multiple initials as evidenced above.

    - Initials may not necessarily be split by a space.

    watch out for:

    - hypenated names: 'B. Walasek-Hoehne'
    - hyphenated initials: 'E. J-M. Voutier' 'J.-L. Vay'
    - multiple surnames: 'M.J. de Loos' 'S.B. van der Geer' 'A. Martinez de la Ossa' 'N. Blaskovic Kraljevic' 'G. Guillermo Cant�n' 'C. Boscolo Meneguolo'
    - surname with apostrophes: 'G. D'Alessandro'
    - extra stuff tacked on: 'S.X. Zheng [on leave]' 'G.R. Li [on leave]' (from the csv file)
    - one rare instance of non-period separated initials: 'Ph. Richerot (from csv file)

    my pattern of a name which should match vast majority of names while not matching vast majority of non-names:
    single letter, followed by a period, potentially followed by a space but
    not always, repeated n times, and ending in a word of more than one character
    which may contain hyphens, apostrophes, repeated n times, and finally
    finishing with a comma

    word character followed by dot and potentially space, repeated n times
    then
    word character repeated n times

    /(\\w\\.\\ ?)+(\\w+\\ ?)+/g   (note this comment had to double up the escape backslashes)

    (https://regexr.com/)

    """
    newline_fixed_text = text
    for newline_char in LINE_TERMINATOR_CHARS:
        newline_fixed_text = newline_fixed_text.replace(newline_char, ' , ')
    potential_authors = newline_fixed_text.replace(NON_BREAKING_SPACE, ' ').replace(' and ', ', ').split(', ')
    filtered_authors = list()
    my_name_pattern = re.compile("(-?\\w\\.\\ ?)+([\\w]{2,}\\ ?)+")
    # the allowance of an optional hyphen preceding an initial is to satisfy a
    # common pattern observed with the papers coming out of asia.
    for author in potential_authors:
        if my_name_pattern.match(author):   # match has an implied ^ at the start
            # which is ok for our purposes.
            filtered_authors.append(author)
    return filtered_authors
