from pathlib import Path
import re, math, struct, json, shutil
src=Path(__file__).resolve().parent.parent/'stl'
out=Path(__file__).resolve().parent
# Pre-layout angles only. Provider must validate resin supports and orientation.
items=[('shared_base',1,0),('electronics_tray',1,0),('base',1,0),('camera_pad',1,0),('camera_post',1,0),('carrier',1,0),('leg',2,0),('head',1,0),('horn_spacer',2,0),('tray_foot',2,0),('switch_cradle',1,0)]
def vertices(name,angle):
 v=[tuple(map(float,m)) for m in re.findall(r'vertex\s+([-\d.e+]+)\s+([-\d.e+]+)\s+([-\d.e+]+)',(src/(name+'.stl')).read_text())]
 c=math.cos(math.radians(angle));s=math.sin(math.radians(angle))
 v=[(x,y*c-z*s,y*s+z*c) for x,y,z in v]
 lo=[min(p[i] for p in v) for i in range(3)]
 return [tuple(p[i]-lo[i] for i in range(3)) for p in v]
parts=[]
for name,qty,a in items:
 for n in range(qty):
  v=vertices(name,a);dims=[max(p[i] for p in v) for i in range(3)]
  parts.append(dict(name=name,copy=n+1,angle=a,v=v,dims=dims))
# MaxRects packing with a 10 mm inter-part gap, 8 mm bed margin.
W,H=280,280;gap=22
bins=[]
for p in sorted(parts,key=lambda p:p['dims'][0]*p['dims'][1],reverse=True):
 choices=[]
 for bi,b in enumerate(bins):
  for ri,(x,y,w,h) in enumerate(b['free']):
   for turn in [False,True]:
    dx,dy=(p['dims'][1],p['dims'][0]) if turn else p['dims'][:2]
    if dx<=w+1e-6 and dy<=h+1e-6:choices.append((min(w-dx,h-dy),max(w-dx,h-dy),bi,x,y,dx,dy,turn))
 if not choices:
  bins.append({'free':[(0,0,W,H)],'parts':[]})
  b=bins[-1];bi=len(bins)-1;x=y=0;dx,dy=p['dims'][:2];turn=False
  assert dx<=W and dy<=H,p['name']
 else:
  _,_,bi,x,y,dx,dy,turn=min(choices);b=bins[bi]
 p.update(x=x,y=y,dx=dx,dy=dy,turn=turn);b['parts'].append(p)
 used=(x-gap,y-gap,x+dx+gap,y+dy+gap);new=[]
 for fx,fy,fw,fh in b['free']:
  x1,y1,x2,y2=used;rx=fx+fw;ry=fy+fh
  if x1>=rx or x2<=fx or y1>=ry or y2<=fy:new.append((fx,fy,fw,fh));continue
  if x1>fx:new.append((fx,fy,x1-fx,fh))
  if x2<rx:new.append((x2,fy,rx-x2,fh))
  if y1>fy:new.append((fx,fy,fw,y1-fy))
  if y2<ry:new.append((fx,y2,fw,ry-y2))
 b['free']=[r for i,r in enumerate(new) if not any(i!=j and r[0]>=q[0] and r[1]>=q[1] and r[0]+r[2]<=q[0]+q[2] and r[1]+r[3]<=q[1]+q[3] for j,q in enumerate(new))]
report=[]
for bi,b in enumerate(bins,1):
 vs=[]
 for p in b['parts']:
  for vx,vy,vz in p['v']:
   if p['turn']:vx,vy=p['dims'][1]-vy,vx
   vs.append((vx+p['x']+8,vy+p['y']+8,vz))
 for i,p in enumerate(b['parts']):
  for q in b['parts'][i+1:]:
   assert p['x']+p['dx']+gap<=q['x']+1e-5 or q['x']+q['dx']+gap<=p['x']+1e-5 or p['y']+p['dy']+gap<=q['y']+1e-5 or q['y']+q['dy']+gap<=p['y']+1e-5
 filename=f'group_{bi:02d}.stl'
 with (out/filename).open('wb') as f:
  f.write(b'V6 grouped separated parts; supports required'.ljust(80,b' '));f.write(struct.pack('<I',len(vs)//3))
  for i in range(0,len(vs),3):
   a,bv,c=vs[i:i+3];u=[bv[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
   n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);length=math.sqrt(sum(t*t for t in n));n=tuple(t/length for t in n) if length else (0,0,0)
   f.write(struct.pack('<12fH',*n,*a,*bv,*c,0))
 bounds=[max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3)]
 report.append(dict(file=filename,size_mm=[round(d,2) for d in bounds],parts=[{k:p[k] for k in ['name','copy','angle','turn','x','y','dx','dy']} for p in b['parts']]))

(out/'layout_report.json').write_text(json.dumps(report,indent=2))
for r in report:print(r['file'],r['size_mm'],[p['name'] for p in r['parts']])
