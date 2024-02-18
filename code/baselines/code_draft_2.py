import cv2
# img_path=""
# with cv2.imread(img_path) as img:
#     pass


# from PIL import Image
# with Image.open('a') as img:
#     pass
# import codecs
# vocabulary_label = "path/to/your/file.txt"
# with codecs.open("", 'r', 'utf8') as zhihu_f_train:
#     pass

import tensorflow as tf
# # sess = tf.compat.v1.Session()
# with tf.summary.create_file_writer("/tmp/tf2_summary_example") as writer:
#     pass

# import tqdm
# file1="a.txt"
# file2="a.txt"
# filename_pairs = [(file1, file2)]
# with tqdm(filename_pairs) as pbar:
#     pass
# from tabulate import tabulate
#
# data = [["Alice", 25, "Engineer"],
#         ["Bob", 30, "Designer"],
#         ["Charlie", 28, "Developer"]]
#
# with tabulate.Table(data=data, headers=["Name", "Age", "Occupation"]) as a:
#     pass
tf.compat.v1.disable_eager_execution() # need to disable eager in TF2.x
# Build a graph.
a = tf.constant(5.0)
b = tf.constant(6.0)
c = a * b
with tf.compat.v1.Session() as e:
    pass
# # Launch the graph in a session.
# sess = tf.compat.v1.Session()
# import madmom
# from madmom.io.audio import audiodecode_to_pipe
#
# infile = "path_to_your_audio_file.wav"  # Replace with the actual path
#
# # Open the audio file and create a processing pipeline
# with audiodecode_to_pipe(infile) as proc:
#     pass
a=list(range(10))
for i,e in enumerate(a):
    e=2
print(a)
