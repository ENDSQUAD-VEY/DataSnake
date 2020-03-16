# DataSnake

Aplicação responsável por realizar o tratamento de dados oriundas de uma tabela temporária no banco de dados. 
Após o tratamento realizado com sucesso, os dados são reinseridos em outra tabela do banco de dados, 
de forma mais entendível pelo robô que fará uso dos dados.


/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\ Module - Log.py /*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\

Módulo responsável por realizar todo o processo de log de execução da aplicação. Utiliza um arquivo com extensão ".csv" para guardar 
todas as informações de rastreio, erro e sucesso de execução.


/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\ Module - END.py /*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\

Módulo responsável por guardar todos os métodos que serão usados durante a execução principal da aplicação. 
Durante as execuções dos métodos executados, há também funções da classe "Log.py" para manter a rastreabilidade de rastreio, sucesso e erro.

/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\ Module - main.py /*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\

Módulo principal da aplicação. Responsável por pegar todos os dados não estruturados de uma tabela do banco de dados toda execução
de forma estruturada, executando os métodos do módulo "END.py" da forma correta e sequenciada.


