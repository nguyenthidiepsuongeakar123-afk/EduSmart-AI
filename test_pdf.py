from modules.knowledge_import.pdf_parser import extract_lessons

pdf = r"D:\Phan mem\ESA\SGK\SGK-Vat-li-12.pdf"

lessons = extract_lessons(pdf)

for lesson in lessons:
    print(lesson)