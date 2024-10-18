import pandas as pd
import pyreadstat
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import sys

# Configurando logging para monitorar o progresso e possíveis erros
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def selecionar_arquivo():
    """Utilizando a biblioteca tkinter, abre uma janela de diálogo para o usuário selecionar o arquivo SPSS."""
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal do Tkinter
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo SPSS",
        filetypes=[("Arquivos SPSS", "*.sav")],
    )
    if not file_path.endswith(".sav"):
        messagebox.showerror(
            "Erro", "Por favor, selecione um arquivo .sav válido.")
        return None
    return file_path


def caixa_dialogo_personalizada(titulo, mensagem, texto_botao1, texto_botao2):
    """Cria uma caixa de diálogo personalizada com dois botões.

    Args:
        titulo (str): Título da janela.
        mensagem (str): Mensagem exibida na caixa de diálogo.
        texto_botao1 (str): Texto do primeiro botão.
        texto_botao2 (str): Texto do segundo botão.

    Returns:
        str: Retorna a escolha feita pelo usuário ('botao1' ou 'botao2').
    """
    root = tk.Toplevel()
    root.title(titulo)

    label = tk.Label(
        root, text=mensagem)
    label.pack(pady=10)

    escolha = tk.StringVar(value="")

    def botao1():
        escolha.set("botao1")
        root.destroy()

    def botao2():
        escolha.set("botao2")
        root.destroy()

    btn1 = tk.Button(root, text=texto_botao1, command=botao1)
    btn1.pack(side=tk.LEFT, padx=10)

    btn2 = tk.Button(root, text=texto_botao2, command=botao2)
    btn2.pack(side=tk.RIGHT, padx=10)

    root.grab_set()
    root.wait_window()

    return escolha.get()


def mapeamento(df, meta, vars_mapeamento):
    """Função que fará o mapeamento dos valores categóricos do dataframe usando os metadados."""

    # Preciso corrigir quanto ao script não conseguir identificar que a variável Supervisora é "mapeável".
    for var in vars_mapeamento:
        if var in meta.variable_value_labels:
            rotulos_valores = meta.variable_value_labels[var]
            df[var] = df[var].map(rotulos_valores)
            logging.info(f"Rótulos aplicados na variável: {var}")
        else:
            logging.warning(
                f"A variável {var} não possui metadados categóricos.")
    return df


def normalizar_dataframe(df, colunas_upper, colunas_int):
    """Normaliza o dataframe convertendo colunas para maiúsculas e tipos apropriados."""
    df.columns = df.columns.str.upper()
    for col in colunas_upper:
        if col in df.columns:
            df[col] = df[col].str.upper()
        else:
            logging.warning(f"A coluna {col} não existe no dataframe.")

    if colunas_int:
        try:
            df[colunas_int] = df[colunas_int].astype(int)
        except KeyError as e:
            logging.error(f"Erro ao converter colunas: {e}")
        except ValueError:
            logging.error(
                f"Erro ao converter valores. Verifique os dados numéricos.")
    return df


def carregar_dados(arquivo, colunas_float_int, colunas_upper, valores_categoricos):
    """Carrega dados do arquivo SPSS e normaliza os dados."""
    try:
        logging.info(f"Carregando arquivo: {arquivo}")
        df, meta = pyreadstat.read_sav(arquivo)
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo SPSS: {e}")
        return None, None

    df = normalizar_dataframe(df, colunas_upper, colunas_float_int)

    # Se houver variáveis categóricas fornecidas, realiza o mapeamento
    if valores_categoricos:
        df = mapeamento(df, meta, valores_categoricos)

    return df, meta


def encontrar_ids_repetidos(df, subset, status_coluna='STATUS', filtro_status='Cancelada'):
    """Filtra registros cancelados e encontra IDs repetidos."""
    logging.info("Filtrando registros...")

    missing_columns = set(subset) - set(df.columns)
    if missing_columns:
        logging.warning(f"Colunas ausentes: {missing_columns}")

        acao = caixa_dialogo_personalizada(titulo="Colunas Ausentes",
                                           mensagem=f"As colunas {
                                               missing_columns} estão ausentes. Deseja continuar sem elas ou fornecer novas?",
                                           texto_botao1="Continuar",
                                           texto_botao2="Editar"
                                           )

        if acao == "botao1":
            subset = [col for col in subset if col not in missing_columns]
        elif acao == "botao2":
            novas_colunas = simpledialog.askstring(
                "Novas colunas", "Informe as novas colunas separadas por vírgula:"
            )
            try:
                subset = [col.strip().upper()
                          for col in novas_colunas.split(',')]
            except AttributeError:
                logging.error(f"Nenhuma coluna válida foi fornecida.")
                messagebox.showerror(
                    "Erro", "Nenhuma coluna válida foi fornecida.")
                sys.exit()

    # Ordenar o DataFrame pelas colunas fornecidas - sbjnum será o index e a ordenação fica a partir do ID
    df = df[subset].set_index('SBJNUM').sort_values('ID')
    df = df[df[status_coluna] != filtro_status]  # Remove registros cancelados

    # Identifica duplicatas
    df_duplicatas = df[df.duplicated('ID', keep=False)]
    return df_duplicatas


def main():
    colunas_float_int = ['SBJNUM', 'ID']
    valores_upper = ['NOME']
    valores_categoricos = ['SUPERVISOR']
    subset_1 = ['SBJNUM', 'ID', 'NOME', 'STATUS', 'SUPERVISOR']

    arquivo = selecionar_arquivo()
    if not arquivo:
        return  # Sai da função se o arquivo não for válido

    df, meta = carregar_dados(arquivo, colunas_float_int,
                              valores_upper, valores_categoricos)
    if df is None:
        return

    ids_duplicados = encontrar_ids_repetidos(df, subset_1)

    if ids_duplicados.empty:
        messagebox.showinfo("Info", "Nenhum ID duplicado encontrado.")
        return

    acao = caixa_dialogo_personalizada(
        titulo='Copiar ou salvar', mensagem="Deseja copiar os IDs para a área de transferência ou salvar em Excel?", texto_botao1="Copiar", texto_botao2="Salvar")
    if acao == "botao1":
        ids_duplicados.to_clipboard()
        messagebox.showinfo(
            "Info", "Dados copiados para a área de transferência!")
    elif acao == "botao2":
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            ids_duplicados.to_excel(file_path)
            messagebox.showinfo("Info", f"Dados salvos em {file_path}!")


if __name__ == "__main__":
    main()
