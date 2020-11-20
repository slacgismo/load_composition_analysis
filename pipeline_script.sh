pip install -r user_requirements.txt
python composite_loads.py
export f=`cat file_loc.txt`
cp -r $f/*.csv $OPENFIDO_OUTPUT
