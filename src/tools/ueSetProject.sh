nc="$(tput sgr0)"
bold="$(tput bold)"
blue="$(tput setaf 4)"
red="$(tput setaf 1)"
green="$(tput setaf 2)"
yellow="$(tput setaf 3)"

prj=$red
grp=$green
ast=$yellow

sp=`python $UE_PATH/core/ueSetProject.py $*`

if [[ $? == 1 ]]; then
  eval $sp

  if [[ -d $PROJ_ROOT/bin ]]; then
    export PATH=$PATH:$PROJ_ROOT/bin
  fi

  export PS1="[\[$prj\]$PROJ\[$nc\]:\[$grp\]$GROUP\[$nc\]:\[$ast\]$ASST\[$nc\]]\n[\u@\h \W]\$ "

  cd $ASST_ROOT

  echo ""
  echo "${bold}Setting current asset to:$nc"
  echo "  Project: [ $prj$PROJ$nc ]"
  echo "  Group:   [ $grp$GROUP$nc ]"
  echo "  Asset:   [ $ast$ASST$nc ]"
  echo ""
else
  echo -e $sp
fi

