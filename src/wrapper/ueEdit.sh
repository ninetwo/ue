rv_path=/opt/rv-Linux-x86-64-3.12.14/bin/rv.bin
rvpkg_path=/opt/rv-Linux-x86-64-3.12.14/bin/rvpkg.bin

ueEditPkg=ueEdit-1.0.rvpkg

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rv-Linux-x86-64-3.12.14/libWorking
export RV_SUPPORT_PATH=$RV_SUPPORT_PATH:/work/bin/rvTests

$rvpkg_path -install $ueEditPkg

$rv_path $*

$rvpkg_path -uninstall $ueEditPkg

