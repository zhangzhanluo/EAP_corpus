import os
import chardet
import pandas as pd

file_home = 'Txts/'
file_paths = os.listdir(file_home)

# records the encoding information for later file reading
encodings = []
for file_path in file_paths:
    encodings.append(chardet.detect(open(file_home + file_path, 'rb').read())['encoding'])
encodings = ['utf-8' if i == 'Windows-1254' else i for i in encodings]
encoding_dic = {x: y for x, y in zip(file_paths, encodings)}

# create the corpus for each subject and for all the subjects
subject_ids = list(set([x[:6] for x in file_paths]))
subject_ids = sorted(subject_ids)
all_all_lines = []
for subject_id in subject_ids:
    all_lines = []
    for file_path in file_paths:
        if file_path.startswith(subject_id):
            with open(file_home + file_path, mode='r', encoding=encoding_dic[file_path]) as file:
                lines = file.readlines()
                all_lines = all_lines + lines
    all_all_lines = all_all_lines + all_lines

    with open('Results/text for subject {}.txt'.format(subject_id), mode='w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line)

with open('Results/text for all subject.txt', mode='w', encoding='utf-8') as f:
    for line in all_all_lines:
        f.write(line)

# create the documentation for the corpus
file_home = 'Xlsxs/'
file_paths = os.listdir(file_home)

files = []
for file_path in file_paths:
    df = pd.read_excel(file_home + file_path, header=0)
    files.append(df.iloc[:, 1:])
all_files = pd.concat(files, axis=0)
all_files['所属一级学科（代码）'] = all_files['所属一级学科（代码）'].apply(lambda x: '0' + str(x))
all_files['所属一级学科（代码）'] = all_files['所属一级学科（代码）'].apply(lambda x: '080700' if x in ['080701', '080702'] else x)
all_files['英语班级'] = 'M31'
all_files['学院代码'] = all_files['学院代码'].apply(lambda x: '020' if x == 20 else x)
all_files['学院代码'] = all_files['学院代码'].apply(lambda x: '440' if x == 440 else x)
grouper = all_files.groupby('所属一级学科（代码）')
for subject_id, group in grouper:
    group.index = ['RA' + str(x) for x in range(1, group.shape[0] + 1)]
    group.to_excel('Results/documentation of the RAs (in corpus for subject {}).xlsx'.format(subject_id),
                   encoding='utf-8-sig')
all_files.index = ['RA' + str(x) for x in range(1, all_files.shape[0] + 1)]
all_files.to_excel('Results/documentation of the RAs (in corpus for all subject).xlsx', encoding='utf-8-sig')
