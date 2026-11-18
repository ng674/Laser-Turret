from pathlib import Path
import subprocess, re, json
root=Path(__file__).resolve().parent
exe='/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'
parts={'shared_base':1,'base':1,'leg':2,'carrier':1,'head':1,'horn_spacer':2,'spacer_core':2,'shim_05':4,'shim_10':2,'shim_15':2,'camera_post':1,'camera_pad':1,'electronics_tray':1,'tray_foot':2,'switch_cradle':1,'servo_coupon':1,'horn_coupon':1,'laser_coupon':1}
logs=[]; report=[]
for part,qty in parts.items():
 out=root/'stl'/f'{part}.stl'
 r=subprocess.run([exe,'--export-format','asciistl','-o',str(out),'-D',f'part="{part}"',str(root/'cad/main.scad')],capture_output=True,text=True)
 logs.append(part+'\n'+r.stdout+r.stderr)
 if r.returncode or 'ERROR:' in r.stderr: raise RuntimeError(logs[-1])
 points=[tuple(map(float,m)) for m in re.findall(r'vertex\s+([-\d.e+]+)\s+([-\d.e+]+)\s+([-\d.e+]+)',out.read_text())]
 lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
 assert abs(lo[2])<0.001,(part,lo)
 # Closed edge incidence check and number of connected shells.
 edges={};parent=list(range(len(points)//3))
 def find(i):
  while parent[i]!=i: parent[i]=parent[parent[i]];i=parent[i]
  return i
 for f in range(len(points)//3):
  tri=points[f*3:f*3+3]
  for a,b in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:
   e=tuple(sorted((a,b)));edges.setdefault(e,[]).append(f)
 for fs in edges.values():
  if len(fs)==2: parent[find(fs[0])]=find(fs[1])
 bad=sum(len(v)!=2 for v in edges.values());shells=len({find(i) for i in range(len(parent))})
 assert bad==0 and shells==1,(part,bad,shells)
 report.append({'part':part,'quantity':qty,'size_mm':[round(hi[i]-lo[i],2) for i in range(3)],'min_z':lo[2],'closed_edges':bad==0,'shells':shells})
(root/'VALIDATION.txt').write_text('\n'.join(logs))
(root/'mesh_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
