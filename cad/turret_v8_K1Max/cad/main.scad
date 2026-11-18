// V8 K1 Max filament-print revision, based on manufacturer STEP measurements. Provisional physical fit.
// Units mm. Z=0 in every individual STL. See README before full printing.
part="assembly";
$fn=48;
pan=0; tilt=0;
// Official ST3215-HS outline drawing; dimensions in reference/servo_dimensions.jpg.
body_l=45.22; body_w=24.72; body_h=32;
axis_offset=10.11;
// Case mounting holes relative to output axis. Hole thread/depth not specified by drawing.
case_holes=[[8.30,-10.25],[8.30,10.25],[29,-10.25],[29,10.25]];
case_screw_clearance=2.8; // washer-bearing slots for supplied small self-tapping screws
horn_radius=7; horn_hole=3.4; horn_gap=10; // printed clearance accommodates multiple fasteners; horn thread still unverified
horn_face=3.2; // STEP: driven horn outer face 9.6 minus front mounting pads 6.4
spacer_h=horn_gap-horn_face;
clearance=0.5;
base_thickness=8;
camera_x=125;
laser_d=10.5; laser_clearance=0.6;
// Generic tape/tie mounting avoids guessing PCB hole patterns.
tray_x=60; tray_y=110;
module plate(w,d,t){r=min(2,w/4,d/4);linear_extrude(t) offset(r=r) square([w-2*r,d-2*r],center=true);}
module hole(d,h){translate([0,0,-0.1]) cylinder(d=d,h=h+0.2);}
module slot(l,d,h){hull() for(x=[-(l-d)/2,(l-d)/2]) translate([x,0,0]) hole(d,h);}
// Mount against servo front face, leaving circular horn free to turn.
module servo_cut(t){
 hole(22,t);
 for(p=case_holes) translate([p[0],p[1],0]) {
  // +/- 0.6 mm adjustment in both directions; use washers under screw heads.
  hull() for(x=[-0.6,0.6],y=[-0.6,0.6]) translate([x,y,0]) hole(case_screw_clearance,t);
  // Recess leaves a 2 mm printed web in the nominal 5 mm flange.
  translate([0,0,2]) hull() for(x=[-0.6,0.6],y=[-0.6,0.6]) translate([x,y,0]) hole(5.5,t-2);
 }
}
module horn_spacer(h=spacer_h){difference(){cylinder(d=19,h=h);horn_cut(h);}}
module horn_cut(t){
 hole(8,t); // retaining-screw tool access
 for(a=[0:90:270]) rotate([0,0,a]) translate([horn_radius,0,0]) hole(horn_hole,t);
}
// Flat deck + two separately printed bolt-on legs avoids tall support structures.
module base(){difference(){plate(110,86,5);servo_cut(5);
 for(x=[-46,46],y=[-30,30]) translate([x,y,0]) hole(3.4,5);
}}
module leg(){difference(){union(){plate(18,80,5);translate([0,0,5]) plate(8,48,40);translate([0,0,45]) plate(18,80,5);}
 for(y=[-30,30]) translate([0,y,0]) hole(3.4,50);
 for(y=[-34,34]) translate([0,y,0]) hole(4.5,5);
}}
// L bracket: horizontal pan horn interface, vertical tilt servo flange.
module carrier(){difference(){union(){plate(66,76,5);translate([-31,-38,0]) cube([5,76,64]);
 for(y=[26,32]) hull(){translate([-29,y,3]) cube([19,3,2]);translate([-29,y,3]) cube([3,3,22]);}}
 horn_cut(5);
 translate([-31.1,0,39]) rotate([0,90,0]) rotate([0,0,90]) servo_cut(5.2);
}}
// Open semicircular saddle for Quarton 10.5 x 19 mm barrel; two ties retain it.
// No metal contacts the electrically live laser case. Optical axis points -Y.
module head(){difference(){union(){
 plate(30,30,4);
 translate([0,-25,0]) plate(28,24,4);
 translate([-10,-36,3.8]) cube([20,22,10.2]);
 }
 horn_cut(4);
 translate([0,-13,14]) rotate([90,0,0]) cylinder(d=laser_d+laser_clearance,h=25);
 for(x=[-11,11],y=[-30,-21]) translate([x,y,0]) rotate([0,0,90]) slot(5,3.8,4);
}}
module laser_coupon(){difference(){cube([20,12,10]);
 translate([10,-0.1,10]) rotate([-90,0,0]) cylinder(d=laser_d+laser_clearance,h=12.2);
}}
// One-piece foundation joins both assemblies. Underside head recesses keep it flat.
module shared_base(){difference(){
 union(){translate([60,0,0]) plate(230,100,base_thickness);
 translate([65,0,0]) plate(20,100,12);}
 for(y=[-30,30]) translate([65,y,0]) {hole(4.5,12);hole(8.5,4);}
 for(x=[-46,46],y=[-34,34]) translate([x,y,0]) {
 hole(4.5,base_thickness); hole(8.5,4); // M4 socket/button head clearance, verify actual head
 }
 for(y=[-20,20]) translate([camera_x,y,0]) {
 hole(3.4,base_thickness); hole(6.5,3.3); // M3 head recess
 }
 // Optional table/board attachment slots outside the towers.
 for(x=[-25,145],y=[-43,43]) translate([x,y,0]) slot(16,4.5,base_thickness);
}}
// Open centre leaves tripod screw access. Rear cable is outside both pillars.
// Resin-bed split with a bolted 20 mm lap; 0.2 mm vertical assembly clearance.
module base_left(){intersection(){shared_base();union(){
 translate([-100,-100,0]) cube([155,200,20]);
 translate([55,-100,0]) cube([20,200,6]);}}}
module base_right(){intersection(){shared_base();union(){
 translate([75,-100,0]) cube([200,200,20]);
 translate([55,-100,6.2]) cube([20,200,20]);}}}
module camera_post(){difference(){union(){
 plate(30,64,5);
 for(y=[-28,28]) translate([0,y,5]) plate(12,8,100);
 translate([0,0,105]) plate(30,64,5);
 }
 for(y=[-18,18]) translate([0,y,105]) hole(3.4,5);
 for(y=[-20,20]) hole_at([0,y,0],3.4,5);
 // Screw head / driver opening through top bridge.
 translate([0,0,105]) slot(26,16,5);
}}
module hole_at(p,d,h){translate(p) hole(d,h);}
module camera_pad(){difference(){plate(100,78,5);
 slot(20,6.8,5); // optional 1/4-20 screw, if later purchased
 for(y=[-18,18]) translate([0,y,0]) hole(3.4,5);
 // 12 mm wide strap slots; straps secure the folding clip, not the lens.
 for(x=[-33,33]) translate([x,0,0]) rotate([0,0,90]) slot(44,12,5);
 // Rear USB lead tie anchor.
 for(x=[-8,8]) translate([x,32,0]) slot(6,3.8,5);
}}
// 200 x 130 overall: attached rear tray for breadboard, boards and connectors.
// Flat electronics panel: no raised rails, ledges or side walls.
// Entire underside is coplanar; print this face directly on the FDM bed.
module electronics_tray(){difference(){union(){
 plate(200,120,4);
 for(x=[-85,85]) translate([x,-62,0]) plate(20,16,4);
 }
 for(x=[-85,85]) translate([x,-67,0]) hole(4.5,4);
 for(x=[-85,85]) translate([x,45,0]) hole(3.4,4);
 for(x=[-75,-50,-25,0,25,50,75],y=[-45,0,45])
 translate([x,y,0]) slot(9,3.8,4);
}}
module tray_foot(){difference(){cylinder(d=16,h=8);hole(3.4,8);hole(6.5,3.3);}}
// Separate tape-mounted bracket: purchased switch can be cable-tied into cradle.
// Deliberately no unverified snap-fit cutout. Terminals remain accessible behind.
module switch_cradle(){difference(){union(){
 plate(46,40,4);
 for(x=[-21,21]) translate([x,0,4]) plate(4,40,22);
 }
 for(x=[-21,21],y=[-12,12]) translate([x,y,15]) rotate([0,90,0])
 cylinder(d=4,h=8,center=true);
}}
module servo_proxy(){color("#343a40") translate([body_l/2-axis_offset,0,-body_h/2]) cube([body_l,body_w,body_h],center=true);color("silver") cylinder(d=19.2,h=horn_face);}
module assembly(){
 color("#48799a") shared_base();
 translate([0,0,base_thickness]) {
 color("#48799a") {translate([0,0,50]) base();for(x=[-46,46]) translate([x,0,0]) leg();}
 translate([0,0,50]) servo_proxy();
 color("silver") translate([0,0,50+horn_face]) horn_spacer();
 translate([0,0,50+horn_gap]) rotate([0,0,pan]) {
 color("#e8a34b") carrier();
 color("silver") translate([-31+horn_face,0,39]) rotate([0,90,0]) horn_spacer();
 translate([-31,0,39]) rotate([0,90,0]) rotate([0,0,90]) servo_proxy();
 translate([-31+horn_gap,0,39]) rotate([0,90,0]) rotate([0,0,tilt]) {color("#e8a34b") head();color("#b6b6b6") translate([0,-16,14]) rotate([90,0,0]) cylinder(d=laser_d,h=19);}
 }
 translate([camera_x,0,0]) {color("#48799a") {camera_post();translate([0,0,110]) camera_pad();}
 // Full camera+clip envelope, not exact folding geometry.
 color([0.18,0.2,0.23,0.65]) translate([0,0,115+43.3/2]) cube([94,71,43.3],center=true);
 color("#80cbdc") translate([0,-36,145]) rotate([90,0,0]) cylinder(d=13,h=3);}
}
 color("#48799a") translate([tray_x,tray_y,8]) electronics_tray();
 for(x=[-85,85]) color("#48799a") translate([tray_x+x,tray_y+45,0]) tray_foot();
 color("#48799a") translate([-12,75,12]) switch_cradle();
 // Breadboard occupies left tray area; Pico and Pololu mount on it.
 color("#e4e1ce") translate([48,125,18]) cube([165,56,12],center=true);
 color("#356a43") translate([130,72,14]) cube([33,42,4],center=true);
}
if(part=="assembly") assembly();
else if(part=="base") base();
else if(part=="leg") translate([0,0,9]) rotate([0,90,0]) leg();
else if(part=="carrier") carrier();
else if(part=="horn_spacer") horn_spacer();
else if(part=="spacer_core") horn_spacer(5.8);
else if(part=="shim_05") horn_spacer(0.5);
else if(part=="shim_10") horn_spacer(1.0);
else if(part=="shim_15") horn_spacer(1.5);
else if(part=="head") head();
else if(part=="shared_base") shared_base();
else if(part=="camera_post") translate([0,0,15]) rotate([0,90,0]) camera_post();
else if(part=="camera_pad") camera_pad();
else if(part=="servo_coupon") difference(){translate([10,0,0]) plate(60,34,5);servo_cut(5);}
else if(part=="horn_coupon") difference(){plate(30,30,4);horn_cut(4);}

else if(part=="electronics_tray") electronics_tray();
else if(part=="tray_foot") tray_foot();
else if(part=="switch_cradle") switch_cradle();
else if(part=="laser_coupon") laser_coupon();

else if(part=="base_left") base_left();
else if(part=="base_right") base_right();
