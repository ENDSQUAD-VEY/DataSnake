__author__ = "Lucas Brabo"
__credits__ = ["Gabriel Oliveira", "Victor Maller"]

#Funcionalidade: Realizar o tratamento de dados recebidos via JSON do projeto END

#----------------------------------------------------------------------------------------#
import log
import os
import sys
import pandas as pd
import pyodbc
import csv
#----------------------------------------------------------------------------------------#

#Instanciando variáveis
ambiente = 'PRD'
errorLine = sys.exc_info()


#Instanciando objeto da classe Log
log = log.Log('END', os.path.basename(__file__), ambiente)


def removeBreakLine(json):
    #Fucionalidade: Receber um JSON agrupado por \n e splitar em um array

    log.logRastreio('removeBreakLine: Splitando JSON a partir da quebra de linha')
    try:
        for key in json:
            json[key] = json[key].split('\n')
        log.logSucesso('removeBreakLine: JSON splitado com sucesso')

    except Exception as errorDescription:
        log.logErro('removeBreakLine: O robô não conseguiu splitar o json a partir da quebra de linha', errorDescription, errorLine)


def convertToNull(json):
    #Fucionalidade: Receber um JSON splitado em array, pegar os valores vazios destes arrays e substituir por null
    
    log.logRastreio('convertToNull: Começando a varrer os arrays presentes no json para substituir vazio por null')
    try:
        for value in json.values():
            for item in range(len(value)):
                if value[item] == '':
                    value[item] = 'null'
        log.logSucesso('convertToNull: Substituições foram realizadas com sucesso nos arrays')

    except Exception as errorDescription:
        log.logErro('convertToNull: O robô não conseguiu realizar a limpeza do array no json', errorDescription, errorLine)


def cleanJson(json):
    #Fucionalidade: Receber um JSON splitado em array, e tratar utilizando as funções chamadas
    log.logRastreio('cleanJson: Chamando a função removeBreakLine')
    try:
        removeBreakLine(json)
    except Exception as errorDescription:
         log.logErro('cleanJson: Não conseguiu realizar a chamada da função removeBreakLine', errorDescription, errorLine)
    
    log.logRastreio('cleanJson: Chamando a função convertToNull')
    try:
        convertToNull(json)
    except Exception as errorDescription:
        log.logErro('cleanJson: Não conseguiu realizar a chamada da função convertToNull', errorDescription, errorLine)
    


def lenghtValues(dicionario, campoReferencia):
    #Esta função retorna o tamanho de um valor do dicionário
    log.logRastreio('lenghtValues: Começando a função lenghtValues')
    try:
        f = len(dicionario[campoReferencia])
        log.logSucesso('lenghtValues: Tamanho do array pego com sucesso')
        return f
    except Exception as errorDescription:
        log.logErro('lenghtValues: Não conseguiu realizar o processamento da função len', errorDescription, errorLine)


def replicateEmail(dicionario, campoReferencia, campoReplicado):
    log.logRastreio('replicateEmail: chamando a função lenghtValues')
    dicSize = lenghtValues(dicionario, campoReferencia) - 1
    log.logRastreio('replicateEmail: Começando a replicação dos dados no Array')
    try:
        for i in range(dicSize):
            dicionario[campoReplicado].append(dicionario[campoReplicado][0])
        log.logSucesso('replicateEmail: Dados replicados com sucesso')
    except Exception as errorDescription:
        log.logErro('replicateEmail: Não conseguiu realizar a replicação de dados no Array', errorDescription, errorLine)


def writeToCsv(fileName, dicionario, Error_DateTime , Email2):
    #Esta função utiliza a biblioteca pandas para criar uma DataFrame a partir do dicionário e converter isso em csv
    log.logRastreio('writeToCsv: Começando a criação do DataFrame')
    #Realiza a criação do DataFrame a partir do dicionário
    try:
        df = pd.DataFrame(dicionario)
        log.logSucesso('writeToCsv: DataFrame criado com sucesso')
    except Exception as errorDescription:
        log.logErro('writeToCsv: Não conseguiu realizar a criação do DataFrame', errorDescription, errorLine)
        errodescript = 'writeToCsv: Não conseguiu realizar a criação do DataFrame'
        InsertIntoErrorTable(errodescript,Error_DateTime , Email2)
        return 1

    #Realiza a replicação dos dados a partir do DataFrame criado
    log.logRastreio('writeToCsv: Começando a replicar os dados do DataFrame para o csv')
    try:
        testFile = os.path.exists(fileName)
        if testFile == True:
            log.logRastreio('writeToCsv: Arquivo csv já existe. Realizando o append')
            df.to_csv(fileName, sep = ',', mode='a' ,index = False, header=False)
        else:
            log.logRastreio('writeToCsv: Arquivo csv não existe. Realizando criação e gravação dos dados')
            df.to_csv(fileName, sep = ',', mode='a' ,index = False)
        log.logSucesso('writeToCsv: Replicação dos dados realizada com sucesso')  
        return 0
    except Exception as errorDescription:
        log.logErro('writeToCsv: Não conseguiu realizar a replicação do DataFrame para o csv', errorDescription, errorLine)
        errodescript = 'Não conseguiu realizar a replicação do DataFrame para o csv'
        InsertIntoErrorTable(errodescript,Error_DateTime , Email2)
        return 1
 


def connectDataBase():
    #Esta função tem por finalidade conectar com o banco de dados
    log.logRastreio('connectDataBase: Conectando ao banco de dados')
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=rpasupport.database.windows.net;DATABASE=RPASUPPORT;UID=adminvale;PWD=Vale@12345678', autocommit = True)
        cursor = connection.cursor()
        log.logSucesso('connectDataBase: Conexão com o banco realizada com sucesso')
        return cursor
    except Exception as errorDescription:
        log.logErro('connectDataBase: Não conseguiu realizar a conexão com o banco', errorDescription, errorLine)
        return 1


def InsertIntoErrorTable(errorDescription, Error_DateTime, Email):
    #Esta funcao tem a funcionalidade de inserir as exceptions na tabela de erro
    Error_DateTime = Error_DateTime
    log.logRastreio('InsertIntoErrorTable: Iniciando insersao da excessao na tabela de erro')
    cursor = connectDataBase()
    log.logRastreio('InsertIntoErrorTable: Buscando email do solicitante')
    emailtest = Email
    #Update da tabela de erro
    error_datetime = Error_DateTime
    descricaoerro = errorDescription 
    params = [descricaoerro, emailtest, error_datetime]
    log.logRastreio('InsertIntoErrorTable: Email do solicitante:', emailtest)
    log.logRastreio('InsertIntoErrorTable: Realizando update de ERRO')
    stmt = ("UPDATE END_ERROR_FORM SET Status_Python = 'ERRO', Error_Description = ? WHERE Email_Requester = ? AND Error_DateTime = ?")
    cursor.execute(stmt, params)
    
    return 0

def convertToArray(param):
    #COnverte dados para array já tratado
    log.logRastreio('convertToArray: Convertendo dados para array. Dados: {}'.format(param))
    array = []
    array.append(param)
    try:
        for i in array:
            arrayFinal = i.split('\n') 
        log.logSucesso('convertoToArray: Array tranformado com sucesso')
        return arrayFinal
    except Exception as errorDescription:
        log.logErro('convertToArray: Não conseguiu realizar a conversão do Array', errorDescription, errorLine)
        return 1

def csvToDataBase(fileName, tableName, Error_DateTime, Email2):
    #Funcionalidade: inserir os dados do csv passado como parâmetro para o banco de dados
    log.logRastreio('csvToDataBase: Começando a inserir os dados do CSV na base. Dados: {}'.format(fileName))
    cursor = connectDataBase()
    try:
        #Abrindo arquivo CSV
        with open(fileName) as csvfile:
            csvData = csv.reader(csvfile, delimiter=',')
            count = 1
            #iterando no CSV para pegar o dados
            for row in csvData:
                Remark = row[0]
                MatAprovAlt = row[1]
                Produto = row[2]
                MatAprov = row[3]
                Observacao = row[4]
                MotivoDaOrdem = row[5]
                EmissorDaOrdem = row[6]
                ValorCondicao = row[7]
                PrazoPag = row[8]
                CodigoMaterial = row[9]
                Quantidade = row[10]
                Centro = row[11]
                Email = row[12]
                AreaVenda = row[13]
                CanalDistrib = row[14]
                FormaPag = row[15]
                if count == 1:
                    count = count + 1
                    continue
                
                #Montando o insert
                qry = '''INSERT INTO {}(Remark,Matricula_do_Aprovador_Alternativo,Produto,Matricula_do_Aprovador,Observacao_da_Aprovacao,Motivo_da_Ordem,
                Emissor_da_Ordem,Valor_Condicao,Prazo_de_Pagamento,Codigo_do_Material,Quantidade,Centro,Email_do_Solicitante,Area_de_Vendas,Canal_de_Distribuicao, Forma_de_Pagamento) 
                values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(tableName,Remark,MatAprovAlt,
                Produto,MatAprov,Observacao,MotivoDaOrdem,EmissorDaOrdem,ValorCondicao,PrazoPag,CodigoMaterial,Quantidade,
                Centro,Email,AreaVenda,CanalDistrib,FormaPag)

                #Realizando o insert no banco
                cursor.execute(qry)
        os.remove(fileName)
        log.logSucesso('csvToDataBase: Dados inserios com sucesso no banco de dados')

    except Exception as errorDescription:
        log.logErro('csvToDataBase: Não conseguiu inserir os dados no banco', errorDescription, errorLine)
        Error_DateTime = Error_DateTime
        errodescript = 'Não conseguiu inserir os dados no banco'
        InsertIntoErrorTable(errodescript, Error_DateTime, Email2)
        return 1
            
