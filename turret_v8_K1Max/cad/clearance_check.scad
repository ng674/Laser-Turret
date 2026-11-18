include <main.scad>
// Invoke with part="none", test_pan and test_tilt. Empty intersection is pass.
test_pan=0; test_tilt=0;
module moving(){translate([0,0,base_thickness+50+horn_gap]) rotate([0,0,test_pan]) {
 carrier();
 translate([-31,0,39]) rotate([0,90,0]) rotate([0,0,90]) servo_proxy();
 translate([-31+horn_gap,0,39]) rotate([0,90,0]) rotate([0,0,test_tilt]) head();
}}
module fixed(){shared_base();
 translate([0,0,base_thickness]) {
 translate([0,0,50]) base();for(x=[-46,46]) translate([x,0,0]) leg();
 translate([camera_x,0,0]) {camera_post();translate([0,0,110]) camera_pad();
 translate([0,0,115+43.3/2]) cube([94,71,43.3],center=true);}}
 translate([tray_x,tray_y,8]) electronics_tray();
 translate([-12,75,12]) switch_cradle();
 translate([48,125,18]) cube([165,56,12],center=true);
 translate([130,72,14]) cube([33,42,4],center=true);
}
check="external";
if(check=="external") intersection(){moving();fixed();}
if(check=="head") intersection(){carrier();
 translate([-31+horn_gap,0,39]) rotate([0,90,0]) rotate([0,0,test_tilt]) head();}
