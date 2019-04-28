# markov-bot
*A Discord bot designed for Repl.it. Generates new messages using Markov chains from user message history*

# Commands
* !mv, !markov [USER]... [OPTION]...
  * Basic syntax
* -s --startswith [STR]
  * Chainn starting word
* -l, --limit [INT]
  * Maximum chain length - set to 14 by default
* "-h, --history [INT]
  * Search history in No. of messages - set to 3000 by default
  
Example commands:
> !markov -s Around -h 5000
>
> Generates a chain for you, beginning with word "Around", and searching backwards 5,000 messages

> !mk PaulAtreides --limit 15 -h 15000
>
> Generates a chain for user "PaulAtreides", limiting the markov chain to 15 words, and searching backwards 15,000 messages.

This is an example of the bot constructing Markov chains, using paragraphs pasted out of the Fellowship of the Ring
![markov-bot test with LOTR paragraphs](https://raw.githubusercontent.com/whambulance/markov-bot/master/markovtest1.png)

Designed to work on Repl.it running on a Flask server
Paste the private code for your Discord bot in the .env file directly. It should look like this:

>DISCORD_BOT_SECRET=T1bAcYNlVgqOHnbT6PbCgqOH.yVzxJ.wMHZ-pb2HXESAeiv0mUcXXak5_M
