# -*- coding: utf-8 -*-
from espeak import espeak

espeak.set_voice("zh")

espeak.synth("世界，你好！")

while espeak.is_playing:
	pass
