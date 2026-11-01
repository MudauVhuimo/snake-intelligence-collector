"""Dependency-free SVG plotting for observational Snake26 research."""
from html import escape

COLORS = ("#60a5fa", "#fbbf24", "#34d399", "#f472b6", "#a78bfa", "#f87171")

def xml(value):
    return escape(str(value), quote=True)

def save(path, title, parts, height=450):
    path.parent.mkdir(parents=True, exist_ok=True)
    source = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" '
              f'role="img" aria-label="{xml(title)}">'
              f'<rect width="1000" height="{height}" fill="#101b2c" rx="15"/>'
              f'<text x="30" y="40" font-size="23" font-family="sans-serif" '
              f'font-weight="bold" fill="#f8fafc">{xml(title)}</text>'
              '<g font-size="13" font-family="sans-serif" fill="#cbd5e1">'
              + "".join(parts) + '</g></svg>')
    path.write_text(source,encoding="utf-8")

def rankings(path, rows, ours):
    if not rows:
        return save(path,"Gauntlet_1 final length",['<text x="60" y="120">No trial data yet</text>'],190)
    top = sorted(rows,key=lambda x:(-x["length"],x["name"]))[:12]
    mine = next((r for r in rows if r["name"]==ours),None)
    if mine and mine not in top:
        top.append(mine)
    maximum=max(1,max(r["length"] for r in top))
    parts=['<text x="370" y="68">Shared published seed and benchmark group; one trial per bot</text>']
    for i,r in enumerate(top):
        y=88+i*29
        length=530*r["length"]/maximum
        color="#fbbf24" if r["name"]==ours else "#60a5fa"
        parts += [f'<text x="347" y="{y+15}" text-anchor="end">{xml(r["name"].split("-",1)[-1][:29])}</text>',
                  f'<rect x="364" y="{y}" width="{length:.1f}" height="20" rx="3" fill="{color}"/>',
                  f'<text x="{370+length:.1f}" y="{y+15}" fill="#fff">{r["length"]}</text>']
    save(path,"Gauntlet_1: final body length",parts,130+29*len(top))

def apples(path, rows, ours):
    if not rows:
        return save(path,"Apples versus final length",["<text x='55' y='120'>No data</text>"],200)
    x_max=max(10,max(r["food"] for r in rows)+5)
    y_max=max(5+5*x_max,max(r["length"] for r in rows)+10)
    X=lambda v:100+810*v/x_max
    Y=lambda v:387-305*v/y_max
    parts=['<line x1="100" y1="387" x2="910" y2="387" stroke="#64748b"/>',
           '<line x1="100" y1="82" x2="100" y2="387" stroke="#64748b"/>',
           f'<line x1="{X(0):.1f}" y1="{Y(5):.1f}" x2="{X(x_max):.1f}" '
           f'y2="{Y(5+5*x_max):.1f}" stroke="#34d399" stroke-dasharray="6 5" stroke-width="2"/>',
           '<text x="640" y="69" fill="#34d399">No-reset: 5 + 5 × apples</text>',
           '<text x="500" y="436" text-anchor="middle">Apples collected</text>']
    for v in range(0,x_max+1,10):
        parts.append(f'<text x="{X(v):.1f}" y="409" text-anchor="middle">{v}</text>')
    for v in range(0,y_max+1,50):
        yy=Y(v)
        parts.extend([f'<line x1="100" y1="{yy:.1f}" x2="910" y2="{yy:.1f}" stroke="#334155"/>',
                      f'<text x="84" y="{yy+4:.1f}" text-anchor="end">{v}</text>'])
    for r in rows:
        cx,cy=X(r["food"]),Y(r["length"])
        mine=r["name"]==ours
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{8 if mine else 4}" '
                     f'fill="{ "#fbbf24" if mine else "#60a5fa"}" opacity=".8">'
                     f'<title>{xml(r["name"])}: {r["food"]} apples, length {r["length"]}</title></circle>')
        if mine:
            parts.append(f'<text x="{cx+11:.1f}" y="{cy-11:.1f}" fill="#fbbf24">Our trial</text>')
    save(path,"Gauntlet_1: food versus retained growth",parts,460)

def growth(path, curves, rows, ours):
    if not curves:
        return save(path,"Gauntlet_1: recorded growth",
                    ['<text x="50" y="110">No matching full trial replay downloaded yet</text>'],190)
    ranks={r["name"]:i for i,r in enumerate(sorted(rows,key=lambda r:-r["length"]))}
    chosen=sorted(curves,key=lambda n:ranks.get(n,99999))[:6]
    if ours in curves and ours not in chosen:
        chosen[-1]=ours
    maximum=max(25,max(value for name in chosen for _,value in curves[name]))
    X=lambda turn:102+812*turn/2000
    Y=lambda v:385-294*v/maximum
    parts=['<line x1="102" y1="385" x2="914" y2="385" stroke="#64748b"/>',
           '<text x="500" y="432" text-anchor="middle">Turn (out of 2,000)</text>']
    for turn in range(0,2001,500):
        parts.append(f'<text x="{X(turn):.1f}" y="408" text-anchor="middle">{turn}</text>')
    for i,name in enumerate(chosen):
        color="#fbbf24" if name==ours else COLORS[i%len(COLORS)]
        points=" ".join(f"{X(t):.1f},{Y(length):.1f}" for t,length in curves[name])
        parts.extend([f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.6">'
                      f'<title>{xml(name)}</title></polyline>',
                      f'<text x="{140+(i%3)*280}" y="{57+(i//3)*17}" fill="{color}">'
                      f'{xml(name.split("-",1)[-1][:25])}</text>'])
    save(path,"Gauntlet_1: actual growth trajectories",parts,455)

def grouped(path,title,categories,values,names):
    high=max([values.get(g,{}).get(c,0) for g in ("Student","Benchmark") for c in categories] or [1])
    high=max(1,high*1.12)
    parts=['<line x1="100" y1="385" x2="925" y2="385" stroke="#64748b"/>',
           '<rect x="660" y="52" width="12" height="12" fill="#60a5fa"/>',
           '<text x="677" y="63">Student snakes</text>',
           '<rect x="808" y="52" width="12" height="12" fill="#fbbf24"/>',
           '<text x="825" y="63">Benchmarks</text>']
    for tick in range(5):
        level=high*tick/4
        y=385-290*tick/4
        parts.extend([f'<line x1="100" y1="{y:.1f}" x2="925" y2="{y:.1f}" stroke="#334155"/>',
                      f'<text x="87" y="{y+4:.1f}" text-anchor="end">{level:.2f}</text>'])
    for i,c in enumerate(categories):
        x=100+(i+.5)*820/len(categories)
        parts.append(f'<text x="{x:.1f}" y="409" text-anchor="middle">{xml(names.get(c,c))}</text>')
        for j,group in enumerate(("Student","Benchmark")):
            v=values.get(group,{}).get(c,0)
            h=290*v/high
            parts.append(f'<rect x="{x-27+j*29:.1f}" y="{385-h:.1f}" width="26" height="{h:.1f}" '
                         f'fill="{COLORS[j]}"><title>{xml(group)}: {v:.3f}</title></rect>')
    save(path,title,parts,455)
