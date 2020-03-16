import sys
import END
import log
import json


cursor = END.connectDataBase()
cursorDelete = END.connectDataBase()
cursor.execute("SELECT * from [dbo].[END_Temp]")
row = cursor.fetchone()
diretorio = "L:\\END\\PRD\\Files\\Python_END\\teste.csv"


while row:
    Remark, MatAprovAlt, Produto, MatAprov, Observacao, MotivoDaOrdem, EmissorDaOrdem, ValorCondicao, PrazoPag, CodigoMaterial, Quantidade, Centro, Email, AreaVenda, CanalDistrib  = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    Remark = Remark + END.convertToArray(row.Remark)
    MatAprovAlt = MatAprovAlt + END.convertToArray(row.MatAprovAlt)
    Produto = Produto + END.convertToArray(row.Produto)
    MatAprov = MatAprov + END.convertToArray(row.MatAprov)
    Observacao = Observacao + END.convertToArray(row.Observacao)
    MotivoDaOrdem = MotivoDaOrdem + END.convertToArray(row.MotivoDaOrdem)
    EmissorDaOrdem = EmissorDaOrdem + END.convertToArray(row.EmissorDaOrdem)
    ValorCondicao =  ValorCondicao + END.convertToArray(row.ValorCondicao)
    PrazoPag = PrazoPag + END.convertToArray(row.PrazoPag)
    CodigoMaterial = CodigoMaterial + END.convertToArray(row.CodigoMaterial)
    Quantidade = Quantidade + END.convertToArray(row.Quantidade)
    Centro = Centro + END.convertToArray(row.Centro)
    Email = Email + END.convertToArray(row.Email)
    AreaVenda = AreaVenda + END.convertToArray(row.AreaVenda)
    CanalDistrib = CanalDistrib + END.convertToArray(row.CanalDistrib)
    identity = row.ID
    
    row = cursor.fetchone()

    json2 = {"Remark": Remark, "MatAprovAlt": MatAprovAlt, "Produto": Produto, "MatAprov": MatAprov,
            "Observacao": Observacao, "MotivoDaOrdem": MotivoDaOrdem, "EmissorDaOrdem": EmissorDaOrdem,
            "ValorCondicao": ValorCondicao, "PrazoPag": PrazoPag, "CodigoMaterial": CodigoMaterial,
            "Quantidade": Quantidade, "Centro": Centro, "Email": Email, "AreaVenda": AreaVenda, "CanalDistrib": CanalDistrib
            }
    END.cleanJson(json2)
    END.replicateEmail(json2, "Remark", "Email")
    END.writeToCsv(diretorio, json2)
    cursorDelete.execute("DELETE from [dbo].[END_Temp] where ID = {}".format(identity))
    



END.csvToDataBase(diretorio, "END_DB")


