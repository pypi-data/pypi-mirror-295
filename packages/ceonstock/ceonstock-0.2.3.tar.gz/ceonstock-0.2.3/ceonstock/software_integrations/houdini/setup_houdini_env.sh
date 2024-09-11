# This file should be sourced
# Jumps into the houdini folder, sources houdini_setup and jumps back
tempWorkingDirTADKLJSDD=$(pwd) 
cd /opt/hfs19.5.605/ 
source houdini_setup 
cd "$tempWorkingDirTADKLJSDD" 
unset tempWorkingDirTADKLJSDD 
