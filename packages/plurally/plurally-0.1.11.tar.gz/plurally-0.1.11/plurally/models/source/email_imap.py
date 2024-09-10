import email
import imaplib
from datetime import datetime, timezone
from email.header import decode_header
from email.utils import parseaddr

from loguru import logger
from pydantic import BaseModel, EmailStr, Field

from plurally.crypto import decrypt, encrypt
from plurally.models.node import Node


class EmailSourceIMAP(Node):
    DESC = """
    Read emails in an inbox from an IMAP server.
    Every email incoming after 'Check Emails After' will be processed by the flow.
    The incoming email will be available in the output.
    """.strip()

    class InitSchema(Node.InitSchema):
        class Config:
            json_schema_extra = {
                "description": "The inputs of this node represents the configuration for reading emails from an IMAP server.",
            }

        username: str = Field(
            title="Email", examples=["name@gmail.com"], format="email"
        )
        password: str = Field(
            title="Password", examples=["password123"], format="password"
        )
        imap_server: str = Field(
            title="IMAP Server",
            examples=["imap.gmail.com"],
            description="IMAP server address.",
        )
        port: int = Field(
            993,
            title="IMAP Port",
            examples=[993],
            description="Port for connecting to the IMAP server.",
        )
        mailbox: str = Field(
            "inbox",
            title="Mailbox",
            examples=["inbox"],
            description="The mailbox to read emails from.",
        )
        check_after: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc),
            title="Check Emails After",
            examples=["2023-08-01 00:00:00"],
            format="date-time",
            description="Only emails received after this time will be processed.",
        )

    SensitiveFields = ("username", "password", "imap_server", "check_after", "mailbox")

    class InputSchema(Node.InputSchema): ...

    class OutputSchema(BaseModel):
        class Config:
            json_schema_extra = {
                "description": "The outputs of this node represents the data associated with each incoming email.",
            }

        sender_name: str = Field(
            title="Sender Name",
            examples=["John Doe"],
            description="Name of the sender of the incoming email.",
        )
        sender_email: EmailStr = Field(
            title="Sender Email",
            description="Email address of the sender of the incoming email.",
        )
        datetime_received: datetime = Field(
            title="Datetime Received",
            examples=["2023-08-01 00:00:00"],
            format="date-time",
            description="Datetime when the incoming email was received.",
        )
        subject: str = Field(
            None,
            title="Subject",
            examples=["Hello"],
            description="Subject of the incoming email.",
        )

        content: str = Field(
            None,
            title="Body",
            examples=["Hello, World!"],
            description="Body of the incoming email.",
        )

    def __init__(
        self,
        init_inputs: InitSchema,
        is_password_encrypted: bool = False,
    ) -> None:
        super().__init__(init_inputs)
        self.username = init_inputs.username

        if is_password_encrypted:
            self.password = init_inputs.password
        else:
            self.password = encrypt(init_inputs.password)

        self.imap_server = init_inputs.imap_server
        self.port = init_inputs.port
        self.mailbox = init_inputs.mailbox
        self._server = None  # lazy init
        self.check_after = init_inputs.check_after

    @property
    def server(self):
        if self._server is None:
            self._server = self._login_server(
                self.username,
                self.password,
                self.imap_server,
                self.port,
                self.mailbox,
            )
        return self._server

    def _login_server(
        self,
        username: EmailStr,
        password: str,
        imap_server: str,
        port: int,
        mailbox: str,
    ):
        logger.debug(f"Logging into {imap_server}:{port}")
        imap = imaplib.IMAP4_SSL(imap_server, port=port)
        password = decrypt(password)
        imap.login(username, password)
        imap.select(mailbox)
        logger.debug(f"Connected successfully to {imap_server}:{port}")
        return imap

    def __call__(self):
        imap_date = self.check_after.strftime("%d-%b-%Y")  # E.g., "01-Aug-2023"
        status, messages = self.server.search(None, f"SINCE {imap_date}")
        email_ids = messages[0].split()
        logger.debug(f"Found {len(email_ids)} emails since {imap_date}")

        self.outputs = None  # Will stop flow if no new emails are found

        for email_id in email_ids:
            res, msg = self.server.fetch(email_id, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    # this is the part containing the actual email content
                    msg = email.message_from_bytes(response_part[1])
                    email_date = msg["Date"]
                    email_date_parsed = email.utils.parsedate_to_datetime(email_date)

                    if email_date_parsed > self.check_after:
                        logger.debug(f"Processing email from {email_date}")

                        if msg["Subject"]:
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(
                                    encoding if encoding else "utf-8"
                                )
                        else:
                            subject = ""

                        from_ = msg.get("From")
                        name, email_address = parseaddr(from_)

                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                        else:
                            body = msg.get_payload(decode=True).decode()

                        self.outputs = dict(
                            sender_name=name,
                            sender_email=email_address,
                            datetime_received=email_date_parsed,
                            subject=subject,
                            content=body,
                        )
                        self.check_after = email_date_parsed
                        logger.debug(
                            f"Email processed, setting check_after={self.check_after.isoformat()}"
                        )
                        return

    def serialize(self):
        payload = super().serialize()
        payload.update(
            {
                "username": self.username,
                "password": self.password,
                "imap_server": self.imap_server,
                "port": self.port,
                "mailbox": self.mailbox,
                "check_after": self.check_after.isoformat(),
            }
        )
        return payload

    @classmethod
    def _parse(cls, **kwargs):
        kwargs["check_after"] = datetime.fromisoformat(kwargs["check_after"])
        return cls(cls.InitSchema(**kwargs), is_password_encrypted=True)
