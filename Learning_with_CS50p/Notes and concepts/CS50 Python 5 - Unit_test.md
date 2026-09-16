### 1. O Conceito de Testes Automatizados (Unit Tests)

Até então, o método comum de testar um código consistia em executar o programa manualmente e digitar diferentes entradas para verificar visualmente se a saída estava correta. No entanto, a forma mais eficiente e profissional de garantir que um programa funcione é escrevendo código adicional cujo único propósito é testar o código principal.

Esse processo é conhecido como **testes unitários (unit tests)**, que consiste em testar unidades individuais do seu código — tipicamente representadas por **funções**. Isso garante mais confiança ao fazer alterações futuras e ajuda a identificar rapidamente erros que poderiam passar despercebidos.

---

### 2. O Problema das Condicionais Manuais e Casos de Borda

Considere uma função simples para calcular o quadrado de um número dentro de um arquivo chamado `calculator.py`:

```
# calculator.py
def main():
    x = int(input("Qual é o valor de x? "))
    print("x ao quadrado é", square(x))

def square(n):
    return n * n

if __name__ == "__main__":
    main()
```

*Nota: A condicional `if __name__ == "__main__":` garante que a função `main()` seja executada apenas quando rodamos o arquivo diretamente, impedindo que ela seja chamada automaticamente quando importamos as funções desse arquivo em outro script.*

Se quisermos criar um script de teste inicial sem frameworks (`test_calculator.py`), poderíamos usar estruturas condicionais simples:

```
# test_calculator.py
from calculator import square

def test_square():
    if square(2) != 4:
        print("Erro: 2 ao quadrado não resultou em 4")
    if square(3) != 9:
        print("Erro: 3 ao quadrado não resultou em 9")

def main():
    test_square()

if __name__ == "__main__":
    main()
```

#### O perigo dos casos de borda (Corner Cases)

Se houvesse um erro em nossa função e tivéssemos implementado acidentalmente `n + n` em vez de `n * n`, nosso teste para `square(2)` ainda assim passaria, pois `2 + 2` também é igual a `4`.
Isso demonstra por que é crucial testar uma variedade de **casos de borda (corner cases)**, incluindo números positivos, negativos e o zero (`0`).

---

### 3. A Palavra-chave `assert` e o Bloco `try-except`

Escrever condicionais `if` para cada teste gera muito código repetitivo. Python possui a palavra-chave **`assert`**, que serve para afirmar que uma expressão booleana é verdadeira.

- Se a expressão for **verdadeira**, o programa continua a execução normalmente sem exibir mensagens.
- Se a expressão for **falsa**, o Python interrompe o programa e dispara uma exceção chamada **`AssertionError`**.

```
# Simplificando os testes com assert
def test_square():
    assert square(2) == 4
    assert square(3) == 9
```

Como o `AssertionError` cru gera mensagens que não são muito amigáveis para o usuário no terminal, podemos capturar essa exceção usando blocos `try` e `except`:

```
def test_square():
    try:
        assert square(2) == 4
    except AssertionError:
        print("Erro: 2 ao quadrado não é 4")

    try:
        assert square(3) == 9
    except AssertionError:
        print("Erro: 3 ao quadrado não é 9")
```

Embora isso forneça mensagens de erro personalizadas, acaba criando dezenas de linhas de código de suporte (*boilerplate*) para testar uma função simples de duas linhas.

---

### 4. Automatização Profissional com `pytest`

O **`pytest`** é uma ferramenta e biblioteca de terceiros (instalada via `pip install pytest`) que automatiza a execução de testes, lidando com a captura de exceções e a formatação das mensagens de erro sem a necessidade de criarmos loops, blocos `try-except` ou mesmo uma função `main()` nos nossos arquivos de teste.

Para testar nossa calculadora usando `pytest`, o arquivo `test_calculator.py` precisa apenas das asserções diretas:

```
# test_calculator.py limpo para o pytest
from calculator import square

def test_square():
    assert square(2) == 4
    assert square(3) == 9
    assert square(-2) == 4
    assert square(-3) == 9
    assert square(0) == 0
```

#### Executando e interpretando o pytest:

No terminal, em vez de executar o interpretador Python, nós chamamos o comando do pytest indicando o arquivo de teste:
`pytest test_calculator.py`

- **Falha (`F` em vermelho):** O pytest mostra exatamente em qual linha o teste falhou e os valores reais que foram retornados versus o esperado (ex: mostrando que a função retornou `6` em vez do esperado `9`).
- **Sucesso (`.` verde):** Um ponto indica que a função de teste passou com 100% de sucesso.

#### Isolando testes para obter mais pistas

Se colocarmos todas as asserções em uma única função e a primeira falhar, o pytest interrompe a execução das seguintes, impedindo-nos de saber se os outros testes passariam. A melhor prática é dividir os testes em múltiplas funções temáticas (como positivos, negativos e zero). Assim, o pytest executará todas e fornecerá pistas melhores sobre onde o bug está localizado.

```
def test_positive():
    assert square(2) == 4
    assert square(3) == 9

def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9

def test_zero():
    assert square(0) == 0
```

---

### 5. Testando Exceções com `pytest.raises`

Podemos testar se o nosso código se comporta de maneira correta ao receber entradas inválidas (como uma string ao invés de um número), garantindo que ele dispare a exceção esperada (por exemplo, um `TypeError` no caso de tentar elevar uma string ao quadrado).

Para testar exceções com o `pytest`, importamos a biblioteca e usamos o gerenciador de contexto `with pytest.raises`:

```
import pytest
from calculator import square

def test_argument_errors():
    # Garantimos que passar "cat" para square dispara obrigatoriamente um TypeError
    with pytest.raises(TypeError):
        square("cat")
```

---

### 6. Testabilidade: Efeitos Colaterais vs. Valores de Retorno

Funções que realizam impressões de tela (`print`) em vez de retornar valores são difíceis de testar diretamente. O `print` gera um **efeito colateral** visual na tela, mas não entrega um dado palpável (retorna `None`).

#### Exemplo com efeito colateral (difícil de testar):

```
# hello.py antigo
def hello(to="world"):
    print("hello,", to)
```

Se tentarmos testar com `assert hello("David") == "hello, David"`, o teste falhará porque a função não possui a instrução `return` e, por padrão, retorna `None`.

#### Refatoração para testabilidade (melhor prática):

Para tornar o código testável, o ideal é fazer a função **retornar** o valor gerado (como uma string formatada) e deixar que a função que a chamou (geralmente a `main()`) decida se quer imprimi-lo ou não.

```
# hello.py aprimorado
def hello(to="world"):
    return f"hello, {to}"

def main():
    name = input("Qual o seu nome? ")
    print(hello(name))
```

Agora, no arquivo de testes, podemos validar os retornos facilmente:

```
# test_hello.py
from hello import hello

def test_default():
    assert hello() == "hello, world"

def test_argument():
    assert hello("David") == "hello, David"
```

---

### 7. Organizando Testes em Pastas (Pacotes)

Quando os projetos crescem, manter todos os testes no mesmo arquivo fica inviável. O `pytest` permite organizar os testes dentro de uma pasta dedicada (como `test/`).

Para que o Python e o `pytest` reconheçam uma pasta de arquivos como um pacote de módulos importáveis, devemos criar um arquivo vazio chamado **`__init__.py`** dentro dela.

A estrutura de diretórios ideal fica assim:

```
meu_projeto/
│
├── hello.py
└── test/
    ├── __init__.py (arquivo vazio)
    └── test_hello.py
```

Para rodar todos os testes contidos na pasta de uma vez só, basta executar no terminal:
`pytest test`

O `pytest` lerá a pasta inteira, executará todos os arquivos que iniciam com `test_` e fornecerá o relatório completo unificado.