from bs4 import BeautifulSoup


class Table:
    """Provides parser and querying data logic for HTML table based on DIVs with ARIA attributes

    Refer for more: WAI-ARIA table design pattern
    https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/table/
    """

    def __init__(self, html_str):
        self.html_str = html_str
        self.soup = BeautifulSoup(self.html_str, "html.parser")

        self.cols = []
        for col in self.soup.find_all(attrs={"role": "columnheader"}):
            if col.name == "span":
                self.cols.append(col.string)

        self.rows = []
        for row in self.soup.find_all(attrs={"role": "row"}):
            values = []
            for value in row.find_all(attrs={"role": "cell"}):
                values.append(value.string)
            if row.name == "div":
                if values:
                    self.rows.append(values)

        self.rows_data = []
        for row in self.rows:
            row_data = dict(zip(self.cols, row))
            self.rows_data.append(row_data)

    def get_data(self, key_col_name: str, key_value: str, col_name: str) -> str:
        for row_data in self.rows_data:
            if row_data[key_col_name] == key_value:
                return row_data[col_name]
        raise ValueError(f"No data found with {key_col_name}={key_value}")
