cwd=$(pwd)
namanager_root_path="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/.."
cd $namanager_root_path

python3 -m venv env/upload
rm -rf build dist
source ./env/upload/bin/activate

pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install twine
pip3 install sdist
python3 setup.py sdist
pip3 install wheel
python3 setup.py bdist_wheel --universal
twine upload dist/*
rm -rf dist
deactivate

cd $CWD
