# This file should be sourced
# Jumps into the houdini folder, sources houdini_setup and jumps back
tempWorkingDirTADKLJSDD=$(pwd) 
# cd /opt/hfs19.5.605/ 
cd /home/dayne/Apps/sidefx/hfs20.0.547/ 
source houdini_setup 
cd "$tempWorkingDirTADKLJSDD" 
unset tempWorkingDirTADKLJSDD 
