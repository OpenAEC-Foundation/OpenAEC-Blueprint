"""Render native-size completion contact sheets for visual review, using CairoSVG."""
from pathlib import Path
import io
import argparse
import json
import math
from functools import lru_cache
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from b2_completion import ROWS, SEMANTIC
from b2_icon_placement_refinements import ACCENT_ROLES
ROOT=Path(__file__).resolve().parents[1]


@lru_cache(maxsize=None)
def svg_master(key,size):
    return (ROOT/f'design/icon-set-b2/svg/{size}/{key}.svg').read_text(encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--from-series',type=int,default=0)
    parser.add_argument('--icons',nargs='+',help='Only rebuild sheets containing these reviewed icon IDs.')
    args=parser.parse_args()
    if args.icons:
        unknown=set(args.icons)-{row[1] for row in ROWS}
        if unknown:parser.error('Unknown icon IDs: '+', '.join(sorted(unknown)))
    themes = json.loads((ROOT/'design/ontwerp-0.4/tokens-0.4.json').read_text(encoding='utf-8'))['themes']
    font = ImageFont.truetype(str(ROOT/'assets/fonts/Inter-Regular.ttf'), 14)
    wrapfont = ImageFont.truetype(str(ROOT/'assets/fonts/Inter-Regular.ttf'), 12)
    smallfont = ImageFont.truetype(str(ROOT/'assets/fonts/Inter-Regular.ttf'), 11)
    out = ROOT/'design/icon-set-b2'
    for start in range(0, len(ROWS), 24):
        rows = ROWS[start:start+24]
        if not any(row[0]>=args.from_series for row in rows):continue
        if args.icons and not any(row[1] in args.icons for row in rows):continue
        for theme in ('dark','light'):
            for mono in (False, True):
                colors = themes[theme]['color']
                sheet = Image.new('RGB', (1120, math.ceil(len(rows)/4)*174+50), colors['frame'])
                draw = ImageDraw.Draw(sheet)
                draw.text((20,14), f'B2 · uitbreiding {start+1}–{start+len(rows)} · {theme}'+(' · monochroom' if mono else ''), font=font, fill=colors['text'])
                for idx, (_, key, label, _, _) in enumerate(rows):
                    x = (idx%4)*280
                    y = (idx//4)*174+50
                    draw.rounded_rectangle((x+8,y+5,x+272,y+168),radius=7,fill=colors['panel'],outline=colors['border-strong'])
                    if draw.textlength(label,font=font)<=244:
                        draw.text((x+20,y+15),label,font=font,fill=colors['text'])
                        key_y=y+37
                    else:
                        words=label.split(); first=''
                        while words and draw.textlength((first+' '+words[0]).strip(),font=wrapfont)<=244:
                            first=(first+' '+words.pop(0)).strip()
                        draw.text((x+20,y+12),first,font=wrapfont,fill=colors['text'])
                        draw.text((x+20,y+26),' '.join(words),font=wrapfont,fill=colors['text'])
                        key_y=y+45
                    draw.text((x+20,key_y),key,font=smallfont,fill=colors['text-secondary'])
                    for px,dx,dy in ((48,110,62),(16,58,123),(24,116,115),(32,180,107)):
                        svg=svg_master(key,16 if px==16 else 24)
                        ink=colors['text'] if mono else colors.get(SEMANTIC.get(key),colors['text'])
                        accent=ink if mono or (key in SEMANTIC and key not in ACCENT_ROLES) else colors['accent']
                        svg=svg.replace('var(--icon-accent,currentColor)',accent).replace('currentColor',ink)
                        data=cairosvg.svg2png(bytestring=svg.encode(),output_width=px,output_height=px)
                        image=Image.open(io.BytesIO(data)).convert('RGBA')
                        sheet.paste(image,(x+dx,y+dy),image)
                        if px!=48:draw.text((x+dx,y+144),str(px),font=smallfont,fill=colors['text-secondary'])
                name=f'completion-preview-{start//24+1}-{theme}'+('-mono' if mono else '')+'.png'
                sheet.save(out/name)
                print(out/name)


if __name__=='__main__':
    main()
