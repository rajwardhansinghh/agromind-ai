"""Standardized distance-weighted k-nearest neighbours, Python standard library only."""
import csv
import heapq
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent
FEATURES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
LIMITS = [(0, 200), (0, 200), (0, 250), (0, 50), (0, 100), (0, 14), (0, 500)]
SEASONS = {
 'rice':['Kharif'], 'maize':['Kharif','Rabi'], 'chickpea':['Rabi'],
 'kidneybeans':['Rabi','Kharif'], 'pigeonpeas':['Kharif'], 'mothbeans':['Kharif'],
 'mungbean':['Kharif','Zaid'], 'blackgram':['Kharif','Zaid'], 'lentil':['Rabi'],
 'cotton':['Kharif'], 'jute':['Kharif'], 'watermelon':['Zaid'], 'muskmelon':['Zaid']}
# Illustrative regional preferences, not learned location features.
REGIONS = {
 'Madhya Pradesh':['maize','chickpea','lentil','cotton','pigeonpeas','blackgram'],
 'Maharashtra':['cotton','pigeonpeas','maize','grapes','banana','orange'],
 'Punjab':['rice','maize','cotton','chickpea'],
 'Uttar Pradesh':['rice','maize','lentil','chickpea'],
 'Gujarat':['cotton','mungbean','chickpea','banana'],
 'Rajasthan':['mothbeans','mungbean','chickpea','cotton'],
 'Other':[]}


def load_rows():
    with (ROOT/'data/crop_recommendation.csv').open(newline='') as f:
        return [(tuple(float(r[k]) for k in FEATURES), r['label']) for r in csv.DictReader(f)]


class KNN:
    def __init__(self, rows, k=9):
        self.rows = rows
        self.k = k
        self.means = [mean(x[i] for x, _ in rows) for i in range(7)]
        self.scales = [pstdev(x[i] for x, _ in rows) or 1 for i in range(7)]
        self.normalized = [(self.transform(x), label) for x, label in rows]
        groups = defaultdict(list)
        for x, label in rows:
            groups[label].append(x)
        self.profiles = {label:[(min(x[i] for x in xs),max(x[i] for x in xs)) for i in range(7)] for label,xs in groups.items()}

    def transform(self, values):
        return tuple((v-m)/s for v,m,s in zip(values,self.means,self.scales))

    def scores(self, values):
        query = self.transform(values)
        neighbours = heapq.nsmallest(self.k, ((math.dist(query,x),label) for x,label in self.normalized))
        votes = Counter()
        for distance,label in neighbours:
            votes[label] += 1/(distance+0.01)
        total = sum(votes.values())
        return {label:weight/total for label,weight in votes.items()}, neighbours[0][0]


def validate(payload):
    if not isinstance(payload,dict):
        raise ValueError('Input must be a JSON object.')
    values=[]
    for key,(low,high) in zip(FEATURES,LIMITS):
        value=payload.get(key)
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f'{key} must be a number from {low} to {high}.')
        values.append(float(value))
    if payload.get('season','Any') not in ['Any','Kharif','Rabi','Zaid']:
        raise ValueError('Choose a valid season.')
    if payload.get('state','Other') not in REGIONS:
        raise ValueError('Choose a valid state.')
    city=payload.get('city','')
    if not isinstance(city,str) or len(city)>80:
        raise ValueError('City must be text up to 80 characters.')
    return values


def recommend(model, payload):
    values=validate(payload)
    season=payload.get('season','Any')
    state=payload.get('state','Other')
    votes,distance=model.scores(values)
    ranked=[]
    for crop,base in votes.items():
        seasonal = SEASONS.get(crop)
        season_factor = 0.65 if season != 'Any' and seasonal and season not in seasonal else 1
        region_factor = 1.08 if crop in REGIONS[state] else 1
        ranked.append((base*season_factor*region_factor,crop,base,season_factor,region_factor))
    ranked.sort(reverse=True)
    results=[]
    for score,crop,base,sf,rf in ranked[:3]:
        profile=model.profiles[crop]
        reasons=[{'feature':key,'value':v,'low':round(lo,2),'high':round(hi,2),'within':lo<=v<=hi} for key,v,(lo,hi) in zip(FEATURES,values,profile)]
        results.append({'crop':crop,'score':round(100*min(score,1),1),'neighbor_support':round(100*base,1), 'season_match':sf==1,'regional_preference':rf>1,'reasons':reasons,'seasons':SEASONS.get(crop,['Perennial / varies by region'])})
    warnings=[]
    if distance>2:
        warnings.append('These inputs are far from the training examples; the recommendation may be unreliable.')
    if season!='Any' and not results[0]['season_match']:
        warnings.append('The leading crop has a season mismatch. Check the local sowing calendar.')
    if len(results)<3:
        warnings.append('Fewer than three crop classes occur among the nearest neighbours; no alternatives were invented.')
    return {'recommendations':results,'warnings':warnings,'model':'Standardized distance-weighted k-NN (k=9)', 'location':{'state':state,'city':payload.get('city','')},'season':season,'nearest_distance':round(distance,3),'notice':'Educational prototype. Scores are ranking indicators, not probabilities of successful harvest. Location and season are illustrative rules, not learned features.'}
