from pathlib import Path
import subprocess
root=Path(__file__).resolve().parent
exe='/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD';rows=[]
for kind in ['external','head']:
 for pan in ([-45,0,45] if kind=='external' else [0]):
  for tilt in [-30,-15,0,15,30]:
   out=root/'preview'/'intersection.stl'
   if out.exists():out.unlink()
   r=subprocess.run([exe,'-o',str(out),'-D','part="none"','-D',f'check="{kind}"','-D',f'test_pan={pan}','-D',f'test_tilt={tilt}',str(root/'cad/clearance_check.scad')],capture_output=True,text=True)
   empty='Current top level object is empty' in r.stderr
   rows.append(f'{kind} pan={pan} tilt={tilt}: '+('PASS empty intersection' if empty else 'FAIL '+r.stderr))
(root/'CLEARANCE.txt').write_text('\n'.join(rows));print('\n'.join(rows))
