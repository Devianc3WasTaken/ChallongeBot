
# Challonge Bot
#### Made to easily register, check in and unregister for tournaments on Challonge.
Currently only working for users who have a Challonge account and not made with other websites (Twitter, Discord, etc.)

All made using Python requests and BeautifulSoup

How to install and run: 
 1. `pip install -r requirements.txt`
 2. For running the discord bot, insert discord token into `.env` and run: `python bot.py`
 3. For running standalone bot: 
	 4. uncomment the `main()` in `main.py` 
	 5. run: `python main.py`

### To-do:
- [x] Integrate into a discord bot to allow various communities (especially the FGC) to easily manage signups to events.
- [x] Allow for check-ins and unregistering
  - [ ] Use of emotes on Discord under posted link for user's registered to the bot to easily signup by clicking the emote
- [x] Allow to show the rules of the event
  - [x] Examples would be: Printing out the rules and asking in the app to confirm "Y or N" if you agree
  - [x] Discord bot automatically DMs the person the rules after signing up, which allows the person to read and join any Discord's if needed
- [ ] Show next match for the user
- [ ] Print / DM list of participants to the user
- [ ] Print / DM the results of the event if it is finished
- [ ] Login using logins from other websites (such as Discord, Twitter, etc.)
- [ ] Potentially be able to create simple double-elim brackets for FGC events

#### How to use via the Discord bot:
- Default command is `.`
- `.userdetails email:password:username` (can **only** be used in DMs with the bot)
	-  For example:  `.userdetails deviance@gmail.com:qwerty123:deviance69`
- `.register [challongelink]` (Registers the user to this event)
	- For example: `.register https://challonge.com/7way2nqm`
- `.checkin [challongelink]` (Checks-in the user for this event)
	- For example: `.checkin https://challonge.com/7way2nqm`
- `.unregister [challongelink]` (Unregisters the user for this event)
	- For example: `.unregister https://challonge.com/7way2nqm`

#### How to use (if using standalone, **NOT** using discord bot):
1. Replace the placeholders in "login.txt" with your own login details. 
	a. For example: `deviance@gmail.com:qwerty123:deviance69`
2. Run the bot and paste in the Challonge link
3. You should be all signed up and ready to go!