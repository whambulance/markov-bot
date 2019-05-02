# markov-bot
*A Discord bot designed in python. Generates new messages using Markov chains from user message history*

Markov chains are cool, and so is this russian man who impersonates your friends.
Paste the private code for your Discord bot in a file called "token.txt" directly. It should look like this:
```
T1bAcYNlVgqOHnbT6PbCgqOH.yVzxJ.wMHZ-pb2HXESAeiv0mUcXXak5_M
```
## User Commands
* !mk, !markov [USER]... [OPTION]...
  * Basic syntax
* -s, --startswith [STR]
  * Chain starting word
* -l, --length [INT]
  * Chain length - Random length between 1 - 14 by default, Max: 100
* !mkjson
  * Update personal JSON list since last refresh
  
## Examples:
```
!markov -s Heiroglyph
Generates a chain for you, beginning with word "Heiroglyph"

!mk PaulAtreides --limit 15
Generates a chain for user "PaulAtreides", limiting the markov chain to 15 words, and searching through 15,000 messages.
```

This is an example of the bot constructing Markov chains, using paragraphs pasted out of the Fellowship of the Ring. This was cut short by the default chain length:
![markov-bot test with LOTR paragraphs](https://raw.githubusercontent.com/whambulance/markov-bot/master/markovtest1.png)

## Admin Commands
*These are set in the code - sorry but as of current there is no easy way to configure this*
* !mkjson createchannel [MSGCOUNT]...
  * Create JSON Markov Dictionaries for the current channel. This takes a very long time (you have been warned)
* !mkjson createuser [USER]...
  * Create a JSON Markov Dictionary for the stated user
* !mkjson updateuser [USER]...
  * Updates the JSON Markov Dictionary for the stated user
  
## Examples:
```
!mkjson createchannel
Generates Markov dictionaires for each user, assigned to the channel you post this in

!mkjson createuser PaulAtreides
Generates a chain for user 'PaulAtreides', assigned to the channel you post this in

!mkjson updateuser PaulAtreides
Updates an existing chain for user 'PaulAtreides', with messages sent since the JSON Dictionary was created/last updated
```
