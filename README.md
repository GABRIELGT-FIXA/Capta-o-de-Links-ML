# Automação de Links de Afiliados do Mercado Livre

Este projeto tem como objetivo automatizar a captura de links de afiliados do Mercado Livre e seu salvamento em uma planilha do Google Sheets. A automação é destinada a quem gerencia múltiplos negócios online e precisa de uma forma rápida e eficiente de gerar links de afiliados para os produtos mais vendidos do Mercado Livre.

---

## Tecnologias Utilizadas 🚀

- **Python**: A linguagem principal do projeto.
- **Selenium**: Usado para automação de navegação web e interação com a página.
- **Undetected Chromedriver**: Para garantir que a automação funcione sem ser detectada como bot pelo Mercado Livre.
- **Google Sheets API**: Para integração com o Google Sheets e salvamento dos dados coletados.
- **OAuth2**: Para autenticação e autorização de acesso à planilha do Google.
- **JSON**: Para gerenciar e salvar os cookies de sessão.

---

## Funcionalidades 🌟

1. **Login automático no Mercado Livre**: Utiliza cookies de sessão para acessar a conta do Mercado Livre sem a necessidade de login manual.
2. **Coleta de links de produtos mais vendidos**: Captura os links de produtos diretamente da página "Mais Vendidos" do Mercado Livre.
3. **Geração de links de afiliados**: Para cada produto coletado, gera automaticamente um link de afiliado.
4. **Armazenamento no Google Sheets**: Todos os dados (título, link original, link de afiliado e imagem) são salvos em uma planilha do Google Sheets para fácil acesso e acompanhamento.

---

## Como Usar 🔧

### 1. Clone o Repositório

```bash
git clone https://github.com/SEU_USUARIO/mercadolivre-affiliate-links.git
cd mercadolivre-affiliate-links
2. Instale as Dependências
Este projeto usa Python e as bibliotecas listadas no arquivo requirements.txt. Instale as dependências executando:

bash
Copiar código
pip install -r requirements.txt
3. Configuração 🔑
Antes de rodar o script, você precisa configurar algumas informações:

Arquivo de Credenciais do Google (JSON):

Vá até Google Cloud Console, crie um novo projeto e habilite a API do Google Sheets.

Baixe o arquivo de credenciais JSON e coloque-o na pasta do projeto. Renomeie o arquivo para SEU_ARQUIVO_CREDENCIAL.json.

ID da Planilha do Google Sheets:

Abra a planilha do Google Sheets que você deseja usar.

O ID é a parte da URL entre /d/ e /edit. Exemplo:

bash
Copiar código
https://docs.google.com/spreadsheets/d/SEU_ID_DE_PLANILHA/edit
Substitua a variável ID_PLANILHA no código pelo ID da planilha.

Nome da Aba:

Defina o nome da aba na planilha onde os dados serão salvos. O padrão é "Página1", mas você pode alterar para o nome desejado.

Cookies de Sessão:

Para realizar o login sem problemas, é necessário que você extraia e salve seus cookies de sessão do Mercado Livre em um arquivo JSON.

Você pode usar ferramentas como Cookie Manager para salvar os cookies do seu navegador após fazer login na sua conta do Mercado Livre.

Como Rodar 🚀
Com tudo configurado, basta executar o script para iniciar a automação:

bash
Copiar código
python main.py
Isso vai iniciar a coleta de links de afiliados do Mercado Livre e armazená-los diretamente na planilha do Google Sheets que você configurou.

Exemplo de Resultado 📊
O script irá coletar dados de produtos como:

Título	Link Original	Link de Afiliado	Imagem
Smartphone XYZ	https://www.mercadolivre.com.br/produtoXYZ	https://meli.la/affiliateLinkXYZ	https://www.mercadolivre.com.br/imageXYZ.jpg

Estrutura do Projeto 📂
bash
Copiar código
mercadolivre-affiliate-links/
├── main.py                        # Arquivo principal para rodar a automação
├── requirements.txt               # Dependências do projeto
├── cookies.json                   # Arquivo de cookies de sessão (gerado manualmente)
├── SEU_ARQUIVO_CREDENCIAL.json     # Arquivo de credenciais do Google (necessário para acessar o Google Sheets)
└── README.md                      # Este arquivo
Contribuindo 🤝
Se você encontrou algum problema ou deseja contribuir para melhorar o projeto, sinta-se à vontade para fazer um fork e enviar um pull request!

Licença 📄
Este projeto é licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.

Agradecimentos 🙏
Selenium - Para automação da navegação web.

Undetected Chromedriver - Para evitar bloqueios de bot no Mercado Livre.

Google Sheets API - Para integração com o Google Sheets.

markdown
Copiar código

### Explicação do README

1. **Introdução**: Uma explicação rápida do que o projeto faz.
2. **Tecnologias Utilizadas**: Descreve as ferramentas e bibliotecas principais usadas no projeto.
3. **Funcionalidades**: Lista das funcionalidades chave da automação.
4. **Como Usar**: Passo a passo para configurar o projeto localmente.
5. **Como Rodar**: Instruções simples para rodar o código após a configuração.
6. **Exemplo de Resultado**: Mostra como os dados são salvos na planilha do Google Sheets.
7. **Estrutura do Projeto**: Mostra como os arquivos estão organizados.
8. **Contribuição**: Instruções sobre como contribuir com o projeto.
9. **Licença**: Informa que a licença do projeto é a MIT License, permitindo que outras pessoas usem e contribuam livremente.

Esse README será útil para que qualquer pessoa que queira usar ou colaborar com o projeto entenda o propósito do código e como configurá-lo corretamente.






