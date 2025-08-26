# **Guia de Execução dos Testes de Automação**

Este documento detalha como configurar o ambiente e executar a suíte de testes automatizados para o sistema "Gestão Pigz" utilizando Pytest e Playwright.

## **Visão Geral da Estrutura de Testes**

Os testes estão localizados na pasta tests/ e seguem as convenções do Pytest.

* conftest.py: Arquivo de configuração central do Pytest. Ele define as *fixtures* que preparam o ambiente para cada teste, como a inicialização do navegador e a criação de uma nova página.  
* test\_\*.py: Arquivos que contêm os casos de teste. Cada arquivo é focado em uma funcionalidade específica da aplicação:  
  * test\_table\_operations.py: Testa as operações em mesas (criar pedido, cancelar, transferir, pagar).  
  * test\_single\_orders.py: Testa a criação de pedidos avulsos (Retirada, Delivery, e com vários métodos de pagamento).  
  * test\_client\_payments.py: Testa os fluxos de pagamento e exclusão de pagamentos na tela de detalhes do cliente.  
  * test\_main\_flow.py: Um script de fluxo principal que parece ser para uma execução ponta-a-ponta, mas não segue o padrão Pytest para descoberta automática de testes.

## **Pré-requisitos**

Antes de executar os testes, certifique-se de que você tem o seguinte instalado:

1. **Python** (versão 3.8 ou superior).  
2. **Pip** (gerenciador de pacotes do Python).  
3. As dependências do projeto. Se você tiver um arquivo requirements.txt, instale-as com:  
   pip install \-r requirements.txt

   Caso contrário, instale as bibliotecas necessárias manualmente:  
   pip install pytest playwright

4. **Instalar os navegadores do Playwright**:  
   pip playwright install

## **Configuração do Ambiente (conftest.py)**

O arquivo conftest.py é fundamental para a execução dos testes. Ele automatiza a preparação do ambiente:

* **browser fixture**: Inicia uma instância do navegador Chromium antes do início da sessão de testes e a fecha no final. Por padrão, está configurada para rodar em modo **headed** (headless=False), o que significa que você verá a janela do navegador abrir e os testes serem executados.  
* **page fixture**: Cria uma nova página (aba) para cada função de teste. Isso garante que os testes sejam isolados e não interfiram uns com os outros. O zoom da página é ajustado para 80% no início de cada teste.

## **Como Executar os Testes**

Abra o terminal na pasta raiz do seu projeto e utilize os seguintes comandos:

### **1\. Executar Todos os Testes**

Para rodar todos os arquivos de teste (test\_\*.py) na pasta tests/, use o comando básico do Pytest. O Pytest irá descobrir e executar todos os testes automaticamente.  
pytest

Adicione \-v (verbose) para ver mais detalhes sobre cada teste executado:  
pytest \-v

### **2\. Executar um Arquivo de Teste Específico**

Se você quiser rodar os testes de apenas um arquivo, especifique o caminho para ele.  
\# Exemplo para rodar apenas os testes de pedidos avulsos  
pytest tests/test\_single\_orders.py

\# Exemplo para rodar apenas os testes de operações em mesas  
pytest tests/test\_table\_operations.py

### **3\. Executar Testes por Marcador (-m)**

Os testes foram organizados com marcadores (markers) para permitir a execução de grupos de testes relacionados a uma funcionalidade.

* @pytest.mark.single\_orders: Para testes de pedidos avulsos.  
* @pytest.mark.client\_payments: Para testes de pagamento de cliente.

Para executar um grupo específico, use a flag \-m seguida do nome do marcador.  
\# Executar apenas os testes de pedidos avulsos  
pytest \-m single\_orders

\# Executar apenas os testes de pagamento de cliente  
pytest \-m client\_payments

### **4\. Executar um Teste Específico por Nome (-k)**

Use a flag \-k para executar testes cujos nomes contenham uma determinada expressão. Isso é útil para rodar um único teste ou um pequeno subconjunto de testes.  
\# Executar o teste que cria um pedido para delivery  
pytest \-k "test\_create\_single\_order\_delivery"

\# Executar todos os testes relacionados a cancelamento  
pytest \-k "cancel"

\# Executar um teste parametrizado específico (ex: com pagamento em Dinheiro)  
pytest \-k "test\_create\_single\_order\_with\_payment and Cash"

### **5\. Opções Adicionais**

* **Executar em Modo Headless**: Para rodar os testes sem abrir a interface gráfica do navegador (ideal para ambientes de integração contínua), edite o arquivo conftest.py e mude headless=False para headless=True.  
  \# Em conftest.py  
  browser \= playwright\_instance.chromium.launch(headless=True, channel="chrome", args=\["--start-maximized"\])

* **Parar na Primeira Falha**: Se você quiser que a suíte de testes pare imediatamente após a primeira falha, use a flag \-x.  
  pytest \-x

### **Nota sobre test\_main\_flow.py**

O arquivo test\_main\_flow.py está estruturado como um script Python procedural e não como um conjunto de casos de teste do Pytest. Portanto, ele não será executado com o comando pytest. Para executá-lo, você deve chamá-lo diretamente com o Python:  
python tests/test\_main\_flow.py  
