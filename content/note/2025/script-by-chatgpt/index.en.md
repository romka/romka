---
date: 2025-03-29 17:14:12 +0100
tags: [2025, Telegram, ChatGPT]
---
Recently, I added automatic posting to my [Telegram channel](https://t.me/romkaeu) from my blog [romka.eu](https://romka.eu). The whole thing works fully automatically:
- the entire blog is just a directory hierarchy, where each post is [a single directory](https://github.com/romka/romka/tree/main/content/note/2025/script-by-chatgpt), and the content -- `index.ru.md` and `index.en.md` files inside it. For convenience, the directory is managed with Git, and all sources are pushed to GitHub,
- as soon as a new post is pushed to GitHub, my custom workflow [send_to_telegram.yml](https://github.com/romka/romka/blob/6cc29f57fe42148fb54758cc105f5e7351dc4fc3/.github/workflows/send_to_telegram.yml) kicks in, finds all the files changed in the latest commit, and passes them to the script [post_to_telegram.py](https://github.com/romka/romka/blob/6cc29f57fe42148fb54758cc105f5e7351dc4fc3/telegram-data/post_to_telegram.py)
- `post_to_telegram.py` takes a local path to a blog post or gallery and, if the config contains `telegram: true`, then the post gets sent to the channel via the Telegram API,
- in response, the Telegram API returns a message ID. That ID gets committed to the file [telegram_mappings.csv](https://github.com/romka/romka/blob/6cc29f57fe42148fb54758cc105f5e7351dc4fc3/telegram-data/telegram_mappings.csv).
- Then, if `post_to_telegram.py` receives a file that is already listed in `telegram_mappings.csv`, instead of sending a new message, it edits the existing one.

There's nothing too crazy about this automation. The most interesting part is that literally all of the components above for automating the process were generated for me by ChatGPT.

I have to admit, that I spent more than a day talking to ChatGPT to get code that works well enough -- and honestly, I probably would've spent about the same amount of time coding it myself (basically, it's mostly about sending simple HTTP requests).

Still, the AI took a wrong turn a few times. For example, when I asked it to make small edits to code that was already working almost perfectly, it started overengineering everything. I had to suggest alternative approaches myself to keep the code both working and readable.

Basically, ChatGPT works like a good smart intern: it generates code that looks plausible, but you absolutely have to review it carefully -- there's almost always something broken or awkward in there.

I've tried a few other AI tools in my work, but so far -- surprisingly -- ChatGPT is still the most reasonable one. “Surprisingly”, because ChatGPT is a general-purpose model. I also tested coding-specific models: JetBrains AI Assistant, GitHub Copilot, and Claude 3.7 Sonnet. The first two are unbelievably dumb -- especially considering they have full access to the project's codebase, unlike ChatGPT. As for Claude, I couldn't even get it to work properly: it not only charges for every API call, but also has a built-in rate limiter. Even the simplest request I send ends up hitting a limit error. I guess it tries to ship my entire codebase with each request. I honestly can't think of any other explanation.

Still, all these AI tools are kind of amazing. Ten years ago, we couldn't even dream of assistant-level intelligence like this. I'm almost scared to imagine what they'll evolve into over the next ten years.
<!--more-->