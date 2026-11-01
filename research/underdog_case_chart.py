"""Visualize two *observed* underdog food races (board path and distance timeline).

The grid is toroidal: apparent long jumps across a board edge are NOT drawn as
straight lines. The displayed head trajectories are from real replay frames.
"""
from html import escape
from pathlib import Path
import argparse
import json

def label(value):
    return escape(str(value),quote=True)

def chart_case(case: dict, path: Path):
    trace=case["trace"]
    if not trace:
        raise ValueError("No observed trace")
    x0,y0,cell=48,64,10
    extent=35*cell
    content=[
        f'<rect x="{x0}" y="{y0}" width="{extent}" height="{extent}" fill="#17243b" stroke="#64748b"/>',
        '<text x="470" y="71" font-size="18" fill="#f8fafc">Distance to the same apple</text>',
        '<text x="470" y="91" font-size="12" fill="#94a3b8">Lower = closer; gaps indicate death or missing position</text>'
    ]
    for n in range(0,36,5):
        xx=x0+n*cell
        yy=y0+n*cell
        content.extend([f'<line x1="{xx}" y1="{y0}" x2="{xx}" y2="{y0+extent}" stroke="#253753"/>',
                        f'<line x1="{x0}" y1="{yy}" x2="{x0+extent}" y2="{yy}" stroke="#253753"/>'])
    def draw_route(field,color):
        pts=[(p["t"],p[field]) for p in trace if p.get(field) is not None]
        if not pts:
            return
        for (t,a),(u,b) in zip(pts,pts[1:]):
            if u!=t+1: continue
            dx,dy=abs(a[0]-b[0]),abs(a[1]-b[1])
            if dx+dy!=1: continue   # Never draw wraparound teleport lines.
            content.append(f'<line x1="{x0+cell*(a[0]+.5):.1f}" y1="{y0+cell*(a[1]+.5):.1f}" '
                           f'x2="{x0+cell*(b[0]+.5):.1f}" y2="{y0+cell*(b[1]+.5):.1f}" '
                           f'stroke="{color}" stroke-width="3.3"/>')
        for _,pos in pts[::max(1,len(pts)//15)]:
            content.append(f'<circle cx="{x0+cell*(pos[0]+.5):.1f}" '
                           f'cy="{y0+cell*(pos[1]+.5):.1f}" r="2.9" fill="{color}"/>')
        first=pts[0][1]
        content.append(f'<circle cx="{x0+cell*(first[0]+.5):.1f}" '
                       f'cy="{y0+cell*(first[1]+.5):.1f}" r="6" '
                       f'fill="none" stroke="{color}" stroke-width="2"/>')
    draw_route("spos","#55b7ff")
    draw_route("bpos","#f9bd55")
    food=case["food"]
    fx=x0+cell*(food[0]+.5)
    fy=y0+cell*(food[1]+.5)
    content.append(f'<rect x="{fx-5}" y="{fy-5}" width="10" height="10" rx="2" '
                   'fill="#4adeb1" stroke="#f8fafc" stroke-width="1.5"/>')
    left,right,top,bottom=480,946,130,373
    max_time=max(1,trace[-1]["t"]-trace[0]["t"])
    max_d=max(1,max([v for p in trace for v in (p.get("sd"),p.get("bd")) if v is not None]+[1]))
    X=lambda t:left+(right-left)*(t-trace[0]["t"])/max_time
    Y=lambda d:bottom-(bottom-top)*d/max_d
    content.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#94a3b8"/>')
    for d in range(0,max_d+1,5):
        yy=Y(d)
        content.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{right}" y2="{yy:.1f}" stroke="#334155"/>')
        content.append(f'<text x="{left-12}" y="{yy+4:.1f}" text-anchor="end" fill="#cbd5e1">{d}</text>')
    for field,color in (("sd","#55b7ff"),("bd","#f9bd55")):
        prior=None
        for p in trace:
            val=p.get(field)
            if val is not None and prior is not None and p["t"]==prior["t"]+1:
                content.append(f'<line x1="{X(prior["t"]):.1f}" y1="{Y(prior[field]):.1f}" '
                               f'x2="{X(p["t"]):.1f}" y2="{Y(val):.1f}" '
                               f'stroke="{color}" stroke-width="2.6"/>')
            prior=p if val is not None else None
    content.extend([
        f'<text x="{left}" y="{bottom+24}" fill="#cbd5e1">First visible (turn {trace[0]["t"]})</text>',
        f'<text x="{right}" y="{bottom+24}" text-anchor="end" fill="#cbd5e1">Capture (+{case["duration"]} turns)</text>',
        '<rect x="480" y="416" width="13" height="13" fill="#55b7ff"/>',
        f'<text x="500" y="428" fill="#cbd5e1">Student: {label(case["student"].split("-",1)[-1])}</text>',
        '<rect x="740" y="416" width="13" height="13" fill="#f9bd55"/>',
        f'<text x="760" y="428" fill="#cbd5e1">Nearest: {label(case["nearest_benchmark"])}</text>',
        f'<text x="48" y="437" fill="#cbd5e1">Initial food distance: student {case["initial_student_distance"]}, '
        f'benchmark {case["initial_benchmark_distance"]} cells</text>',
    ])
    title=f"Observed underdog capture: {case['student'].split('-',1)[-1]} vs {case['nearest_benchmark']}"
    source=('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 465" role="img" '
            f'aria-label="{label(title)}">'
            '<rect width="1000" height="465" fill="#0e192a" rx="15"/>'
            f'<text x="40" y="34" font-size="21" font-family="sans-serif" fill="#f8fafc">{label(title)}</text>'
            '<g font-family="sans-serif" font-size="12">'+''.join(content)+'</g></svg>')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(source,encoding="utf-8")

def build(data_dir: Path):
    cases=json.loads((data_dir/"reports"/"underdog_examples.json").read_text(encoding="utf-8"))
    folder=data_dir/"reports"/"charts"
    selected=cases[:1]
    alt=next((c for c in cases if c["nearest_benchmark"]=="~gauntlet_1"),None)
    if alt and alt not in selected:
        selected.append(alt)
    for i,case in enumerate(selected,1):
        chart_case(case,folder/f"underdog_case_{i}.svg")
    return len(selected)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,default=Path("data"))
    args=p.parse_args()
    print("Generated",build(args.data_dir),"observed snake-head spatial diagrams.")

if __name__=="__main__":
    main()
