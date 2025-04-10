import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from errors.send_email_error import SendEmailError
from models.recovery_code import RecoveryCode
from services.password_recovery_code_manager import PasswordRecoveryCodeManager
from utils.env_loader import EnvManager

class PasswordRecoveryEmailSender():
    def _set_code_in_html(self, html: str | None, code: str, username: str) -> str:
        
        if html is None: 
            html = self.load_default_template()
                
        parser = BeautifulSoup(html, "html.parser")
        html_username = parser.find(id= "username-to-recovering-password")
        html_code = parser.find(id= "password-recovery-code")
        
        if html_username is None or html_code is None:
            html = self.load_default_template()
            parser = BeautifulSoup(html, "html.parser")
            html_username = parser.find(id="username-to-recovering-password")
            html_code = parser.find(id="password-recovery-code")
        
        if html_username:
            html_username.string = username
        if html_code:
            html_code.string = code

        return str(parser)
    
    def send_email_recovery_password(self, username:str, sender_email: str, password_email: str,
                                    receiver_email: str, email_template_html: str = None, custom_code: str = None) -> None:
        
        if custom_code: 
            code = RecoveryCode(code= custom_code, minutes_of_code_lifetime= int(EnvManager().get("CODE_EXPIRE_MINUTES")))
            PasswordRecoveryCodeManager().save_code(user_email= receiver_email, code= code)
            
        message = MIMEMultipart("alternative")
        message["Subject"] = "Restablecer contraseña"
        message["From"] = sender_email
        message["To"] = receiver_email
    
        html = self._set_code_in_html(html= email_template_html,
                                      code= self.build_code(receiver_email).code if custom_code is None else custom_code,
                                      username= username) 
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password_email)
                server.sendmail(sender_email, receiver_email, message.as_string())
                
        except Exception as E:
            raise SendEmailError(str(E))
        
    def build_code(self, user_email: str) -> RecoveryCode:
        p = PasswordRecoveryCodeManager()
        code = p.generate_code(user_email= user_email)
        
        return code
    
    def load_default_template(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join("..", "templates", "default_email_template.html")
        template_path = os.path.abspath(os.path.join(current_dir, relative_path))

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"""Plantilla no encontrada, relative path:{relative_path}, 
                                    absolute path: {template_path}""")
            
        with open(template_path, encoding="utf-8") as file:
            html = file.read()
            
        return html