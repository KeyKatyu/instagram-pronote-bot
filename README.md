# Instagram Pronote BOT

A Python script which posts the daily canteen menu in a story &amp; sends a message when a teacher is absent or when there is a new grade !
I'm not a professional dev but I tried to learn Python by creating a small useful project.

## Libraries
I used this libraries in my code :
- [pronotepy's](https://github.com/Bapt5/pronotepy) fork by Bapt5
- [instagrapi](https://github.com/adw0rd/instagrapi) by adw0rd
- PIL
- schedule
- time, datetime
- re

*Thanks to them because I couldn't have succeeded without their libraries !*

## What the script can do ?
By launching the file, it will :
- check every X minutes if there is a new absent teacher or a new grade,
- post at the exactly time (UTC hour) the daily canteen menu and that on monday, tuesday, wednesday, thursday & friday.

## How to edit ?
First, you must edit the `client = pronotepy.Client()` line. If you're using an ENT for the Pronote connection, you must import it before (`from pronotepy.ent import YOUR_ENT`) and if you're not using an ENT you must delete the import line and the `ent=` in client constructor.

Next, edit the `instagram.login()` line. I advise you to create a special account because Instagram can ban it. *NOTE : The script sends messages on the only **FIRST THREAD** of the Instagram's account, so please be careful the users can't dm you.*

To finish, you can modify the schedule's time and hours in the `client.logged_in` if.

**YOU MUST DOWNLOAD THE `BOT FOLDER` BECAUSE IT CONTAINS SOME IMPORTANT FILES**

## I hope you will find your happiness in my code !
