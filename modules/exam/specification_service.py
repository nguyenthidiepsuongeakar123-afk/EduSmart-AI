class SpecificationService:
    """
    Sinh bảng đặc tả
    """

    def generate(self, matrix):

        specification = {

            "matrix": matrix,

            "status": "ready"

        }

        return specification