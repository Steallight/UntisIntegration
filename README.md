[maven-central]: https://img.shields.io/badge/python-v1-blue
[progress-release]: https://img.shields.io/badge/build-stable-green
[installation]: #-installation

# UntisIntegration
A simple Discord bot to fetch your school schedule from Untis.

![maven-central][]
![progress-release][]

## Quick Links
- [Installation](#installation)
- [Usage](#usage)
- [How it works](#how-it-works)

## Installation
1. **Clone the repository:**

```Bash
git clone https://github.com/your-username/UntisIntegration.git
```

2. **Create a virtual environment (recommended):**

```Bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```Bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Create a `.env` file in the project root with the following:   
```env
UNTIS_SERVER=<your_untis_server_address>
UNTIS_USERNAME=<your_untis_username>
UNTIS_PASSWORD=<your_untis_password>
UNTIS_SCHOOL=<your_untis_school_name>
DC_TOKEN=<your_discord_bot_token>
UNTIS_KLASSE=<your_untis_class_name>  # Optional: For specific class schedules
```

## Usage
1. **Run the bot:**

```Bash
python main.py
```


2. **In Discord:**

Send `!plan` in a channel where the bot is present. Your schedule will be sent as a DM.

### How it works
- `PeriodObject`: Represents a single class period with details like time, subject, teacher, and room.
- `erstelle_stundenplan`: Processes Untis data and formats it into a readable schedule string.
- **Discord Bot**: Listens for `!plan` commands, fetches the schedule, and sends it via DM.
### Additional Notes
- Use a secure method for storing environment variables.
- Consider error handling and caching for performance.
- Customize the schedule format and Discord integration.
### Potential Enhancements
- Command-line arguments for class selection.
- Caching for frequent schedule requests.
- Support for multiple classes.
- Cloud deployment for continuous availability.
