from requests import Response
import re


class WResponse:

    def __init__(self, response: Response) -> None:
        self.response = response
        charset: re.Match = re.search(
            r'charset=["\']?([a-z0-9-]*)["\']?', response.text
        )
        self.response.encoding = (
            charset.group(1) if charset else response.apparent_encoding
        )

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def content(self) -> bytes:
        return self.response.content

    @property
    def text(self) -> str:
        return self.response.text

    @property
    def headers(self) -> dict:
        return self.response.headers

    @property
    def cookies(self) -> dict:
        return self.response.cookies

    @property
    def url(self) -> str:
        return self.response.url

    @property
    def encoding(self) -> str:
        return self.response.encoding

    @property
    def is_redirect(self) -> bool:
        return self.response.is_redirect

    @property
    def history(self) -> list:
        return self.response.history
