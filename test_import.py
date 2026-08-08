from modules.knowledge_import.parser import parse_docx

file_path = r"D:\Phan mem\ESA\SGK\SGK-Vat-li-12.pdf"

lessons = parse_docx(file_path)

print("=" * 50)

for lesson in lessons:
    print(lesson)

print("=" * 50)
print(f"Tổng số bài: {len(lessons)}")