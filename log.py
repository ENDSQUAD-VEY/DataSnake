__author__ = "Lucas Brabo"


######## Import de Bots deve ser realizado no começo do código ########
import os
import getpass
import sys
from datetime import datetime
#######################################################################


############## Instanciando funções globais de suporte ################
def getUser():
    #Função que retorna o nome do usuário atual
    return getpass.getuser()

def timeStamp():
    #Função que gera um TimeStamp para colocar no arquivo
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")
#######################################################################


class Log:
    def __init__(self, project, scriptName, environment):
        #Construtor padrão da classe
        self.project = project
        self.scriptName = scriptName
        self.environment = environment
        self.filePath = 'L:\\{}\\{}\\Logs\\python_log.csv'.format(project, environment)


    def openFile(self):

        """Este método tem por função instânciar um objeto de escrita.
        Verifica se o mesmo existe, se existir, apenas retorna o objeto de escrita,
        caso não exista, cria o mesmo e adiciona nome as colunas do csv"""

        testFile = os.path.exists(self.filePath)
        if testFile == True:
            f = open(self.filePath, 'a+')
            return f
        else:
            f = open(self.filePath, 'a+')
            f.write("{},{},{},{},{},{},{},{},{},{}\n".format('TIME', 'RUNNER', 'PROJECT_NAME', 'BOT_NAME', 'STATUS', 'ERROR_LINE', 'AA_DESCRIPTION', 'DEV_DESCRIPTION', 'VARIABLE', 'ENVIRONMENT'))
            return f
    
    def writeFile(self, text):

        """Este método tem por função realizar a escrita do texto
        passado como parâmetro e fechar o objeto de escrita. text é um
        parâmetro obrigatório"""

        f = self.openFile()
        f.write(text)
        f.close()
        return 0

    def logRastreio(self, devDescription, variable = 'NULL'):

        """Função para gerar log de rastreio através do método writeFile(),
        para realizar o padrão do log de rastreio. devDescription é um parâmetro obrigatório"""
        
        text = ("{},{},{},{},{},{},{},{},{},{}\n".format(timeStamp(), getUser(), self.project, self.scriptName, 'RASTREIO', 'NULL', 'NULL' ,devDescription, variable, self.environment))
        self.writeFile(text)
        return 0

    def logSucesso(self, devDescription, variable = 'NULL'):

        """Função para gerar log de Sucesso através do método writeFile(),
        para realizar o padrão do log de Sucesso. devDescription é um parâmetro obrigatório"""

        text = ("{},{},{},{},{},{},{},{},{},{}\n".format(timeStamp(), getUser(), self.project, self.scriptName, 'SUCESSO', 'NULL', 'NULL' ,devDescription, variable, self.environment))
        self.writeFile(text)
        return 0

    def logErro(self, devDescription, pythonDescription, errorLine, variable = 'NULL'):

        """Função para gerar log de Erro através do método writeFile(),
        para realizar o padrão do log de Erro. devDescription, errorLine e pythonDescriptio
        são parâmetros obrigatórios"""

        text = ("{},{},{},{},{},{},{},{},{},{}\n".format(timeStamp(), getUser(), self.project, self.scriptName, 'ERRO', errorLine, pythonDescription, devDescription, variable, self.environment))
        self.writeFile(text)
        return 0


