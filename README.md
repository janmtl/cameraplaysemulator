Camera Plays Emulator
=====================
A python app that uses the feed from a webcam to send commands to a video game emulator. The output is also automatically streamed to Twitch.tv.

Based on [WhereIsTheFish](http://github.com/catherinemoresco/whereisthefish) which has popularly implemented for [FishPlaysPokemon](http://www.twitch.tv/fishplayspokemon).

This project is in cooperation with Alex Leavitt's [uscplayspokemon](http://github.com/alexleavitt/uscplayspokemon).

Quickstart
----------
1. Make sure openCV is install on your system
2. Start up [VBA](http://visualboyadvance.net/) with your desired ROM
3. Set `Options -> Emulator -> Show speed -> None`
4. Run `python lib/run.py`