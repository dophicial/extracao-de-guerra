# Extracao de Guerra

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SEU_USUARIO/extracao-de-guerra/blob/main/colab_app.ipynb)

> **Importante:** substitua `SEU_USUARIO` na URL acima pelo usuário do GitHub que contém este repositório para que o Colab localize o notebook.

Aplicativo em Python para consultas rápidas ao **DirectData** com visual escuro minimalista. Entre as funcionalidades:

- Busca instantânea (≤30s) com retorno completo de dados cadastrais.
- Painel com gráficos e filtros.
- Exportação para PDF e Excel.
- Histórico de consultas para reabertura e comparação.
- Interface em Português.

## Execução no Google Colab

1. Abra o notebook acima pelo badge "Abrir no Colab".
2. Execute as células de instalação e inicialização.
3. Será exibido um link público para acessar o aplicativo.

## Variáveis de ambiente

Configure no Colab se possuir uma chave da API:

```python
import os
os.environ['DIRECTD_API_KEY'] = 'sua_chave_aqui'
# os.environ['DIRECTD_BASE_URL'] = 'https://app.directd.com.br/api'
```

Você também pode salvar `DIRECTD_API_KEY` e `DIRECTD_BASE_URL` em **Secrets** do Colab; o notebook `colab_app.ipynb` irá carregá-las automaticamente.

Sem a chave, dados fictícios de demonstração serão utilizados.

Se `DIRECTD_BASE_URL` não for informado, o app utilizará `https://app.directd.com.br/api` como padrão.
