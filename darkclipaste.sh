
DIR="$(dirname "$(readlink "$0")")" 

full_path="${DIR}/main.py"

python3 $full_path "$@"
