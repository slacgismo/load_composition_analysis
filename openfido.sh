set -u
set -e
set -x
pip -q install -r user_requirements.txt
cp $OPENFIDO_INPUT/user_config.csv $PWD
python path.py
python src/scripts/composite_loads.py
len_file=$(wc -l < file_loc.txt)
len_debug=$(wc -l < debug_loc.txt)
for i in $(seq 1 $len_file)
do
	f=$(awk NR==$i file_loc.txt)
	cp -r $f/*.csv $OPENFIDO_OUTPUT
done
for i in $(seq 1 $len_debug)
do
	f=$(awk NR==$i debug_loc.txt)
	cp -r $f/*.png $OPENFIDO_OUTPUT
done
