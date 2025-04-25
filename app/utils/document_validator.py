import re

class DocumentValidator:
    @staticmethod
    def sanitize(document: str) -> str:
        return re.sub(r"\D", "", document)

    @staticmethod
    def calculate_cnpj_digit(numbers: str, weights: list[int]) -> str:
        total = sum(int(d) * w for d, w in zip(numbers, weights))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)

    @classmethod
    def validate_cnpj(cls, cnpj: str) -> bool:
        cnpj = cls.sanitize(cnpj)

        if len(cnpj) != 14 or cnpj in (c * 14 for c in "0123456789"):
            return False

        first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        second_weights = [6] + first_weights

        first_digit = cls.calculate_cnpj_digit(cnpj[:12], first_weights)
        second_digit = cls.calculate_cnpj_digit(cnpj[:12] + first_digit, second_weights)

        return cnpj[-2:] == first_digit + second_digit

