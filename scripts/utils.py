import re
from PyPDF2 import PdfReader

def extract_dialogues(pdf_path, start_page, end_page, spoken_roles, silent_roles):
    """
    Wyciąga kwestie dialogowe z pliku PDF.
    Obsługuje:
    1. IMIĘ: treść
    2. IMIĘ: (pusto) -> treść w następnej linii
    3. IMIĘ w osobnej linii -> treść w kolejnych liniach
    """
    reader = PdfReader(pdf_path)
    dialogues = []
    roles_set = set([r.title() for r in spoken_roles + silent_roles])

    text = ''
    for i in range(start_page - 1, end_page):
        page_text = reader.pages[i].extract_text()
        if page_text:
            text += page_text + '\n'

    lines = text.split('\n')
    current_character = None
    current_line = ''

    for idx, line in enumerate(lines):
        line = line.strip()

        # Format 1 i 2: IMIĘ: treść lub IMIĘ: (treść dalej)
        m = re.match(r'^([A-ZĄĆĘŁŃÓŚŻŹ]{2,}(?: [A-ZĄĆĘŁŃÓŚŻŹ]{2,})?):\s*(.*)$', line)
        if m:
            char_name, line_text = m.groups()
            char_name = char_name.title()

            if not line_text.strip() and idx + 1 < len(lines):
                next_line = lines[idx+1].strip()
                line_text = next_line

            if char_name in roles_set and line_text:
                dialogues.append({'character': char_name, 'line': line_text})
            current_character = None
            current_line = ''
            continue

        # Format 3: Teatralny (IMIĘ osobno)
        if re.fullmatch(r'[A-ZĄĆĘŁŃÓŚŻŹ]{2,}(?: [A-ZĄĆĘŁŃÓŚŻŹ]{2,})?', line):
            if current_character and current_line:
                if current_character in roles_set:
                    dialogues.append({'character': current_character, 'line': current_line.strip()})
            current_character = line.title()
            current_line = ''
        elif line == '':
            if current_character and current_line:
                if current_character in roles_set:
                    dialogues.append({'character': current_character, 'line': current_line.strip()})
                current_character = None
                current_line = ''
        else:
            current_line += ' ' + line

    if current_character and current_line:
        if current_character in roles_set:
            dialogues.append({'character': current_character, 'line': current_line.strip()})

    return dialogues
