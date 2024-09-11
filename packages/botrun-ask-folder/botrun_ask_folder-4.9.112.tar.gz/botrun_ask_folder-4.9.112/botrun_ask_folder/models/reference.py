from typing import List


class Reference:
    def __init__(
        self,
        file_name: str,
        file_link: str,
        page_numbers: List[int] = [],
        sheet_names: List[str] = [],
    ):
        self.file_name = file_name
        self.file_link = file_link
        self.page_numbers = page_numbers
        self.sheet_names = sheet_names

    def to_md(self):
        md = f"[{self.file_name}]({self.file_link})"
        if self.page_numbers:
            md += f" - 第 {",".join(self.page_numbers)} 頁"
        if self.sheet_names:
            md += f" - 頁籤：{",".join(self.sheet_names)}"
        return md
