import random
import json
import colorsys

def get_n_colors(num):
    hls_colors, i, step = [], 0, 360 / num
    while i < 360:
        h, s, l = i, 90 + random.random() * 10, 50 + random.random() * 10
        hls_colors.append([h / 360, l / 100, s / 100])
        i += step
    rgb_colors = [colorsys.hls_to_rgb(h, l, s) for h, l, s in hls_colors]
    rgb_colors = [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in rgb_colors]
    return rgb_colors

if __name__ == '__main__':
    rgb_colors = get_n_colors(63)
    with open('colors.json', 'w') as f:
        json.dump(dict(zip(range(1, 64), rgb_colors)), f)