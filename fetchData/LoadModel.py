import xlsxwriter as xls
import xlrd
import os.path
import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path


class Model(nn.Module):

    def __init__(self, input_size, hidden_size, number_layer, num_class=2):
        super().__init__()
        self.h1 = nn.Linear(input_size, hidden_size)
        self.linears = nn.ModuleList(
            [nn.Linear(hidden_size, hidden_size) for i in range(number_layer - 1)])
        self.hfinal = nn.Linear(hidden_size, num_class)

    def forward(self, x):
        x = self.h1(x)
        x = torch.tanh(x)
        for i in range(1, len(self.linears)):
            x = self.linears[i](x)
        x = self.hfinal(x)
        x = F.softmax(x, dim=1)
        return x


def loadModel(timeframe: str, delay: int) -> Model:
    path_to_pth = Path(
        "/Users/douglasbouchet/HXRO_ANN_Trader/saved_model/models/" +
        timeframe + "/" + str(delay) + ".pth")
    if (not path_to_pth.is_file()):
        print("the requested model does not exist")
        exit()
    path_to_excel = Path("/Users/douglasbouchet/HXRO_ANN_Trader/saved_model/specs/" +
                         timeframe + ".xlsx")
    if (not path_to_excel.is_file()):
        print("the requested excel does not exist")
        exit()
    op = xlrd.open_workbook(path_to_excel)
    sheets = op.sheets()
    wind_size = int(sheets[0].cell(delay, 4).value)
    n_indic = int(sheets[0].cell(delay, 5).value)
    n_hidd_layer = int(sheets[0].cell(delay, 10).value)
    input_size = n_indic * wind_size
    hidden_size = round((2/3)*input_size)
    load_model = Model(input_size, hidden_size, n_hidd_layer)
    load_checkpoint = torch.load(path_to_pth)
    load_model.load_state_dict(load_checkpoint["model_state"])
    load_model.eval()
    return load_model
