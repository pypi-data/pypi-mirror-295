import pandas as pd

from wiliot_tools.shipment_approval_gui.resources.config import FULL_COLUMNS, DISPLAY_COLS


class Requests:

    def __init__(self):
        self.df = None
        self.read_local_file()

    def read_local_file(self):
        try:
            self.df = pd.read_csv('data/requests.csv', index_col=0, dtype=str)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=FULL_COLUMNS)
        # self.load_df()

    def get_df(self, cols):
        return self.df[cols]

    def delete(self, request_id):
        self.df = self.df[self.df['requestId'] != request_id]

    def add_row(self, row, cols=FULL_COLUMNS):
        new_row_df = pd.DataFrame([row], columns=cols)
        self.df = pd.concat([new_row_df, self.df]).reset_index(drop=True)
        return tuple(new_row_df[DISPLAY_COLS].iloc[0])

    def process_response(self, response):
        row = []
        for col in FULL_COLUMNS:
            if col in response:
                row.append(response[col])
            elif "summaryData" in response and col in response["summaryData"]:
                row.append(response["summaryData"][col])
            elif col.endswith("otherIssuesQty") and row[-1] != "-":
                row.append(row[-7] - row[-2] - row[-4] - row[-6])
            elif col.endswith("sampleTestStatus") and row[-1] != "-":
                if "sampleTests" in response and len(response["sampleTests"]) > 0 and len([test for test in response["sampleTests"] if test['failBinStr'] == 'PASS']):
                    row.append('Passed')
                else:
                    row.append('Failed')
            elif col.endswith("Status") and row[-1] != "-":
                if row[-1] > 0:
                    row.append('Failed')
                else:
                    row.append('Passed')
            elif "sampleTest" in col and row[-1] != "-":
                res_col = col.replace("sampleTest", "")
                res_col = res_col[0].lower() + res_col[1:]
                if "sampleTests" in response and len(response["sampleTests"]) > 0 and res_col in response["sampleTests"][0]:
                    if 'Avg' in col:
                        row.append(", \n".join([str(round(test[res_col],2)) for test in response["sampleTests"]]))
                    else:
                        row.append(", \n".join([str(test[res_col]) for test in response["sampleTests"]]))
                else:
                    row.append("No Test")
            elif "commonRunNames" in response["summaryData"] and col == 'reelName':
                row.append(response["summaryData"]["commonRunNames"].split("_20")[0])
            else:
                row.append("-")
        return self.add_row(row)


    def save_data(self):
        self.df.to_csv("data/requests.csv")
