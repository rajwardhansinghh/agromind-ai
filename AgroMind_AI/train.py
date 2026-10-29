"""Reproduce stratified holdout evaluation; never fit preprocessing on test rows."""
import hashlib
import json
import random
from collections import defaultdict
from model import KNN, ROOT, load_rows

def evaluate():
    groups=defaultdict(list)
    for row in load_rows():
        groups[row[1]].append(row)
    rng=random.Random(42)
    train,test=[],[]
    for label in sorted(groups):
        rows=list(groups[label]);rng.shuffle(rows)
        cut=int(len(rows)*0.8)
        train.extend(rows[:cut]);test.extend(rows[cut:])
    model=KNN(train)
    confusion={label:{other:0 for other in sorted(groups)} for label in sorted(groups)}
    correct=0
    for x,label in test:
        scores,_=model.scores(x)
        prediction=max(scores,key=scores.get)
        confusion[label][prediction]+=1
        correct+=prediction==label
    metrics={'algorithm':'Standardized distance-weighted k-NN','k':9,'seed':42,'split':'80/20 stratified per crop','training_rows':len(train),'test_rows':len(test),'correct':correct,'accuracy':correct/len(test),'dataset_sha256':hashlib.sha256((ROOT/'data/crop_recommendation.csv').read_bytes()).hexdigest(),'scope':'Seven-feature classifier only. Location/season rules are not evaluated. Single random holdout; not field validation.','confusion_matrix':confusion}
    (ROOT/'models/metrics.json').write_text(json.dumps(metrics,indent=2))
    print(json.dumps({k:v for k,v in metrics.items() if k!='confusion_matrix'},indent=2))
    return metrics
if __name__=='__main__':evaluate()
