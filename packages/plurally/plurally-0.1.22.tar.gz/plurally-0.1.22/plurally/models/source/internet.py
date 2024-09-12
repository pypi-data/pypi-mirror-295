import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from plurally.models.node import Node


class InternetPage(Node):

    class InitSchema(Node.InitSchema):
        selector: str = Field(
            title="Selector",
            description="The selector to use to scrape the content",
            examples=["h1"],
        )

    class InputSchema(Node.InputSchema):
        url: str = Field(
            title="URL",
            description="The URL of the page to scrape",
            examples=["https://example.com"],
        )

    class OutputSchema(BaseModel):
        content: str = Field(
            title="Content",
            description="The content of the page",
        )

    DESC = "Scrape the content of a webpage"

    def __init__(self, init_inputs: InitSchema, outputs=None):
        self.selector = init_inputs.selector
        super().__init__(init_inputs, outputs)

    def _get_html_content(self, url):
        req = requests.get(url)
        req.raise_for_status()

        return req.text

    def forward(self, node_inputs):
        req = requests.get(node_inputs.url)
        req.raise_for_status()

        html_content = self._get_html_content(node_inputs.url)

        soup = BeautifulSoup(html_content, "html.parser")
        selected = soup.select_one(self.selector)
        if selected is None:
            self.outputs = {"content": ""}
        else:
            content = selected.get_text()
            self.outputs = {"content": content}
