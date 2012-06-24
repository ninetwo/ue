rv_path=/opt/rv-Linux-x86-64-3.12.14/bin/rv.bin
rvpkg_path=/opt/rv-Linux-x86-64-3.12.14/bin/rvpkg.bin

ueEditPkg=ueEdit-1.0.rvpkg


if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running ueEdit"
  exit 0
fi

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rv-Linux-x86-64-3.12.14/libWorking
export RV_SUPPORT_PATH=$RV_SUPPORT_PATH:$UE_PATH/src/ueEdit/package

$rvpkg_path -install $ueEditPkg

$rv_path $*

$rvpkg_path -uninstall $ueEditPkg

