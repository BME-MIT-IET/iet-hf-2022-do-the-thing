cwd=$(pwd)
namanager_root_path="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )/.."
cd $namanager_root_path

pip3 uninstall -y namanager
pip3 uninstall -y dist/namanager-`python3 setup.py -V`-py2.py3-none-any.whl
rm -rf build dist

pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install sdist wheel
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
pip3 install dist/namanager-`python3 setup.py -V`-py2.py3-none-any.whl

cd $CWD
