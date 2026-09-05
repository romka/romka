---
title: Robot Wants Kitty Is Back in Your Browser
date: 2026-09-05 16:28:20 +0200
draft: false
tags: [game, flash, Robot Wants Kitty, metroidvania, remaster, Defold, work]
---
In the mid-2000s and early 2010s, it was hard to imagine the internet without Flash—a technology that brought video to the web (YouTube would have been impossible without Flash back then!), animated banners, advanced website interfaces and, of course, games. Without Flash, the web of that time was primitive and boring. Flash was a breakthrough technology that was ahead of its time and shaped what the internet would look like for the next 10–20 years. Starting in the early 2010s, the technology gradually began to die: HTML5 started standardizing things such as video and WebAssembly, and everything that had previously required a third-party Flash plugin could now be implemented using standard browser features. Apple's refusal to support Flash on its mobile devices was a serious blow to the technology.

In the end, the era of Flash in general, and Flash games in particular, came to an end in 2017, when Adobe announced that it would stop developing and supporting Flash Player. A whole layer of internet culture from the 2000s and early 2010s was buried along with Flash. The vast majority of games from that time were primitive, unplayable garbage, but every now and then there were gems.

One such gem is the Robot Wants [Kitty|Puppy|Fishy|Ice Cream] series. I was a big fan of these games, so I decided to port them to a modern technology stack so that they could be played directly in a browser. There will be a separate post about the porting process, but right now I want to share that Mike Hommel, creator of the original games, gave me permission to publish remastered versions of his games.

{{<img "robot-wants-kitty-gameplay.png" >}}

The Robot Wants Stuff games are perfectly balanced metroidvanias. Playing as Robot, you need to rescue his pet. But Robot is weak and clumsy by default, so even though the entire world is completely open from the start, reaching its farthest corners and finding the keys that open the way to the pet means making your way through a tangled maze and defeating hordes of enemies.

In a poorly balanced game, constantly lacking abilities would be annoying. In the Robot Wants Stuff series, it works as a hint. Robot is always just a little short of something: sometimes he cannot quite jump onto the platform he needs, sometimes he cannot dive into the water or deflect an enemy attack. The game never tells you directly where to go, but it constantly shows you _why_ you should return later. Finding new power-ups and unlocking new abilities gives you a rush: “Aha! Now I know how to get farther in that room!” This feeling of satisfaction from solving a puzzle is the most valuable emotion a gamer can experience, and the Robot Wants Stuff games deliver it in full!

The first game I brought into the modern age is Robot Wants Kitty. Once you know the right route, Robot Wants Kitty can be completed in about fifteen minutes. If you do not know where to go... honestly, I am a little jealous. You still have the chance to experience that pleasure of exploring it for the first time, when the small map gradually comes together in your head and every new ability turns several old dead ends into new routes.

You can **[play Robot Wants Kitty](https://flames.cool/games/robot-wants-kitty/)** on my other website.

Robot Wants Kitty is the first of four games. Remasters of _Robot Wants Puppy_, _Robot Wants Fishy_, and _Robot Wants Ice Cream_ will follow later.

In addition to regular keyboard controls, I added touch controls. On a phone, the game automatically opens in a portrait Game Boy-style layout: the game screen is at the top and the controls are underneath it. So now you can help Robot rescue Kitty on a computer, phone, or tablet.

If you would like to support the creator of the original games, Hamumu Games has an official modern collection of the entire series: [Robot Wants It All on Steam](https://store.steampowered.com/app/834760/Robot_Wants_It_All/).

Soon I will write a separate post with the technical details: how I reconstructed the game from the SWF, ported it to Defold, and made sure it worked consistently in modern browsers and on touch screens.
{{< more >}}
<!--more-->
