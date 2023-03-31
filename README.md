# Klotski's Implementation with Python

## Introdução
**Klotski** trata-se de um jogo de quebra-cabeças que envolve mover uma ou mais peças num tabuleiro (5x4) de forma a alcançar um objetivo. Neste jogo, o objetivo é mover a peça vermelha ao longo do tabuleiro até alcançar a sua respetiva posição final. Mais ainda, as peças podem apresentar tanto um formato como um tamanho variáveis, aumentando, assim, a quantidade de configurações possíveis para o tabuleiro.
Este jogo dispõe de vários níveis de dificuldade de forma a estimular o jogador e simultaneamente proporcionar uma experiência mais desafiante.

## Pré-Requesitos
De forma a compilar e executar o programa são necessários vários pré-requesitos:
- Instalação da Livraria **[Pygame](https://www.pygame.org/wiki/GettingStarted)**
- Versão do Python compatível com a livraria **Pygame**

## Compilação e Execução
De forma a compilar e executar o programa, basta executar o seguinte comando no seu terminal: 

``` python3 -m Game.py ```

## Interface Gráfica
A Implementação em Python do **Jogo *Klotski*** dispõe de uma Interface Gráfica.
Esta apresenta vários menus, níveis e configurações modificáveis tendo em atenção o interesse do utilizador.

### Menu's
Existem 3 Menus:
- ***Main Menu*** (Ecrã Inicial do Jogo)
- ***Modes Menu*** (Permite a escolha entre duas dificuldades de Níveis: ***Easy*** e ***Hard***)
- ***Options Menu*** (Contém informações sobre o jogo e de possíveis alterações dos algoritmos a testar)

### Níveis
Os Níveís para além de poderem ser resolvidos por parte do utilizador, estes apresentam outras funcionalidades:
- Regressar à escolha de nível através do butão ***Home*** (**botão 1**).
- Dar ***reset*** ao nível (isto é, voltar à configuração inicial do nível) pressionado o respetivo botão (**botão 2**).
- Resolução do Nível com recurso a um Algoritmo de Pesquisa (**A* Algorithm**) através do **botão 3**.
- Visualizar a Eficiência de vários Algoritmos de Pesquisa (através do **tempo**, **quantidade de nós explorados** e de **passos até alcançar a solução**) na resolução do nível atual. Para tal, bastará pressionar o **botão 4**.

<div align="center">
    <img src="/Images_Read_Me/Level_Buttons.png">
</div>
