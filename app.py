from database import (
    init_database,
    insert_document,
    get_all_documents,
    create_default_folders,
    get_all_folders,

    has_system_settings,
    get_system_settings,
    save_system_settings
)
from modules.exam import (
    MatrixService,
    SpecificationService,
    ExamService
)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    jsonify
)

import os
from datetime import datetime
import json

# ===========================
# KHỞI TẠO HỆ THỐNG ESA
# ===========================

app = Flask(__name__)

app.secret_key = "ESA_SECRET_KEY_2026"

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_database()

create_default_folders()

# ===========================
# TRANG CHỦ
# ===========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    # Kiểm tra chưa chọn file
    if file is None or file.filename == "":
        return redirect("/library")

    save_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

    file.save(save_path)

    file_size = round(os.path.getsize(save_path) / 1024 / 1024, 2)

    extension = os.path.splitext(file.filename)[1].lower()

    if extension == ".pdf":
        file_type = "PDF"

    elif extension in [".doc", ".docx"]:
        file_type = "WORD"

    elif extension in [".xls", ".xlsx"]:
        file_type = "EXCEL"

    elif extension in [".ppt", ".pptx"]:
        file_type = "POWERPOINT"

    elif extension in [".jpg", ".jpeg", ".png"]:
        file_type = "IMAGE"

    else:
        file_type = "KHÁC"

    insert_document(

        file_name=file.filename,

        file_type=file_type,

        file_size=file_size,

        file_path=save_path

)

    print("Đã lưu:", file.filename)

    return redirect("/library")

@app.route("/library")
def library():

    documents = get_all_documents()

    folders = get_all_folders()

    return render_template(
        "library.html",
        documents=documents,
        folders=folders
    )

# ===========================
# MODULE SINH ĐỀ
# ===========================

@app.route("/generate_exam")
def generate_exam():

    has_setting = has_system_settings()

    setting = None

    if has_setting:
        setting = get_system_settings()

    # ==========================
    # Danh sách bài (Demo)
    # Sau này sẽ lấy từ lesson_master
    # ==========================
    subject = request.args.get("subject", "Vật lí")
    grade = request.args.get("grade", "12")

    lesson_data = {
        "Vật lí": {
            "10": [
                {"id": 101, "name": "Bài 1. Mở đầu"},
                {"id": 102, "name": "Bài 2. Động học"},
                {"id": 103, "name": "Bài 3. Chuyển động thẳng"},
                {"id": 104, "name": "Bài 4. Chuyển động biến đổi"},
            ],
            "11": [
                {"id": 201, "name": "Bài 1. Dao động điều hòa"},
                {"id": 202, "name": "Bài 2. Sóng cơ"},
                {"id": 203, "name": "Bài 3. Điện trường"},
            ],
            "12": [
                {"id": 301, "name": "Bài 1. Cấu trúc của chất. Sự chuyển thể"},
                {"id": 302, "name": "Bài 2. Nội năng"},
                {"id": 303, "name": "Bài 3. Nhiệt động lực học"},
                {"id": 304, "name": "Bài 4. Khí lí tưởng"},
                {"id": 305, "name": "Bài 5. Định luật Boyle"},
            ]
        }
    }

    lessons = lesson_data.get(subject, {}).get(
        grade,
        []
    )

    lessons = [
        {"id": 1, "name": "Bài 1. Cấu trúc của chất"},
        {"id": 2, "name": "Bài 2. Nội năng"},
        {"id": 3, "name": "Bài 3. Khí lí tưởng"},
        {"id": 4, "name": "Bài 4. Định luật Boyle"},
        {"id": 5, "name": "Bài 5. Định luật Charles"}
    ]

    return render_template(

        "generate_exam.html",

        has_setting=has_setting,

        setting=setting,

        lessons=lessons

    )

# ===========================
# ESA SINH ĐỀ
# ===========================

@app.route("/generate_exam", methods=["POST"])
def generate_exam_submit():

    try:

        exam_config = {

            # ===== Thông tin đề =====

            "subject": request.form.get("subject", ""),

            "grade": request.form.get("grade", ""),

            "semester": request.form.get("semester", ""),

            "exam_type": request.form.get("exam_type", ""),

            "duration": request.form.get("duration", ""),

            "class_level": request.form.get("class_level", ""),

            "purpose": request.form.get("purpose", ""),

            # ===== Phạm vi kiến thức =====

            "lesson_scope": request.form.get("lesson_scope", ""),

            # ===== Yêu cầu cần đạt =====

            "requirement_mode": request.form.get("requirement_mode", ""),

            "teacher_requirement": request.form.get("teacher_requirement", ""),

            # ===== Nguồn dữ liệu =====

            "source_sgk": "source_sgk" in request.form,

            "source_sgv": "source_sgv" in request.form,

            "source_plan": "source_plan" in request.form,

            "source_department": "source_department" in request.form,

            "source_library": "source_library" in request.form

        }

        # ==========================
        # Danh sách bài (Demo)
        # ==========================

        lessons = [
            {"id": 1, "name": "Bài 1. Cấu trúc của chất"},
            {"id": 2, "name": "Bài 2. Nội năng"},
            {"id": 3, "name": "Bài 3. Khí lí tưởng"},
            {"id": 4, "name": "Bài 4. Định luật Boyle"},
            {"id": 5, "name": "Bài 5. Định luật Charles"}
        ]

        # ===========================
        # ESA Exam Engine
        # ===========================

        matrix_service = MatrixService()
        matrix = matrix_service.generate(exam_config)

        specification_service = SpecificationService()
        specification = specification_service.generate(matrix)

        exam_service = ExamService()
        exam = exam_service.generate(specification)

        print("="*50)
        print("ESA EXAM CONFIG")
        print("="*50)
        print(json.dumps(
            exam_config,
            indent=4,
            ensure_ascii=False
        ))
        print("="*50)

        flash("Đã nhận dữ liệu sinh đề.", "success")

        return render_template(
            "generate_exam.html",
            exam_config=exam_config,
            matrix=matrix,
            specification=specification,
            exam=exam,
            lessons=lessons,
            has_setting=has_system_settings(),
            setting=get_system_settings() if has_system_settings() else None
        )

    except Exception as e:

        flash(str(e), "danger")

        return redirect("/generate_exam")


# ===========================
# MODULE CHẤM BÀI
# ===========================

@app.route("/grade_exam")
def grade_exam():

    return render_template(
        "grade_exam.html"
    )

# ===========================
# HỒ SƠ HỌC TẬP
# ===========================

@app.route("/student_profile")
def student_profile():

    return render_template(
        "student_profile.html"
    )

# ===========================
# ÔN TẬP THÔNG MINH
# ===========================

@app.route("/smart_review")
def smart_review():

    return render_template(
        "smart_review.html"
    )

# ===========================
# CÀI ĐẶT
# ===========================

@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )


# Chạy chương trình
if __name__ == "__main__":
    app.run(debug=True)