import email
import imaplib
import re
from datetime import datetime, timedelta, timezone
from email.header import decode_header
from email.utils import parseaddr

from loguru import logger
from pydantic import BaseModel, EmailStr, Field, model_validator

from plurally.crypto import decrypt, encrypt
from plurally.models.misc import Table
from plurally.models.node import Node


def decode_body(part):
    charset = part.get_content_charset() or "utf-8"
    try:
        return part.get_payload(decode=True).decode(charset)
    except UnicodeDecodeError:
        return part.get_payload(decode=True).decode("iso-8859-1")
    except Exception as e:
        logger.error(f"Error decoding email body with charset {charset}")
        raise e


class EmailSchema(BaseModel):

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


class EmailIMAPBase(Node):

    SensitiveFields = ("username", "password", "imap_server", "mailbox")

    class InitSchema(Node.InitSchema):
        class Config:
            json_schema_extra = {
                "description": "The inputs of this block represents the configuration for reading emails from an IMAP server.",
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

    def serialize(self):
        payload = super().serialize()
        payload.update(
            {
                "username": self.username,
                "password": self.password,
                "imap_server": self.imap_server,
                "port": self.port,
                "mailbox": self.mailbox,
            }
        )
        return payload

    @classmethod
    def _parse(cls, **kwargs):
        return cls(cls.InitSchema(**kwargs), is_password_encrypted=True)

    def _parse_email(self, msg, msg_id):
        # Check if the email has been read (based on the \Seen flag)
        status, flags_data = self.server.fetch(msg_id, "(FLAGS)")
        flags = flags_data[0].decode("utf-8")
        is_seen = "\\Seen" in flags

        if msg["Subject"]:
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
        else:
            subject = ""

        from_ = msg.get("From")
        name, email_address = parseaddr(from_)

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = decode_body(part)
        else:
            body = decode_body(msg)

        if True:
            # Remove any prefix quotes from the email body
            body = re.sub(r"(?:> ?)*", "", body).strip()

        return {
            "subject": subject,
            "sender_name": name,
            "sender_email": email_address,
            "body": body,
            "seen": is_seen,
        }


class EmailSourceIMAP(EmailIMAPBase):
    DESC = """
    Read emails in a mailbox from an IMAP server.
    The incoming email will be available in the output.
    """.strip()

    class InitSchema(EmailIMAPBase.InitSchema):
        limit: int = Field(
            default_factory=lambda: 1000000,
            title="Max Emails",
            examples=[1000000],
            description="The maximum number of emails to process.",
        )

    class InputSchema(Node.InputSchema):

        range_start: datetime = Field(
            title="Start Date",
            examples=["2023-08-01 00:00:00"],
            format="date-time",
            description="Only emails received after this date will be processed.",
        )

        range_end: datetime = Field(
            default_factory=lambda: None,
            title="End Date",
            examples=["2023-08-01 00:00:00"],
            format="date-time",
            description="Only emails received before this data will be processed. If not provided, all emails after 'Start Date' will be processed.",
        )

        @model_validator(mode="after")
        def ckeck_model(cls, schema):
            range_start = schema.range_start

            assert range_start, "Start date is required"
            if range_start.tzinfo:
                range_start = range_start.astimezone(timezone.utc).replace(tzinfo=None)

            range_end = schema.range_end
            if range_end:
                if range_end.tzinfo:
                    range_end = range_end.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                range_end = datetime.now(tz=timezone.utc).replace(tzinfo=None)

            if range_start > range_end:
                raise ValueError(
                    f"End date must be after start date, got {range_start} and {range_end}"
                )

            schema.range_start = range_start
            schema.range_end = range_end
            return schema

    class OutputSchema(BaseModel):
        emails: Table = Field(
            title="Emails",
            description="The emails read from the mailbox, columns will be 'sender_name', 'sender_email', 'datetime_received', 'subject', 'body', 'seen'.",
        )

    def __init__(self, init_inputs: InitSchema, is_password_encrypted: bool = False):
        self.limit = init_inputs.limit
        super().__init__(init_inputs, is_password_encrypted=is_password_encrypted)

    def serialize(self):
        return super().serialize() | {
            "limit": self.limit,
        }

    def forward(self, node_input: InputSchema):
        imap_date_start = node_input.range_start.strftime(
            "%d-%b-%Y"
        )  # E.g., "01-Aug-2023"
        imap_date_end = (node_input.range_end + timedelta(days=1)).strftime("%d-%b-%Y")

        status, messages = self.server.search(
            None, f"SINCE {imap_date_start} BEFORE {imap_date_end}"
        )
        email_ids = messages[0].split()
        logger.debug(
            f"Found {len(email_ids)} emails between {imap_date_start} and {imap_date_end}"
        )
        emails = []
        for email_id in email_ids:
            res, msg = self.server.fetch(email_id, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    # this is the part containing the actual email content
                    msg = email.message_from_bytes(response_part[1])
                    email_date = msg["Date"]
                    email_date_parsed = email.utils.parsedate_to_datetime(email_date)

                    if email_date_parsed.tzinfo:
                        email_date_parsed = email_date_parsed.astimezone(
                            timezone.utc
                        ).replace(tzinfo=None)

                    if (
                        email_date_parsed > node_input.range_start
                        and email_date_parsed < node_input.range_end
                    ):
                        logger.debug(f"Processing email from {email_date}")
                        email_data = self._parse_email(msg, email_id)
                        email_data["datetime_received"] = email_date_parsed
                        emails.append(email_data)
                        if self.limit and len(emails) >= self.limit:
                            logger.debug("Limit reached, stopping processing")
                            break
                    else:
                        logger.debug(
                            f"Skipping email from {email_date} ({email_date_parsed}), not in range {node_input.range_start} - {node_input.range_end}"
                        )

        logger.debug(f"Processed {len(emails)} emails")
        self.outputs = {"emails": Table(data=emails)}


class NewEmail(EmailIMAPBase):
    DESC = """
    Read emails in an inbox from an IMAP server.
    Every email incoming after 'Check Emails After' will be processed by the flow.
    The incoming email will be available in the output.
    """.strip()

    class InitSchema(EmailIMAPBase.InitSchema):

        check_after: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc),
            title="Check Emails After",
            examples=["2023-08-01 00:00:00"],
            format="date-time",
            description="Only emails received after this time will be processed.",
        )

    SensitiveFields = (*EmailIMAPBase.SensitiveFields, "mailbox")

    class InputSchema(Node.InputSchema): ...

    class OutputSchema(EmailSchema):
        class Config:
            json_schema_extra = {
                "description": "The outputs of this block represents the data associated with each incoming email.",
            }

    def __init__(
        self,
        init_inputs: InitSchema,
        is_password_encrypted: bool = False,
    ) -> None:
        self.check_after = init_inputs.check_after
        super().__init__(init_inputs, is_password_encrypted=is_password_encrypted)

    def forward(self, _: InputSchema):
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
                                    body = decode_body(part)
                        else:
                            body = decode_body(msg)

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
                "check_after": self.check_after.isoformat(),
            }
        )
        return payload

    @classmethod
    def _parse(cls, **kwargs):
        kwargs["check_after"] = datetime.fromisoformat(kwargs["check_after"])
        return cls(cls.InitSchema(**kwargs), is_password_encrypted=True)
