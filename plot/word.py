# -*- coding: utf-8 -*-

import matplotlib.pyplot as plot
import matplotlib.font_manager
import filepickle
import numpy as np


word_embed_fp = 'spike/garbage/embed.dump'
reduced_word_fp = 'spike/garbage/rword.dump'

c = filepickle.load(word_embed_fp)
wlist = filepickle.load(reduced_word_fp)


nword = len(wlist)


prop = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')

fig, axes = plot.subplots(figsize=(5, 5))
xmin, xmax = min(c[:, 0]), max(c[:, 0])
ymin, ymax = min(c[:, 1]), max(c[:, 1])
axes.set_xlim(xmin, xmax)
axes.set_ylim(ymin, ymax)

#plot.scatter(c[:, 0], c[:, 1], cmap='rainbow')

for i in range(500):
    plot.text(
        x=c[i, 0],
        y=c[i, 1],
        s=wlist[i],
        horizontalalignment='center',
        verticalalignment='center', fontproperties=prop)

plot.show()
