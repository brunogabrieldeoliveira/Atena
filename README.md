# 📈 Agente de IA para Análise de Investimentos

Este projeto é um **Agente Inteligente** desenvolvido com **LangChain** e **Streamlit**, projetado para auxiliar na análise de investimentos. Através da integração com a **OpenAI API**, o agente oferece insights, responde a perguntas sobre o mercado financeiro e ajuda na tomada de decisões estratégicas com base em dados.

---

## 🚀 Funcionalidades

- Processamento de linguagem natural via **LangChain**
- Interface interativa com **Streamlit**
- Análise contextual de investimentos
- Fácil integração com a **OpenAI API**

---

## 🧠 Tecnologias Utilizadas

- Python
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- `.env` para variáveis de ambiente

---

## ⚙️ Pré-requisitos

- Python 3.8+
- Git
- Conta na OpenAI com chave de API ativa

---

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/brunogabrieldeoliveira/Atena.git
cd nome-do-repositorio
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)
   
Windows:
python -m venv venv
venv\Scripts\activate

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

### 3. Instale as dependências

pip install -r requirements.txt


🔐 Configuração da API Key
Para garantir a segurança da sua chave da API, usamos um arquivo .env que não está incluído no repositório.

### 1. Crie um arquivo .env na raiz do projeto:

touch .env  # Linux/Mac
type nul > .env  # Windows

### 2. Adicione sua chave da OpenAI:

OPENAI_API_KEY=sua-chave-aqui

▶️ Executando o Projeto
Após configurar tudo corretamente, execute:

streamlit run app.py
A aplicação será iniciada e um link será gerado no terminal para acesso via navegador.

🧪 Exemplo de Uso

* 1. Anexe relatórios em formato pdf para o seu agente analisar.
* 2. Pergunte sobre os indicadores operacionais da empresa em análise!

O agente irá responder com base nos dados disponíveis e capacidades da OpenAI.

📌 Observações
O projeto está em fase de desenvolvimento contínuo. Contribuições são bem-vindas!

Lembre-se de NÃO versionar o .env nem compartilhar sua chave da OpenAI.

⭐ Gostou do projeto?
Deixe uma estrela no repositório para apoiar o desenvolvimento! 🌟
