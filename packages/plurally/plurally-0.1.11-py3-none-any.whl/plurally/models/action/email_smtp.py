import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger
from pydantic import BaseModel, EmailStr, Field

from plurally.crypto import decrypt, encrypt
from plurally.models.node import Node


class SendEmailSMTP(Node):

    class InitSchema(Node.InitSchema):
        username: str = Field(
            title="Email",
            examples=["myname@gmail.com"],
            format="email",
            description="The email address to send emails from.",
        )
        password: str = Field(
            title="Password",
            format="password",
            description="The password for the email address.",
        )
        smtp_server: str = Field(
            title="SMTP Server",
            description="The SMTP server's address",
            examples=["smtp.gmail.com"],
        )
        fullname: str = Field(
            "",
            title="Full name",
            description="The name to send emails from.",
            examples=["My Name"],
        )
        port: int = Field(
            587,
            title="Port",
            description="The port to connect to the SMTP server.",
            examples=[587],
        )

    SensitiveFields = ("username", "password", "smtp_server", "fullname")

    class InputSchema(Node.InputSchema):
        email_address: EmailStr
        subject: str = ""
        body: str = ""

    class OutputSchema(BaseModel): ...

    def __init__(
        self,
        init_inputs: InitSchema,
        is_password_encrypted: bool = False,
    ):
        super().__init__(init_inputs)
        self.username = init_inputs.username
        self.fullname = init_inputs.fullname

        if is_password_encrypted:
            self.password = init_inputs.password
        else:
            self.password = encrypt(init_inputs.password)

        self.smtp_server = init_inputs.smtp_server
        self.port = init_inputs.port
        self._server = None  # lazy init

    @property
    def from_email(self):
        return f"{self.fullname} <{self.username}>" if self.fullname else self.username

    def _login_server(self, username: EmailStr, password: str, smtp_server, port):
        logger.debug(f"Logging to {smtp_server}:{port}")
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        password = decrypt(password)
        server.login(username, password)
        logger.debug(f"Connected successfully to {smtp_server}:{port}")
        return server

    @property
    def server(self):
        if self._server is None:
            self._server = self._login_server(
                self.username, self.password, self.smtp_server, self.port
            )
        return self._server

    def forward(self, node_input: InputSchema):
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = node_input.email_address
        msg["Subject"] = node_input.subject

        # Attach the plain text body to the email
        msg.attach(MIMEText(node_input.body, "plain"))
        self.server.sendmail(
            self.from_email,
            node_input.email_address,
            msg.as_string(),
        )
        logger.debug(f"Email sent successfully from {self.from_email}")

    def serialize(self):
        payload = super().serialize()
        payload.update(
            {
                "username": self.username,
                "smtp_server": self.smtp_server,
                "port": self.port,
                "fullname": self.fullname,
                "password": self.password,
            }
        )
        return payload

    @classmethod
    def _parse(cls, **kwargs):
        return cls(cls.InitSchema(**kwargs), is_password_encrypted=True)
