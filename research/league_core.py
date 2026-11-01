"""Compare real league and on-arrival results WITHOUT confusing their rankings.

Current-season catalog and official standings are used for outcome statistics.
Full replay data is counted separately, not imputed from final match summaries.
"""
from collections import Counter, defaultdict
from statistics import mean, median
from pathlib import Path
import sqlite3
from .food_race_core import group

SUITES=("910000","911000","912000")

def midranks(values):
    order=sorted(range(len(values)),key=lambda i:values[i])
    ranks=[0.0]*len(values)
    for start in range(len(values)):
        if start and values[order[start]]==values[order[start-1]]:
            continue
        stop=start+1
        while stop<len(values) and values[order[start]]==values[order[stop]]:
            stop+=1
        rank=(start+1+stop)/2
        for k in range(start,stop):
            ranks[order[k]]=rank
    return ranks

def spearman(values_x,values_y):
    if len(values_x)!=len(values_y) or len(values_x)<4:
        return None
    xx=midranks(values_x)
    yy=midranks(values_y)
    mx,my=mean(xx),mean(yy)
    denom=(sum((a-mx)**2 for a in xx)*sum((b-my)**2 for b in yy))**.5
    return round(sum((a-mx)*(b-my) for a,b in zip(xx,yy))/denom,3) if denom else None

def current_season(db):
    r=db.execute("""SELECT s.name FROM seasons s
                    JOIN standings t ON t.season_name=s.name
                    GROUP BY s.name ORDER BY s.name DESC LIMIT 1""").fetchone()
    return r[0] if r else None

def load(db,season):
    # Standings are authoritative for division rank, not a reconstructed
    # ranking from the currently indexed subset of games.
    standings={}
    for name,d,rank,points,rating in db.execute(
        """SELECT team_slug,division,division_rank,points,rating
           FROM standings WHERE season_name=?""",(season,)):
        if name and not name.startswith("~"):
            standings[name]=dict(division=d,rank=rank,points=points,rating=rating)

    trials=defaultdict(dict)
    for name,replay,place,length,food,kills in db.execute(
        """SELECT p.team_slug,m.replay_name,p.placement,p.final_length,
                  p.food_eaten,p.kills FROM matches m JOIN participants p
                  ON p.season_name=m.season_name AND p.replay_name=m.replay_name
                  WHERE m.season_name=? AND m.kind='trial'
                    AND p.team_slug NOT LIKE '~%'""",(season,)):
        key=next((k for k in SUITES if replay.endswith("/trial-"+k+".rep")),None)
        if key:
            trials[name][key]=dict(place=place,length=length,food=food,kills=kills)
    complete={}
    for name,t in trials.items():
        if len(t)!=3 or any(t[k]["place"] is None or t[k]["length"] is None for k in SUITES):
            continue
        complete[name]=dict(
            mean_place=mean(t[k]["place"] for k in SUITES),
            mean_length=mean(t[k]["length"] for k in SUITES),
            mean_food=mean(t[k]["food"] or 0 for k in SUITES),
            gauntlet_length=t["912000"]["length"],
            gauntlet_food=t["912000"]["food"],
            gauntlet_place=t["912000"]["place"])
    ranked=sorted(complete,key=lambda n:(complete[n]["mean_place"],
                                        -complete[n]["mean_length"],n))
    for pos,name in enumerate(ranked,1):
        complete[name]["trial_rank"]=pos
    return standings,complete

def match_data(db,season):
    """One row per cataloged latest-season league game and its student players."""
    matches=[]
    rows=db.execute(
        """SELECT m.replay_name,m.division,m.replay_sha256,
                  p.team_slug,p.placement,p.final_length,p.food_eaten,p.kills
           FROM matches m JOIN participants p
             ON p.season_name=m.season_name AND p.replay_name=m.replay_name
           WHERE m.season_name=? AND m.kind='league' AND m.kept=1
           ORDER BY m.replay_name""",(season,)).fetchall()
    grouped={}
    for replay,division,sha,name,place,length,food,kills in rows:
        r=grouped.setdefault(replay,dict(name=replay,division=division,
                                         downloaded=bool(sha),players=[]))
        r["players"].append(dict(name=name,student=not name.startswith("~"),
                                 placement=place,length=length,food=food,kills=kills))
    for game in grouped.values():
        humans=[p for p in game["players"] if p["student"]]
        game["humans"]=len(humans)
        game["type"]="student-only" if len(humans)==len(game["players"]) else "mixed"
        matches.append(game)
    return matches

def team_league_metrics(matches):
    per=defaultdict(list)
    for game in matches:
        humans=[p for p in game["players"] if p["student"]]
        if len(humans)<2:
            continue
        for p in humans:
            if p["placement"] is None:
                continue
            food=p["food"] if p["food"] is not None else None
            retained=(p["length"]/(5+5*food) if p["length"] is not None and
                      food is not None and 5+5*food>0 else None)
            opponents=[x for x in humans if x["name"]!=p["name"]]
            competitor_food=[x["food"] for x in opponents if x["food"] is not None]
            per[p["name"]].append(dict(
                placement=p["placement"],winner=(p["placement"]==1),
                food=food,length=p["length"],kills=p["kills"],retained=retained,
                versus_students=game["humans"]-1,
                food_edge=(food-mean(competitor_food) if food is not None and competitor_food else None),
                downloaded=game["downloaded"],type=game["type"]))
    result={}
    for team,obs in per.items():
        def avg(k):
            values=[x[k] for x in obs if x[k] is not None]
            return mean(values) if values else None
        result[team]=dict(
            league_games=len(obs),league_wins=sum(x["winner"] for x in obs),
            avg_place=avg("placement"),win_rate=avg("winner"),
            avg_food=avg("food"),avg_length=avg("length"),avg_kills=avg("kills"),
            avg_retained=avg("retained"),avg_food_edge=avg("food_edge"),
            mixed_games=sum(x["type"]=="mixed" for x in obs),
            pure_games=sum(x["type"]=="student-only" for x in obs),
            replay_games=sum(x["downloaded"] for x in obs))
    return result

def historical_catalog_coverage(db):
    return db.execute(
        """SELECT m.season_name,m.kind,
                  COUNT(DISTINCT m.replay_name),
                  SUM(CASE WHEN m.replay_sha256 IS NOT NULL THEN 1 ELSE 0 END),
                  COUNT(DISTINCT m.replay_sha256)
           FROM matches m WHERE m.kind IN ('league','trial')
           GROUP BY m.season_name,m.kind ORDER BY m.season_name DESC"""
    ).fetchall()

def build_data(db):
    season=current_season(db)
    if not season:
        return dict(season=None)
    standings,trials=load(db,season)
    matches=match_data(db,season)
    league=team_league_metrics(matches)
    divisions=defaultdict(list)
    for name,rank in standings.items():
        if rank["division"] is not None and rank["rank"] is not None:
            divisions[rank["division"]].append(name)
    top_div1=sorted(divisions[1],key=lambda n:(standings[n]["rank"],n))
    div1_observed=[n for n in top_div1 if n in trials]
    comparisons={}
    for division,names in divisions.items():
        pairs=[n for n in names if n in trials]
        comparisons[division]=dict(
            n=len(pairs),
            official_vs_trial_len=spearman([standings[n]["rank"] for n in pairs],
                                          [-trials[n]["mean_length"] for n in pairs]),
            official_vs_gauntlet_len=spearman([standings[n]["rank"] for n in pairs],
                                             [-trials[n]["gauntlet_length"] for n in pairs]),
            official_vs_trial_overall_rank=spearman([standings[n]["rank"] for n in pairs],
                                                   [trials[n]["trial_rank"] for n in pairs]))
    coverage=historical_catalog_coverage(db)
    latest_kind=Counter()
    latest_downloaded=Counter()
    for game in matches:
        key=game["type"]+" / "+str(game["humans"])+" students"
        latest_kind[key]+=1
        if game["downloaded"]:latest_downloaded[key]+=1
    return dict(season=season,standings=standings,trials=trials,
                matches=matches,league=league,comparisons=comparisons,
                div1=top_div1,latest_kind=latest_kind,
                latest_downloaded=latest_downloaded,coverage=coverage)
