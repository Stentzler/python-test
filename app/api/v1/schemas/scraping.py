from pydantic import BaseModel, field_validator
from app.utils.document_validator import DocumentValidator

class ScrapeRequest(BaseModel):
    cnpj: str

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v):
        if not DocumentValidator.validate_cnpj(v):
            raise ValueError(f"CNPJ inválido: {v}. Verifique se possui 14 dígitos e se estão corretos.")
        return v
