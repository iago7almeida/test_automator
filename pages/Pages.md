# **Automação de Testes \- Page Objects (Sistema de Gestão Pigz)**

Este documento descreve a estrutura e o conteúdo da pasta pages, que contém os Page Objects para a automação de testes do sistema "Gestão Pigz" utilizando Python com Playwright.

## **Visão Geral**

O projeto utiliza o padrão de design **Page Object Model (POM)**. Este padrão visa criar uma abstração das páginas da interface do usuário (UI) e encapsular as interações do usuário como métodos. Isso torna os testes mais legíveis, robustos e fáceis de manter.  
**Tecnologias:**

* **Linguagem:** Python  
* **Framework de Automação:** Playwright  
* **Padrão de Design:** Page Object Model (POM)

## **Estrutura do Projeto**

A pasta pages/ contém um arquivo .py para cada página ou componente principal da aplicação.

* base\_page.py: A classe base da qual todas as outras páginas herdam.  
* login\_page.py: Gerencia a tela e o fluxo de login.  
* dashboard\_page.py: Representa o painel principal após o login, servindo como ponto de navegação.  
* client\_list\_page.py: Gerencia a lista de clientes.  
* client\_details\_page.py: Gerencia a tela de detalhes de um cliente específico.  
* new\_order\_page.py: Gerencia a criação de um "Pedido Avulso" (Delivery ou Retirada).  
* order\_sheet\_page.py: Gerencia a tela de "Comandas de Mesa", um fluxo complexo que inclui abrir mesas, adicionar pedidos, transferir, pagar e cancelar comandas.  
* tables\_page.py: Uma implementação alternativa ou anterior para interagir com a tela de mesas. **(Nota: Há sobreposição com order\_sheet\_page.py)**.  
* modal\_handler.py: Um módulo auxiliar para gerenciar modais (pop-ups) que podem aparecer de forma assíncrona.

## **Descrição dos Page Objects**

A seguir, uma descrição detalhada de cada módulo.

### **1\. base\_page.py**

É a fundação de todos os Page Objects.

* **Propósito:** Centralizar funcionalidades comuns a todas as páginas.  
* **Responsabilidades:**  
  * Fornecer métodos básicos de interação com a página, como click(), fill(), navigate() e wait\_for\_selector().  
  * Implementar lógicas de tratamento de componentes globais, como o modal "Caixa Aberto Identificado\!" através do método handle\_keep\_open\_modal\_if\_present().

### **2\. login\_page.py**

Gerencia a tela de autenticação.

* **Propósito:** Encapsular todos os elementos e ações da página de login.  
* **Responsabilidades:**  
  * Navegar para a URL de login.  
  * Preencher os campos de e-mail e senha.  
  * Clicar no botão de submissão para realizar o login.

### **3\. dashboard\_page.py**

Representa o painel principal da aplicação.

* **Propósito:** Servir como o principal hub de navegação após o login.  
* **Responsabilidades:**  
  * Navegar para as principais seções do sistema:  
    * navigate\_to\_tables(): Vai para "Mesas e Comandas".  
    * navigate\_to\_new\_order(): Vai para "Novo Pedido".  
    * navigate\_to\_clients(): Vai para a lista de "Clientes".

### **4\. client\_list\_page.py**

Gerencia a página que exibe a lista de todos os clientes cadastrados.

* **Propósito:** Abstrair interações com a tabela de clientes.  
* **Responsabilidades:**  
  * select\_first\_client(): Seleciona o primeiro cliente da lista para ver seus detalhes.  
  * A estrutura para select\_client\_by\_name() existe, mas está marcada como "não implementada com locators reais", indicando uma área para desenvolvimento futuro.

### **5\. client\_details\_page.py**

Gerencia a tela de detalhes de um cliente, que aparece após selecionar um cliente na lista.

* **Propósito:** Encapsular as ações relacionadas a um único cliente.  
* **Responsabilidades:**  
  * Receber pagamentos de dívidas (open\_receive\_payment\_modal, fill\_payment\_amount, confirm\_receive\_payment).  
  * Visualizar o extrato de transações (open\_transactions\_history).  
  * Excluir pagamentos do extrato do cliente (delete\_all\_listed\_payments).  
  * Fechar a tela de detalhes do cliente (close\_client\_area\_or\_modal).

### **6\. new\_order\_page.py**

Gerencia a criação de um pedido avulso.

* **Propósito:** Abstrair o fluxo completo de criação de um pedido que não está atrelado a uma mesa.  
* **Responsabilidades:**  
  * Selecionar um cliente para o pedido.  
  * Definir o tipo de pedido: "Retirada" (set\_order\_type\_retirada) ou "Delivery" (set\_order\_type\_delivery).  
  * Adicionar produtos ao carrinho.  
  * Avançar para a tela de pagamento e selecionar o método (Dinheiro, Pix, Cartão, Vales, etc.).  
  * Finalizar e enviar o pedido (confirm\_send\_order).

### **7\. order\_sheet\_page.py**

É uma das páginas mais complexas, gerenciando o fluxo de "Mesas e Comandas".

* **Propósito:** Orquestrar todas as operações relacionadas a uma comanda de mesa.  
* **Responsabilidades:**  
  * Abrir uma mesa e adicionar o primeiro pedido (add\_order\_to\_table).  
  * Adicionar novos pedidos a uma mesa já aberta.  
  * Cancelar uma comanda (cancel\_order\_sheet).  
  * Transferir itens ou a comanda inteira para outra mesa (transfer\_order\_sheet).  
  * Receber o pagamento da comanda (receive\_payment\_for\_table), suportando diversos métodos de pagamento, incluindo "Fiado" (OnCustomerAccount).  
  * Lidar com modais específicos, como o de pagamentos já registrados.

### **8\. tables\_page.py**

Uma página que também interage com a tela de mesas.

* **Propósito:** Similar ao order\_sheet\_page.py, parece ser uma implementação alternativa ou mais antiga para o gerenciamento de mesas.  
* **Responsabilidades:**  
  * open\_or\_add\_to\_table(): Abre ou adiciona itens a uma mesa.  
  * cancel\_order\_sheet\_for\_table(): Cancela a comanda de uma mesa.  
* **Nota:** As funcionalidades desta classe têm grande sobreposição com OrderSheetPage. Seria ideal unificar a lógica para evitar duplicidade e confusão.

### **9\. modal\_handler.py**

Um módulo auxiliar, não um Page Object.

* **Propósito:** Centralizar a lógica para detectar e interagir com modais (pop-ups) que podem aparecer em diferentes momentos da navegação.  
* **Funções:** Keep\_open, registered\_payments, orderSheet\_opened, multiple\_commands, tax\_note.  
* **Nota:** A refatoração moveu algumas dessas lógicas para métodos privados dentro das próprias classes de página (ex: \_handle\_registered\_payments\_modal em OrderSheetPage), o que é uma boa prática.

## **Conceitos e Padrões Importantes**

* **Locators:** Os seletores (majoritariamente XPaths) são centralizados como constantes de classe no topo de cada arquivo. Muitos contêm comentários como "refine-os para maior robustez", indicando que devem ser substituídos por seletores mais estáveis (como data-testid, IDs ou seletores CSS mais específicos) sempre que possível.  
* **Waits vme.sleep():** O código mistura o uso de time.sleep() com os waits explícitos do Playwright (wait\_for\_selector). A boa prática é sempre preferir waits explícitos, pois eles aguardam uma condição específica e não pausam a execução por um tempo fixo, tornando os testes mais rápidos e confiáveis.  
* **Encapsulamento:** Cada classe é responsável apenas por sua respectiva área da aplicação, seguindo o Princípio de Responsabilidade Única.

## **Sugestões de Melhoria e Refatoração**

1. **Unificar OrderSheetPage e TablesPage:** A sobreposição de funcionalidade entre essas duas classes deve ser resolvida. A lógica deve ser consolidada em uma única classe (OrderSheetPage parece ser a mais completa) para criar uma única fonte de verdade.  
2. **Substituir time.sleep():** Trocar todas as ocorrências de time.sleep() por esperas explícitas do Playwright (page.wait\_for\_selector, page.wait\_for\_load\_state, expect(locator).to\_be\_visible(), etc.).  
3. **Melhorar Locators:** Substituir XPaths frágeis e baseados em estrutura por seletores mais robustos. A melhor opção é trabalhar com a equipe de desenvolvimento para adicionar atributos de teste, como data-testid.  
4. **Remover Código Comentado:** Funcionalidades comentadas, como select\_client\_by\_name, devem ser implementadas ou removidas para manter o código limpo.  
5. **Parametrização:** Evitar valores "hardcoded" (como o valor "Porque sim" na exclusão de pagamento ou valores de pagamento fixos) nos métodos das páginas. Eles devem ser recebidos como parâmetros dos métodos de teste.

## **Como Usar**

Em um script de teste, você instancia a classe de página necessária e chama seus métodos em sequência para simular um fluxo de usuário.  
**Exemplo de um teste de criação de pedido:**

* \# Em um arquivo como tests/test\_create\_order.py

  from pages.login\_page import LoginPage  
  from pages.dashboard\_page import DashboardPage  
  from pages.new\_order\_page import NewOrderPage

  def test\_create\_new\_delivery\_order(page):  
      \# 1\. Login  
      login\_page \= LoginPage(page)  
      login\_page.navigate\_to\_login\_page()  
      login\_page.login("seu\_email@pigz.dev", "sua\_senha")

      \# 2\. Navegar para Novo Pedido  
      dashboard \= DashboardPage(page)  
      dashboard.navigate\_to\_new\_order()

      \# 3\. Criar o Pedido  
      new\_order\_page \= NewOrderPage(page)  
      new\_order\_page.select\_client\_for\_order()  
      new\_order\_page.set\_order\_type\_delivery()  
      new\_order\_page.add\_default\_product\_to\_order()  
      new\_order\_page.proceed\_to\_payment\_or\_send\_order()  
      new\_order\_page.select\_payment\_method\_single\_order("Pix")  
      new\_order\_page.confirm\_send\_order()

      \# Aqui, adicionar uma asserção para verificar o sucesso do pedido.  
