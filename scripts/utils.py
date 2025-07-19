from PyPDF2 import PdfReader

def extract_dialogues(pdf_path, start_page, end_page, spoken_roles, silent_roles):
    reader = PdfReader(pdf_path)
    dialogues = []

    # Zbierz wszystkie role jako wielkie litery
    all_roles = [r.upper() for r in spoken_roles + silent_roles]

    for page_num in range(start_page - 1, end_page):
        if page_num >= len(reader.pages):
            continue

        page = reader.pages[page_num]
        text = page.extract_text()
        if not text:
            continue

        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            line_upper = line.upper()

            if line_upper in all_roles:
                character = line_upper
                spoken = character in [r.upper() for r in spoken_roles]

                # Zbieramy kolejne linie jako wypowiedź postaci
                dialogue_lines = []
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    next_upper = next_line.upper()

                    if next_upper in all_roles or next_line == '':
                        break

                    dialogue_lines.append(next_line)
                    i += 1

                full_line = ' '.join(dialogue_lines)

                dialogues.append({
                    'character': character,
                    'line': full_line,
                    'spoken': spoken,
                })
            else:
                i += 1

    return dialogues
