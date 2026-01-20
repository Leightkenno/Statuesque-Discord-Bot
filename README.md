# Statuesque Bot 🎮

A feature-rich Discord bot designed for Statuesque clan, providing comprehensive clan management, player tracking, competitions, event scheduling, and fun minigames.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 📊 Player Stats & Tracking
- Link multiple RuneScape accounts to Discord
- View player stats, skills, and combat levels
- Compare stats between players
- Track player activities via RuneMetrics
- Automatic activity monitoring

### 🏆 Boss & Drop Logging
- Log valuable drops with GP values
- Track boss kill counts and personal bests
- View drop history and leaderboards
- Boss kill leaderboards

### 🎯 Skilling Competitions
- Create skill-based XP competitions
- Automatic clan member enrollment
- Real-time XP tracking via hiscores
- Leaderboards with automatic updates
- Background sync every 30 minutes

### 📅 Event Scheduler
- Weekly event scheduling (Monday → Sunday)
- Event categories with colored indicators:
  - 🟥 Hard PvM (Raids, Solak, Vorago, etc.)
  - 🟧 Medium PvM (GWD2, Nex, ED1-3, etc.)
  - 🟩 Easy PvM (Arch-Glacor, Croesus, etc.)
  - 🟦 Skilling (Portables, Clan Gatherings)
  - 🟪 Minigames (Castle Wars, Pest Control)
  - ⬜ Clan Events (Citadel, Specials)
  - 🟫 Giveaways (Drop Parties, Raffles)
  - 🔵 Game Nexus (Non-RS games)
- Support for tags: `[L]` Learner, `[E]` Experienced, `[LS]` LootShare, `[K]` Keeps, `[S]` Splits

### 👥 Clan Management
- Automatic clan roster sync from RuneScape
- Discord role sync based on clan rank
- Track member joins, leaves, and promotions
- Name change detection
- Configurable public/private announcement channels

### 🏅 Hall of Fame
- Generate visual Hall of Fame images
- 30+ achievement categories (Titles, Capes, Rare Items)
- Customizable member lists per category
- Post to any channel

### ⚔️ Duel Arena Minigame
- Challenge other players to duels
- Animated GIF battles with:
  - Health bars
  - Hit splats with damage numbers
  - Special attacks (Dragon Claws, AGS, Ice Barrage, etc.)
  - Victory animations

### 🌍 World Events
- Wilderness Flash Event tracker
- Game time display
- Automated event announcements

### 👋 Welcome System
- Customizable welcome messages via JSON
- Embedded messages with fields
- Ping new users and/or roles
- Full emoji support
- Preview before going live

## 📋 Commands

### Account Management
| Command | Description |
|---------|-------------|
| `/link <rsn>` | Link your RuneScape account |
| `/unlink <rsn>` | Unlink an account |
| `/accounts` | View linked accounts |
| `/setprimary <rsn>` | Set primary account |

### Stats & Information
| Command | Description |
|---------|-------------|
| `/stats [rsn]` | View player stats |
| `/skill <skill> [rsn]` | View specific skill |
| `/compare <rsn1> <rsn2>` | Compare two players |
| `/price <item>` | Check GE prices |
| `/claninfo` | View clan statistics |

### Boss & Drops
| Command | Description |
|---------|-------------|
| `/drop <item> [boss] [value]` | Log a drop |
| `/drops [rsn]` | View drop history |
| `/kc <boss> <count>` | Log boss kills |
| `/bosslog [rsn]` | View boss kills |
| `/bossboard <boss>` | Boss leaderboard |

### Competitions (Admin)
| Command | Description |
|---------|-------------|
| `/compstart <skill> <title> <end_date>` | Start competition |
| `/compleaderboard [top]` | View standings |
| `/compinfo` | Competition details |
| `/compupdate` | Refresh XP data |
| `/comprefresh` | Sync clan roster |
| `/compend [channel]` | End & post results |
| `/compcancel` | Cancel competition |

### Event Scheduling (Admin)
| Command | Description |
|---------|-------------|
| `/schedule start [title] [week_start]` | Start schedule session |
| `/schedule add <day> <event> <host> <time> <category>` | Add event |
| `/schedule view` | View current schedule |
| `/schedule remove <id>` | Remove event |
| `/schedule generate` | Generate final embed |
| `/schedule categories` | Show category list |
| `/schedule cancel` | Cancel session |

### Hall of Fame (Admin)
| Command | Description |
|---------|-------------|
| `/hofstart [title]` | Start HoF session |
| `/hofadd <category> <members>` | Add members to category |
| `/hofremove <category> <member>` | Remove member |
| `/hofpreview` | Preview image |
| `/hofpost [channel]` | Post publicly |
| `/hoflist` | List current data |

### Welcome System (Admin)
| Command | Description |
|---------|-------------|
| `/welcome init` | Initialize config |
| `/welcome preview` | Preview message |
| `/welcome toggle` | Enable/disable |
| `/welcome title <text>` | Set title |
| `/welcome description <text>` | Set description |
| `/welcome color <hex>` | Set color |
| `/welcome addfield <name> <value>` | Add field |
| `/welcome clearfields` | Remove all fields |
| `/welcome pingrole <role>` | Set ping role |
| `/welcome reload` | Reload from JSON |

### Clan Management (Admin)
| Command | Description |
|---------|-------------|
| `/setclan <name>` | Set clan to track |
| `/clanlist` | View clan members |
| `/maprank <clan_rank> <discord_role>` | Map rank to role |
| `/rankmaps` | View rank mappings |
| `/toggleautorole` | Toggle auto role sync |
| `/syncme` | Sync your role |

### Minigames
| Command | Description |
|---------|-------------|
| `/duel <@user>` | Challenge to animated duel |
| `/quickduel <@user>` | Instant duel result |

### World Events
| Command | Description |
|---------|-------------|
| `/wildyflash` | Current Wilderness Flash Event |
| `/gametime` | Current game time (UTC) |

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Discord Bot Token
- Discord Server with admin permissions

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Leightkenno/statuesque-bot.git
   cd statuesque-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install discord.py aiohttp aiosqlite Pillow
   ```

4. **Configure the bot**
   
   Edit `bot.py` and update the configuration section:
   ```python
   BOT_CONFIG = {
       "clan_name": "YourClanName",
       "clan_motto": "Your Clan Motto",
       "logo_url": "https://your-logo-url.png",
       # ... other settings
   }
   
   TOKEN = "your-bot-token-here"
   GUILD_ID = 123456789  # Your Discord server ID
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## 📁 File Structure

```
statuesque-bot/
├── bot.py                 # Main bot file
├── clan_bot.db           # SQLite database (auto-created)
├── welcome_config.json   # Welcome message configuration
└── README.md
```

## ⚙️ Configuration

### Bot Configuration
Edit the `BOT_CONFIG` dictionary in `bot.py`:

```python
BOT_CONFIG = {
    "clan_name": "Statuesque",
    "clan_motto": "Always Aiming Higher",
    "logo_url": "https://...",
    "primary_color": 0x2ECC71,
    "success_color": 0x27AE60,
    "warning_color": 0xF39C12,
    "error_color": 0xE74C3C,
    "gold_color": 0xFFD700,
    "clan_public_channel": "clan-chat",
    "clan_private_channel": "staff-logs",
}
```

### Welcome Messages
Edit `welcome_config.json` or use `/welcome` commands:

```json
{
  "guild_id": {
    "enabled": true,
    "ping_user": true,
    "ping_role": null,
    "title": "Welcome! 🎉",
    "description": "We're glad you're here!",
    "color": "2ECC71",
    "fields": [
      {
        "name": "📋 Getting Started",
        "value": "• Introduce yourself\n• Link your RSN with /link",
        "inline": false
      }
    ],
    "footer": {
      "text": "Welcome to the clan!",
      "icon": true
    },
    "thumbnail": "user"
  }
}
```

## 🗄️ Database

The bot uses SQLite with the following tables:
- `linked_accounts` - Discord to RSN links
- `drop_log` - Logged drops
- `boss_kills` - Boss kill counts
- `activity_tracking` - Player activity monitoring
- `guild_settings` - Server configuration
- `schedule_sessions` - Event schedule sessions
- `schedule_entries` - Scheduled events
- `clan_members` - Clan roster
- `rank_mappings` - Clan rank to Discord role mappings
- `name_changes` - Detected name changes
- `competitions` - Skilling competitions
- `competition_participants` - Competition participants

## 🔗 API Sources

- **RuneMetrics** - Player profiles and activity
- **RS Hiscores** - Skills and rankings
- **RS Clan Hiscores** - Clan member lists
- **RS Wiki API** - Item prices
- **Ely.gg API** - Alternative price data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [RuneScape Wiki](https://runescape.wiki) - Price data and images
- [Jagex](https://www.jagex.com) - RuneScape APIs

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Contact me on Discord @Oogleb

---

**Made with ❤️ for the Statuesque Clan**
