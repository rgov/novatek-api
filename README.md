# Novatek API for Python

I bought one of these [APEMAN 4K action cameras][az], a cheap GoPro knockoff.

![Camera][photo]

[az]: https://www.amazon.com/gp/product/B01JCESY98
[photo]: https://images-na.ssl-images-amazon.com/images/I/51YiLJNQy5L._SL500_AC_SS350_.jpg

As far as I can tell, the APEMAN is using a digital camera SoC from 
[Novatek][novatek]; I don't know who wrote the software onboard.

[novatek]: http://www.novatek.com.tw/en-global/Product/product/Index/product_1

The camera can be set to broadcast a Wi-Fi network, which allows you to use an
app like [CamKing][camking] to control it remotely. The app allows you to start
and stop recording, take photos, and change some configuration settings.

[camking]: https://itunes.apple.com/us/app/camking/id1205765256?mt=8

The app communicates to an HTTP endpoint at http://192.168.1.254, which also
provides a user interface for uploading and downloading files from the SD card.
There is also a streaming video feed available at http://192.168.1.254:8192.

This repo contains `novatek.py`, a *very* crummy wrapper around the HTTP API to
allow you to do things like change configuration settings and list files. The
behavior was reverse engineered from the iOS and Android versions of CamKing.

There should be other functions that I have not exposed yet. Most of the methods
do not return useful values, or do any error checking at all.

A much nicer project that works with a very similar camera is over at Steven
Hiscock's [yidashcam](https://github.com/kwirk/yidashcam).
