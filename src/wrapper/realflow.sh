realflow_path=/opt/realflow/bin/realflow

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running realflow"
  exit 0
fi

$realflow_path $*

