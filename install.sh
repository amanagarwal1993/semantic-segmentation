cd ~
wget http://kitti.is.tue.mpg.de/kitti/data_road.zip
unzip data_road.zip
mv data_road semantic-segmentation/data
pip install tqdm
cd semantic-segmentation
python main.py