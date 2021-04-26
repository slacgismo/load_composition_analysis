set -u
set -e
set -x
<<<<<<< HEAD
python3 -m pip -q install -r requirements.txt
cp $OPENFIDO_INPUT/config.csv $PWD
python3 path.py
python3 src/scripts/composite_loads.py
=======
pip -q install -r user_requirements.txt
cp $OPENFIDO_INPUT/user_config.csv $PWD
python path.py
python src/scripts/composite_loads.py
>>>>>>> dc834c640f4f9cef874a90c3b1b73e3245535241
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
