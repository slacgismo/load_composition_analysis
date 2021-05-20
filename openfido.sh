# nounset: undefined variable outputs error message, and forces an exit
set -u

# errexit: abort script at first error
set -e

# print command to stderr before executing it:
set -x

echo "OPENFIDO_INPUT = $OPENFIDO_INPUT\n"
echo "OPENFIDO_OUTPUT = $OPENFIDO_OUTPUT\n"

python3 -m pip -q install -r requirements.txt
cp $OPENFIDO_INPUT/config.csv $PWD
python3 src/scripts-derin/composite_loads.py
len_file=$(wc -l < logs/file_loc.txt)
len_debug=$(wc -l < logs/debug_loc.txt)
for i in $(seq 1 $len_file)
do
	f=$(awk NR==$i logs/file_loc.txt)
	cp -r $f/*.csv $OPENFIDO_OUTPUT
done
for i in $(seq 1 $len_debug)
do
	f=$(awk NR==$i debug_loc.txt)
	cp -r $f/*.png $OPENFIDO_OUTPUT
done
