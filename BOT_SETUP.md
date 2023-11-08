# 🚀 Telegram Bot configuration guide
___

## 🤖 Step #1
___
### Create a Telegram bot using **BotFather**
- Contact the [@BotFather](https://telegram.me/BotFather) bot to receive a list of Telegram chat commands.
- Now use the **/newbot** command and wait for instructions to select a name and username. Upon successfully creating your bot, you’ll receive the **bot's token**.
- Specify the BOT_TOKEN in [.env](.env) file with your **bot's token**.


## 💬 Step #2

---
### Telegram chat
- Create a Telegram group chat
- Add bot to created chat
- Get the list of updates for your Bot https://api.telegram.org/bot<YourBotToken>/getUpdates (replace \<YourBotToken> with the token of your bot)
- Look for the **"chat"** object, it should look like this: "chat":{"id":**<group_ID>**,"title":""}
- Specify the CHAT_ID parameter in [.env](.env) file with your **<group_ID>**.
