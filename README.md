# This time i didnt skid! i stole!


# Account Link & Recovery Bot 🤖  

This repository contains a **Telegram bot** designed for **account linking** and **recovery** purposes. Whether you're connecting in-game accounts or restoring lost data, this bot simplifies the process with its intuitive commands and database integration.  

## 🚀 Features  
- **Account Linking:** Easily bind your in-game account using `/connect`.  
- **Profile Management:** View account details, including trophies, gems, and VIP status, with `/profile`.  
- **Account Recovery:** Recover lost accounts securely via `/recloud`.  
- **Cancellation Option:** Exit recovery mode at any time using `/stop`.  

## 🛠️ Technologies Used  
- **Python**  
- **Telegram Bot API** (`pyTelegramBotAPI`)  
- **SQLite** for database management  

## 📜 Commands  
| Command       | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `/start`      | Start the bot and view basic instructions.                                  |
| `/connect`    | Link your account by providing your in-game ID.                            |
| `/profile`    | View your linked account's details, including trophies and gems.           |
| `/recloud`    | Start the recovery process for a lost account.                             |
| `/stop`       | Cancel the recovery process and return to the main menu.                   |

## 📂 Folder Structure  
- **`database/Bot/users.db`**: Stores bot-specific user data.  
- **`database/Player/plr.db`**: Stores game-related player data.  

## 📝 Setup  
1. Clone the repository.  
2. Install required dependencies using `pip install pyTelegramBotAPI`.  
3. Replace the `YOUR_BOT_TOKEN` in the script with your Telegram Bot Token.  
4. Set up the SQLite databases for user and player data.  
5. Run the bot using `python bot.py`.
