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
        ref_name = self.file_name
        if self.page_numbers and len(self.page_numbers) > 0:
            pages = ", ".join([str(page) for page in self.page_numbers])
            ref_name += f" - 第 {pages} 頁"
        elif self.sheet_names and len(self.sheet_names) > 0:
            sheets = ", ".join(self.sheet_names)
            ref_name += f" - 頁籤：{sheets}"
        md = f"[{ref_name}]({self.file_link})"
        return md
