### O que é uma Expressão Regular (Regex)?

Uma **expressão regular** (ou *regex*) é essencialmente um **padrão** usado na programação para verificar se um conjunto de dados (normalmente entradas de usuários) corresponde a um formato esperado. Elas são amplamente utilizadas para:

- **Validar dados**: Verificar se o que foi digitado é realmente um e-mail válido, um telefone, etc.
- **Limpar dados**: Padronizar e corrigir dados inconsistentes ou desorganizados gerados por humanos.
- **Extrair dados**: Isolar partes específicas de uma string maior de forma automatizada.

---

### 2. O Problema da Validação Manual

Antes de usar regex, o professor demonstra como validar um e-mail de forma convencional em um arquivo chamado `validate.py`. Usando métodos básicos de strings (`in`, `.strip()`, `.split()`), o código rapidamente se torna longo, confuso e frágil:

```
# Validação manual e frágil
email = input("Qual o seu email? ").strip()

if "@" in email and "." in email:
    username, domain = email.split("@")
    if username and domain.endswith(".edu"):
        print("Válido")
    else:
        print("Inválido")
else:
    print("Inválido")
```

Embora esse código pareça correto, ele aceita entradas absurdas como `"@.edu"` ou `"meuemail@.edu"`. Para validar regras complexas de forma limpa e robusta, recorre-se ao módulo nativo **`re`**.

---

### 3. O Módulo `re` e o Vocabulário de Símbolos

Para iniciar o uso de expressões regulares em Python, importa-se o módulo `re` e utiliza-se a função **`re.search(padrão, string, flags=0)`**, que busca por um padrão específico dentro de uma string.

Para construir esses padrões, utiliza-se um vocabulário de símbolos especiais (*meta-caracteres*):

- **`.` (ponto)**: Corresponde a qualquer caractere, exceto uma quebra de linha.
- **(asterisco)**: Indica **zero ou mais** repetições do caractere anterior.
- **`+` (mais)**: Indica **uma ou mais** repetições do caractere anterior (garante que o campo não esteja vazio).
- **`?` (ponto de interrogação)**: Indica **zero ou uma** repetição, tornando o caractere ou grupo anterior **opcional**.
- **`{m}`**: Exige exatamente `m` repetições.
- **`{m,n}`**: Permite uma faixa de `m` a `n` repetições.

---

### 4. Caracteres de Escape e Strings Cruas (Raw Strings)

Como o caractere `.` (ponto) tem um significado especial em regex (qualquer caractere), surge um problema ao tentar validar um ponto literal em um e-mail (como o `.` de `.edu`).

- **Escape (`\`)**: Para dizer ao interpretador de regex que queremos um ponto literal, devemos "escapá-lo" usando uma barra invertida: `\.`.
- **Raw Strings (`r"..."`)**: No Python, a barra invertida também inicia sequências de escape normais (como `\n` para quebra de linha). Para evitar que o Python confunda os escapes da regex com comandos do próprio Python, sempre definimos padrões regex usando o prefixo `r` antes das aspas, criando uma *raw string* (string crua).

```
import re
email = input("Email: ").strip()

# Procura por um ou mais caracteres, um "@", um ou mais caracteres e um ".edu" literal
if re.search(r".+@.+\.edu", email):
    print("Válido")
```

---

### 5. Âncoras de Início (`^`) e Fim (`$`)

O método `re.search` busca o padrão em **qualquer lugar** da string. Isso significa que a frase *"Meu e-mail é malan@harvard.edu."* seria considerada válida pelo código acima. Para restringir a busca de modo que a entrada corresponda *apenas* e *exatamente* ao padrão, usamos **âncoras**:

- **`^` (circunflexo)**: Força a correspondência a começar no **início** da string.
- **`$` (cifrão)**: Força a correspondência a terminar no **fim** da string.

```
# Agora a string inteira precisa ser exatamente o formato do e-mail
if re.search(r"^.+@.+\.edu$", email):
```

---

### 6. Conjuntos de Caracteres, Intervalos e Atalhos (Classes)

Para limitar quais caracteres são permitidos (por exemplo, impedir que o usuário digite múltiplos `@` na mesma entrada), utilizamos colchetes `[...]`.

#### Conjuntos e Complementos

- **`[^...]`**: O circunflexo *dentro* de colchetes funciona como o operador de **negação/complemento**, indicando "qualquer caractere, exceto os listados".
    - `[^@]+` significa "um ou mais caracteres que **não** sejam `@`".
- **Intervalos `[a-zA-Z0-9]`**: Dentro dos colchetes, podemos definir intervalos usando hífens para economizar digitação.
    - `[a-zA-Z0-9_]` aceita qualquer letra maiúscula ou minúscula, números e sublinhados.

#### Classes de Caracteres Embutidas (Atalhos)

Para simplificar a escrita de intervalos comuns, existem atalhos pré-definidos:

- **`\w`**: Um caractere de palavra (equivalente a `[a-zA-Z0-9_]`).
- **`\W`**: Qualquer caractere que **não** seja de palavra.
- **`\d`**: Qualquer dígito decimal (``).
- **`\D`**: Qualquer caractere que **não** seja um dígito.
- **`\s`**: Qualquer caractere de espaço em branco (como espaços, tabs).
- **`\S`**: Qualquer caractere que **não** seja espaço em branco.

#### Utilizando Flags (Ex: `re.IGNORECASE`)

Em vez de especificar letras maiúsculas e minúsculas no padrão, podemos passar a flag **`re.IGNORECASE`** como terceiro argumento de `re.search` para tratar a string de forma insensível a maiúsculas/minúsculas.

```
# Validação robusta de e-mail usando âncoras, atalhos e flags
if re.search(r"^\w+@\w+\.edu$", email, re.IGNORECASE):
```

---

### 7. Limpando Dados com Grupos de Captura (`(...)`) e o Operador Walrus (`:=`)

O professor apresenta o arquivo `format.py` para demonstrar como padronizar nomes digitados por usuários (ex: converter `"Malan, David"` para `"David Malan"`).

#### Grupos de Captura

Parênteses **`(...)`** em regex têm dupla função: agrupam partes da expressão e **capturam** o texto correspondente para que possamos extraí-lo mais tarde.
Se a busca for bem-sucedida, `re.search` retorna um objeto de correspondência (*matches*). Podemos acessar os dados capturados usando o método **`.group(index)`**, onde o índice `1` representa o primeiro par de parênteses, `2` o segundo, e assim por diante.

#### O Operador Walrus (`:=`)

O operador de atribuição **`:=`** (apelidado de *walrus* ou morsa) permite atribuir um valor a uma variável e realizar uma verificação condicional na mesma linha de código, deixando o fluxo muito mais limpo.

```
# format.py
import re

name = input("Qual o seu nome? ").strip()

# Busca por "Sobrenome, Nome" permitindo espaços opcionais (\s*)
if matches := re.search(r"^(.+),\s*(.+)$", name):
    # Reorganiza o nome invertendo os grupos capturados
    name = f"{matches.group(2)} {matches.group(1)}"

print(f"Olá, {name}")
```

---

### 8. Extração Avançada e Grupos de Não-Captura (`(?:...)`)

No exemplo final (`twitter.py`), o objetivo é extrair o nome de usuário do Twitter a partir de uma URL colada pelo usuário (ex: extrair `"davidjmalan"` de `"https://twitter.com/davidjmalan"`).

Para tornar o padrão tolerante a variações comuns (como a presença ou ausência de `https://` ou de `www.`), estruturamos grupos opcionais usando `?`:

#### Grupos de Não-Captura (`(?:...)`)

Se usarmos parênteses normais para tornar o protocolo `(https?://)?` e o subdomínio `(www\.)?` opcionais, o Python os tratará como grupos de captura, bagunçando a numeração das variáveis `.group(1)`, `.group(2)`, etc.
Para agrupar elementos sem salvá-los na memória de captura, adicionamos o prefixo **`?:`** logo após abrir o parêntese.

```
# twitter.py
import re

url = input("URL do Twitter: ").strip()

# Padrão com grupos de não-captura (?:...) e um grupo de captura final (...)
padrão = r"^(?:https?://)?(?:www\.)?twitter\.com/([a-z0-9_]+)$"

if matches := re.search(padrão, url, re.IGNORECASE):
    # Apenas o nome do usuário final é capturado no grupo 1
    print(f"Usuário: {matches.group(1)}")
```

---

### 9. Outras Funções do Módulo `re`

A aula conclui mencionando que a biblioteca `re` possui outras funções de grande utilidade prática além do `re.search`:

- **`re.sub(padrão, substituto, string)`**: Substitui as correspondências do padrão por uma nova string (útil para encontrar e substituir usando regex).
- **`re.match()`**: Semelhante ao `re.search()`, mas sempre força a correspondência a partir do início da string (dispensando o uso manual de `^`).
- **`re.fullmatch()`**: Semelhante ao `re.match()`, mas exige que o padrão cubra toda a string do início ao fim (dispensando `^` e `$`).
- **`re.split()`**: Divide uma string utilizando padrões regex como separadores (em vez de um caractere fixo).
- **`re.findall()`**: Retorna uma lista com todas as ocorrências encontradas do padrão dentro do texto.
