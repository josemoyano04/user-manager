from pydantic import BaseModel, EmailStr, Field

class RecoveryPasswordRequest(BaseModel):
    receiver_email: EmailStr = Field(..., description="Email del destinatario")
    sender_email: EmailStr = Field(..., description="Email del remitente")
    password_email: str = Field(..., description="Contraseña del remitente")
    email_template_html: str | None = Field(None, description="Plantilla HTML del correo electrónico")
    custom_code: str | None = Field(None, description="Código de recuperación personalizado")