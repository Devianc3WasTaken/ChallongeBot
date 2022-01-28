Challonge Bot made to easily register, check in and unregister for tournaments on Challonge.

Currently only working for users who have a Challonge account and not made with other websites (Twitter, Discord, etc.)

All made using Python requests, BeautifulSoup and pickle.

To-do:
- [ ] Integrate into a discord bot to allow various communities (especially the FGC) to easily manage signups to events.
- [x] Allow for check-ins and unregistering
  - [ ] Use of emotes on Discord under posted link for user's registered to the bot to easily signup by clicking the emote
- [ ] Allow to show the rules of the event
  - [ ] Examples would be: Printing out the rules and asking in the app to confirm "Y or N" if you agree
  - [ ] Discord bot automatically DMs the person the rules after signing up, which allows the person to read and join any Discord's if needed
- [ ] Show next match for the user
- [ ] Print / DM list of participants to the user
- [ ] Print / DM the results of the event if it is finished
- [ ] Login using login's from other websites (such as Discord, Twitter, etc.)
- [ ] Potentially be able to create simple double-elim brackets for FGC events

How to use:
1) Replace the placeholders in "login.txt" with your own login details. For example: deviance@gmail.com:qwerty123:deviance69
2) Run the bot and paste in the Challonge link
3) You should be all signed up and ready to go!
