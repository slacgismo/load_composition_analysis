pip install -r user_requirements.txt
python composite_loads.py
len=$(wc -l < file_loc.txt)
for i in $(seq 1 $len)
do
	f=$(awk NR==$i file_loc.txt)
	cp -r $f/*.csv $OPENFIDO_OUTPUT
done
cp -r *.png $OPENFIDO_OUTPUT