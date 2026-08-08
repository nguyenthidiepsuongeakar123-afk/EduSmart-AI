class ExamService:
    """
    Sinh đề kiểm tra
    """

    def generate(self, specification):

        exam = {

            "status": "ready",

            "specification": specification,

            "questions": []

        }

        return exam