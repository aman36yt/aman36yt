"""Generate original profile SVGs. Python standard library only."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
THEMES = {'dark': ('#0d1117', '#e6edf3', '#9da7b5', '#aa9bef', '#252d3a'),
          'light': ('#faf9ff', '#242238', '#625f75', '#7053bd', '#dfdaed')}

def text(x,y,value,size=16,color=None):
    return f'<text x="{x}" y="{y}" font-size="{size}"'+(f' fill="{color}"' if color else '')+f'>{escape(str(value))}</text>'

def svg(theme,w,h,body):
    bg,fg,muted,accent,border=THEMES[theme]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{bg}" stroke="{border}"/><g fill="{fg}" font-family="monospace">{body}</g></svg>'

def write(name,theme,w,h,body):
    (OUT / f'{name}-{theme}.svg').write_text(svg(theme,w,h,body), encoding='utf-8')

def api(path):
    headers={'Accept':'application/vnd.github+json','User-Agent':'aman-profile-generator'}
    if os.getenv('GH_TOKEN'):
        headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com'+path,headers=headers), timeout=30) as response:
        return json.load(response)

def fetch(username):
    user=api('/users/'+username)
    repos=[]
    page=1
    while True:
        batch=api(f'/users/{username}/repos?per_page=100&page={page}&type=owner')
        repos.extend(batch)
        if len(batch)<100:
            break
        page+=1
    original=[r for r in repos if not r['fork']]
    return {'repos':len(repos),'followers':user['followers'],
            'stars':sum(r['stargazers_count'] for r in original),
            'languages':dict(Counter(r['language'] for r in original if r['language'])),
            'updated':datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')}

def generate(stats=None):
    for theme,(_,fg,muted,accent,border) in THEMES.items():
        body=''.join(f'<circle cx="{30+i*22}" cy="27" r="6" fill="{c}"/>' for i,c in enumerate(['#ff6b7a','#f5c66e','#73d6ae']))
        body+=text(116,33,'aman@github: ~/profile',14,muted)
        body+=f'<path d="M1 52H899" stroke="{border}"/>'
        body+=text(34,92,'$ ./profile.sh --live',17,accent)
        body+=text(34,146,'AMAN',48,fg)
        body+=text(36,180,'Full-stack developer / Curious builder',20,accent)
        for y,label,value in [(228,'stack','Node.js • Express • MongoDB • MySQL'),(260,'building','NUVORA / Care-via / CropGuard'),(292,'learning','Java + data structures & algorithms')]:
            body+=text(36,y,label,15,muted)+text(164,y,value,15)
        body+=text(36,340,'> Turning ideas into working applications',16,accent)
        body+=f'<rect x="450" y="326" width="9" height="18" fill="{accent}"><animate attributeName="opacity" values="1;0;1" dur="1.3s" repeatCount="indefinite"/></rect>'
        write('banner',theme,900,370,body)
        for name,title,lines in [('skills','01 / BUILD TOOLKIT',['HTML • CSS • JavaScript','Node.js • Express • EJS','MongoDB • MySQL','Bootstrap • Tailwind CSS']),('focus','02 / NEXT CHAPTER',['Java + DSA practice','API design + authentication','AI-powered applications','Clean code + useful interfaces'])]:
            body=text(26,40,title,17,accent)
            body+=''.join(text(26,84+i*33,line,15) for i,line in enumerate(lines))
            write(name,theme,440,215,body)
        body=text(28,42,'GITHUB / PUBLIC SNAPSHOT',18,accent)
        if stats is None:
            body+=text(28,95,'Waiting for the first stats update.',16)
            body+=text(28,134,'Run the Update profile workflow.',14,muted)
        else:
            for x,label,key in [(28,'PUBLIC REPOS','repos'),(210,'STARS*','stars'),(385,'FOLLOWERS','followers')]:
                body+=text(x,100,stats[key],34,accent)+text(x,130,label,12,muted)
            body+=text(28,163,'*Stars on owned, non-fork repositories',12,muted)
            body+=text(28,188,'Updated '+stats['updated'],12,muted)
        write('stats',theme,590,215,body)
        body=text(28,40,'LANGUAGES / REPOSITORY COUNT',17,accent)
        if stats is None:
            body+=text(28,88,'Available after the first update.',15,muted)
        else:
            langs=sorted(stats['languages'].items(),key=lambda x:(-x[1],x[0]))[:5]
            if not langs:
                body+=text(28,88,'No public language data yet.',15,muted)
            for i,(language,count) in enumerate(langs):
                y=80+i*34
                body+=text(28,y,language,14)+f'<rect x="170" y="{y-12}" rx="4" width="{max(2,320*count/max(c for _,c in langs))}" height="12" fill="{accent}"/>'+text(512,y,count,14)
        body+=text(28,268,'Primary language per owned non-fork repo; top 5.',12,muted)
        write('languages',theme,590,290,body)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--fetch',action='store_true')
    parser.add_argument('--username',default='aman36yt')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9-]+',args.username):
        parser.error('Invalid GitHub username')
    # Fetch all data before writing; failures preserve the previous cards.
    generate(fetch(args.username) if args.fetch else None)
