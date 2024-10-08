# Scripts para Manipulação de Arquivos SPSS

Este repositório contém uma coleção de scripts/estudos para **manipulação e análise de arquivos SPSS (.sav)**, usando bibliotecas Python como pyreadstat, pandas e outras. Os scripts foram criados para automatizar a verificação e processamento de dados em pesquisas e entrevistas.

## Funcionalidades 

- **Leitura de arquivos SPSS:** Scripts que utilizam a biblioteca pyreadstat para carregar arquivos .sav em um DataFrame do pandas.
- **Manipulação de dados:** Ferramentas para normalizar colunas, transformar tipos de dados (ex: de float/int), e padronizar valores textuais.
- **Mapeamento de valores categóricos:** Automação da conversão de códigos categóricos em seus rótulos descritivos.
- **Verificação de duplicidade:** Identificação de IDs duplicados e registros inválidos com base em critérios customizáveis.
- **Extração de metadados:** Extração de informações detalhadas dos metadados do arquivo SPSS, como número de variáveis, número de registros e dicionário de variáveis.
- **Seleção de arquivos via interface gráfica:** Opção para selecionar arquivos SPSS via uma janela de diálogo gráfica, evitando a necessidade de digitar manualmente o caminho do arquivo.

## Estrutura dos Scripts
### 1. Carregamento e Visualização de Metadados

### Objetivo:
Carregar arquivos .sav e exibir informações básicas sobre o conjunto de dados, como número de variáveis, registros e rótulos das variáveis.   

### Descrição:
- Exibe metadados do arquivo.
- Abre uma janela para o usuário selecionar o arquivo SPSS.
___
### 2. Verificação de Duplicidades

### Objetivo: 
Normalizar colunas de texto e converter tipos de dados. Além disso, faz mapeamento de valores categóricos para facilitar a análise. A partir disso, identifica e lista registros duplicados com base em IDs, útil para processos de controle de qualidade.

### Descrição:
- Normaliza nomes de colunas e converte colunas numéricas.
- Converte variáveis categóricas em seus rótulos correspondentes.
- Verificação e listagem de duplicidades por ID.
___
### 3. Geração de Relatórios Personalizados

### Objetivo:
Permitir ao usuário gerar diferentes relatórios a partir dos dados carregados, como Pantry Check, Endereço, Listagem de IDs/SBJNUM e Canceladas.

### Descrição:
- Exportação de resultados diretamente para a área de transferência ou para um arquivo Excel.

## Pré-requisitos

Para rodar os scripts deste repositório, você precisará ter as seguintes bibliotecas instaladas:

```pip install pandas pyreadstat tqdm```

Se você deseja habilitar a seleção de arquivos via interface gráfica:

```pip install tkinter```

## Como usar

**1. Seleção de arquivos:** Ao executar o script, uma janela de diálogo será aberta para que você selecione o arquivo SPSS que deseja processar.<br>
**2. Carregamento e manipulação de dados:** O script irá carregar os dados e normalizar as colunas conforme a configuração inicial.<br>
**3. Verificação de duplicidades:** Se houver necessidade, o script identifica e exibe IDs duplicados.

## Atualizações Futuras

Este repositório está em desenvolvimento contínuo e será atualizado com novos scripts e funcionalidades focadas na auditoria e verificação a partir de arquivos SPSS (.sav).