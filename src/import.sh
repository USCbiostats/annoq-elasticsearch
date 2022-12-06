data_dir=/Users/zhuliu/projects/api/cloudes/es_api/data/hrc_12_2019/

for i in `ls $data_dir`;do
echo "import data $i"
cat $data_dir$i|zcat|python3 ./load_data.py
done
