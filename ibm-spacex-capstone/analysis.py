from pathlib import Path
import pandas as pd, numpy as np, json, sqlite3
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score,recall_score,f1_score
P=Path(__file__).parent
D=pd.read_csv(P/'data/dataset_part_2.csv'); X=pd.read_csv(P/'data/dataset_part_3.csv');y=D.Class
tr,te=train_test_split(np.arange(len(y)),test_size=.2,random_state=2,stratify=y)
models=[('Logistic regression',LogisticRegression(max_iter=3000),{'model__C':[.01,.1,1,10]}),('SVM',SVC(),{'model__C':[.1,1,10],'model__kernel':['linear','rbf'],'model__gamma':['scale',.01,.1]}),('Decision tree',DecisionTreeClassifier(random_state=2),{'model__max_depth':[2,3,4,6,None],'model__min_samples_leaf':[1,2,4]}),('KNN',KNeighborsClassifier(),{'model__n_neighbors':[3,5,7,9],'model__p':[1,2]})]
results=[]; fitted={}
for name,m,grid in models:
 g=GridSearchCV(Pipeline([('scale',StandardScaler()),('model',m)]),grid,cv=StratifiedKFold(5,shuffle=True,random_state=2),scoring='accuracy',n_jobs=1)
 g.fit(X.iloc[tr],y.iloc[tr]);p=g.predict(X.iloc[te]);fitted[name]=g
 results.append(dict(name=name,cv=float(g.best_score_),test=float(accuracy_score(y.iloc[te],p)),precision=float(precision_score(y.iloc[te],p)),recall=float(recall_score(y.iloc[te],p)),f1=float(f1_score(y.iloc[te],p)),cm=confusion_matrix(y.iloc[te],p).tolist(),params=g.best_params_))
best=max(results,key=lambda z:z['cv']);bm=fitted[best['name']]
temporal=GridSearchCV(bm.estimator,bm.param_grid,cv=StratifiedKFold(5,shuffle=True,random_state=2),n_jobs=1).fit(X.iloc[:72],y.iloc[:72])
sql=pd.read_csv(P/'data/Spacex.csv');sql['Landing_Outcome']=sql.Landing_Outcome.str.strip(); sql['Mission_Outcome']=sql.Mission_Outcome.str.strip(); con=sqlite3.connect(':memory:');sql.to_sql('launches',con,index=False)
queries={
'sites':'SELECT DISTINCT Launch_Site FROM launches ORDER BY Launch_Site',
'ccaf_first5':"SELECT Date, Launch_Site, Payload FROM launches WHERE Launch_Site LIKE 'CCA%' LIMIT 5",
'nasa_payload':"SELECT SUM(PAYLOAD_MASS__KG_) AS kg FROM launches WHERE Customer='NASA (CRS)'",
'f9v11_average':"SELECT AVG(PAYLOAD_MASS__KG_) AS kg FROM launches WHERE Booster_Version LIKE 'F9 v1.1%'",
'first_ground':"SELECT MIN(Date) AS date FROM launches WHERE Landing_Outcome='Success (ground pad)'",
'drone_4_6t':"SELECT Booster_Version FROM launches WHERE Landing_Outcome='Success (drone ship)' AND PAYLOAD_MASS__KG_>4000 AND PAYLOAD_MASS__KG_<6000",
'mission_outcomes':'SELECT Mission_Outcome, COUNT(*) AS n FROM launches GROUP BY Mission_Outcome',
'max_payload':"SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM launches WHERE PAYLOAD_MASS__KG_=(SELECT MAX(PAYLOAD_MASS__KG_) FROM launches)",
'failures_2015':"SELECT Date, Booster_Version, Launch_Site FROM launches WHERE Date LIKE '2015%' AND Landing_Outcome='Failure (drone ship)'",
'landing_rank':"SELECT Landing_Outcome,COUNT(*) AS n FROM launches WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY n DESC"}
sqlout={k:pd.read_sql_query(q,con).to_dict('records') for k,q in queries.items()}
(P/'queries.sql').write_text('\n\n'.join('-- '+k+'\n'+q+';' for k,q in queries.items()))
site=D.groupby('LaunchSite').Class.agg(['sum','count','mean']).reset_index();year=D.groupby(D.Date.str[:4]).Class.agg(['sum','count','mean']).reset_index();orb=D.groupby('Orbit').Class.agg(['sum','count','mean']).reset_index()
dash=pd.read_csv(P/'data/spacex_launch_dash.csv'); ds=dash.groupby('Launch Site')['class'].agg(['sum','count','mean']).reset_index()
geo=pd.read_csv(P/'data/spacex_launch_geo.csv')
res=dict(n=len(D),success=int(y.sum()),site=site.to_dict('records'),year=year.to_dict('records'),orbit=orb.to_dict('records'),models=results,best=best,temporal=float(temporal.score(X.iloc[72:],y.iloc[72:])),sql=sqlout,dash=ds.to_dict('records'),geosites=geo.groupby('Launch Site').agg(Lat=('Lat','first'),Long=('Long','first'),success=('class','sum'),n=('class','size')).reset_index().to_dict('records'),dates=[D.Date.min(),D.Date.max()],train=len(tr),test=len(te),test_positive=int(y.iloc[te].sum()),payload={str(k):v for k,v in D.groupby(pd.cut(D.PayloadMass,[0,4000,8000,16000])).Class.agg(['count','mean']).to_dict('index').items()})
(P/'results.json').write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
