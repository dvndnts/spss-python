import pyreadstat
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog


def info_metadata(meta):
    # Exibe informações básicas sobre os metadados.
    print("Metadata:")
    # Acessando as informações corretamente a partir do meta
    print(f"Qtde. de variáveis: {len(meta.column_names)}")
    print(f"Qtde. de casos/registros: {meta.number_rows}")
    print('-'*100)
    # Exibir a lista com os nomes das colunas/variáveis
    print(f"\nNome das variáveis: {meta.column_names}")


def selecionar_arquivo():
    """Utilizando a biblioteca tkinter, abre uma janela de diálogo para o usuário selecionar o arquivo SPSS."""
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal do Tkinter
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo SPSS",
        # Filtrar para mostrar apenas arquivos .sav
        filetypes=[("Arquivos SPSS", "*.sav")],
    )
    return file_path


# Selecionar o arquivo usando o diálogo
file_name = selecionar_arquivo()
# se quiser colocar diretamente no código é só modificar para
# r'[caminho_do_arquivo]'

if not file_name:
    print("Nenhum arquivo foi selecionado.")
else:
    try:
        # Carregar o arquivo SPSS
        df, meta = pyreadstat.read_sav(file_name)
        """
        DF - Dataframe contendo os dados
        Meta - Objeto que contém as informações dos metadados do SPSS (labels, dicionário de variáveis, etc)
        """
        print(f"Carregamento concluído. Total de linhas: {len(df)}\n")

        # Exibir informações dos metadados
        info_metadata(meta)

    except FileNotFoundError:
        print(f'Arquivo SPSS não foi encontrado. Verifique o caminho do arquivo.')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
