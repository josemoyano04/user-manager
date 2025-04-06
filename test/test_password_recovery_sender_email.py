import pytest
from services.password_recovery_email_sender import PasswordRecoveryEmailSender
from utils.env_loader import EnvManager

def test_set_code_in_html():
    # Arrange
    sender = PasswordRecoveryEmailSender()
    html_template = """
    <html>
        <body>
            <p>Hola <span id="username-to-recovering-password"></span>,</p>
            <p>Tu código de recuperación es: <span id="password-recovery-code"></span></p>
        </body>
    </html>
    """
    code = "12345"
    username = "ExampleUser"

    # Act
    result = sender._set_code_in_html(html=html_template, code=code, username=username)

    # Assert
    assert '<span id="username-to-recovering-password">ExampleUser</span>' in result
    assert '<span id="password-recovery-code">12345</span>' in result


def test_set_code_in_html_with_none_html():
    # Arrange
    sender = PasswordRecoveryEmailSender()
    code = "12345"
    username = "ExampleUser"

    # Act
    result = sender._set_code_in_html(html=None, code=code, username=username)

    # Assert
    assert 'ExampleUser' in result
    assert '12345' in result
    
def test_send_email_recovery_password_with_none_html():
    sender = PasswordRecoveryEmailSender()
    env = EnvManager()
    username = "ExampleUser"
    sender_email = env.get("SENDER_EMAIL")
    password_email = env.get("PASSWORD_EMAIL")
    
    sender.send_email_recovery_password(username= username,
                                        sender_email= sender_email,
                                        password_email= password_email,
                                        receiver_email= sender_email)


def test_send_email_recovery_password_with_html():
    sender = PasswordRecoveryEmailSender()
    env = EnvManager()
    username = "ExampleUser"
    sender_email = env.get("SENDER_EMAIL")
    password_email = env.get("PASSWORD_EMAIL")
    
    sender.send_email_recovery_password(username= username,
                                        sender_email= sender_email,
                                        password_email= password_email,
                                        receiver_email= sender_email,
                                        email_template_html= """
                                        <html>
                                            <body>
                                                <p>Hola <span id="username-to-recovering-password"></span>,</p>
                                                <p>Tu código de recuperación es: <span id="password-recovery-code"></span></p>
                                            </body>
                                        </html>
                                        """)