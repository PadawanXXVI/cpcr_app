# 📊 Sistema de Controle de Processos da CPCR - NOVACAP

Este sistema web foi desenvolvido para a Comissão Permanente Central de Relacionamentos (CPCR) da NOVACAP, com o objetivo de automatizar o fluxo de controle de processos administrativos vinculados ao Programa Administração 24h.

## 🚀 Funcionalidades

- Cadastro, atualização e consulta de processos administrativos
- Controle de status e movimentações
- Exportação de dados para Excel
- Autenticação e gestão de usuários
- Integração com Power BI para dashboards
- Registro de histórico de movimentações

## 🧱 Tecnologias Utilizadas

- Python + Flask (Backend)
- MySQL (Banco de Dados)
- HTML5 + CSS3 (Frontend)
- Pandas (Exportação)
- Power BI (Visualização de dados)
- Git + GitHub (Controle de versão)

## ⚙️ Instalação

```bash
# Clonar o repositório
git clone https://github.com/PadawanXXVI/cpcr_app.git
cd cpcr_app

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

## 💻 Execução

```bash
python app.py
```

Acesse no navegador: http://localhost:5000

## 🔐 Segurança

As variáveis sensíveis estão centralizadas no arquivo `.env` (NÃO versionado). Use o modelo de configuração disponível.

## 📄 Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

## 🤝 Contribuições

Sinta-se à vontade para abrir issues ou pull requests para sugerir melhorias!
