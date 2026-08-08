class MatrixService:
    """
    ESA Matrix Generator
    Sinh ma trận đề kiểm tra
    """

    def generate(self, exam_config):

        matrix = {
            "subject": exam_config.get("subject", ""),
            "grade": exam_config.get("grade", ""),
            "semester": exam_config.get("semester", ""),
            "exam_type": exam_config.get("exam_type", ""),
            "duration": exam_config.get("duration", ""),
            "purpose": exam_config.get("purpose", ""),
            "class_level": exam_config.get("class_level", ""),
            "lesson_scope": exam_config.get("lesson_scope", ""),
            "requirement_mode": exam_config.get("requirement_mode", ""),
            "teacher_requirement": exam_config.get(
                "teacher_requirement", ""
            ),

            # bước sau sẽ sinh thật
            "levels": [
                "Nhận biết",
                "Thông hiểu",
                "Vận dụng",
                "Vận dụng cao"
            ],

            "status": "ready"
        }

        return matrix