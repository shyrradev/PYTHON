from pathlib import Path
import math,pandas as pd,folium
from folium.plugins import MarkerCluster
P=Path(__file__).parent
D=pd.read_csv(P/'data/spacex_launch_geo.csv')
m=folium.Map([32,-99],zoom_start=4,tiles='OpenStreetMap')
cluster=MarkerCluster(name='Launch records').add_to(m)
for _,r in D.iterrows():
 folium.CircleMarker([r.Lat,r.Long],radius=7,color='green' if r['class']==1 else 'red',fill=True,fill_opacity=.8,popup=f"Flight {r['Flight Number']}, {r['Launch Site']}, class {r['class']}").add_to(cluster)
for site,g in D.groupby('Launch Site'):
 r=g.iloc[0];folium.CircleMarker([r.Lat,r.Long],radius=12,color='#1455b8',weight=3,fill=False,tooltip=f"{site}: {int(g['class'].sum())}/{len(g)} successful").add_to(m)
a=D[D['Launch Site']=='CCAFS LC-40'].iloc[0];b=D[D['Launch Site']=='KSC LC-39A'].iloc[0]
p1=[a.Lat,a.Long];p2=[b.Lat,b.Long]
phi1,phi2=map(math.radians,[a.Lat,b.Lat]);dphi=phi2-phi1;dl=math.radians(b.Long-a.Long)
km=6371*2*math.asin(math.sqrt(math.sin(dphi/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2))
folium.PolyLine([p1,p2],color='blue',weight=4,tooltip=f'Pad-to-pad distance: {km:.2f} km').add_to(m)
folium.Marker([(a.Lat+b.Lat)/2,(a.Long+b.Long)/2],icon=folium.DivIcon(html=f'<div style="font: bold 17px Arial;background:white;border:1px solid navy;width:265px;padding:6px">LC-40 to LC-39A: {km:.2f} km</div>')).add_to(m)
folium.LayerControl().add_to(m);m.save(str(P/'launch_map.html'))
print('Generated map with 56 launch records. Pad-to-pad distance:',round(km,2),'km')
