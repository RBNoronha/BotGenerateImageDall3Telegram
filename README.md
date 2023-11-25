
# Bot de Geração de Imagens do Telegram

## Descrição
Este bot do Telegram permite aos usuários gerar imagens personalizadas com base em textos usando a API DALL-E da OpenAI. Ele oferece uma interface interativa para escolher o tamanho e a qualidade da imagem.

## Recursos
- Geração de imagens com base em texto usando a API DALL-E da OpenAI.
- Opções interativas para escolher tamanho e qualidade da imagem.
- Capacidade de gerar a mesma imagem novamente ou iniciar uma nova solicitação.

## Pré-requisitos
- Python 3.6 ou superior.
- Uma conta de desenvolvedor na OpenAI para acessar a API DALL-E.
- Um bot do Telegram configurado através do BotFather.

## Instalação
Instale as bibliotecas necessárias usando o seguinte comando:
```bash
pip install telepot requests openai
```

## Configuração do Bot no Telegram
1. Crie um novo bot conversando com o [BotFather](https://t.me/botfather) no Telegram.
2. Siga as instruções para criar um novo bot e obtenha o token do bot.
3. Insira o token do bot no script.

## Configuração da API DALL-E
1. Crie uma conta na [OpenAI](https://openai.com/) e obtenha a chave de API para a API DALL-E.
2. Substitua a chave de API no script.

## Execução
Execute o bot com o seguinte comando:
```bash
python BotTelegramGenerateImageDall3.py
```

## Uso
1. Inicie uma conversa com o bot no Telegram.
2. Use o comando `/start` para ativar o bot.
3. Siga as instruções interativas para gerar a sua imagem.

## Contribuições
Contribuições são bem-vindas. Por favor, abra issues ou pull requests para sugerir melhorias.

## Licença
Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
