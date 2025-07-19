import re
from PyPDF2 import PdfReader

def extract_dialogues(pdf_path, start_page, end_page, spoken_roles, silent_roles):
    reader = PdfReader(pdf_path)
    dialogues = []
    roles_set = set(spoken_roles + silent_roles)

    text = ''
    for i in range(start_page - 1, end_page):
        text += reader.pages[i].extract_text() + '\n'

    lines = text.split('\n')
    current_character = None
    current_line = ''

    for line in lines:
        line = line.strip()

        # Jeśli linia to IMIĘ POSTACI (wielkimi literami, jedno lub dwa słowa)
        if re.fullmatch(r'[A-ZĄĆĘŁŃÓŚŻŹ]{2,}( [A-ZĄĆĘŁŃÓŚŻŹ]{2,})?', line):
            # Zapamiętaj poprzednią kwestię
            if current_character and current_line:
                if current_character in roles_set:
                    dialogues.append({
                        'character': current_character.title(),
                        'line': current_line.strip()
                    })
            current_character = line.title()
            current_line = ''
        elif line == '':
            # Koniec wypowiedzi
            if current_character and current_line:
                if current_character in roles_set:
                    dialogues.append({
                        'character': current_character.title(),
                        'line': current_line.strip()
                    })
                current_character = None
                current_line = ''
        else:
            current_line += ' ' + line

    # Dodaj ostatnią kwestię, jeśli została
    if current_character and current_line:
        if current_character in roles_set:
            dialogues.append({
                'character': current_character.title(),
                'line': current_line.strip()
            })

    return dialogues

