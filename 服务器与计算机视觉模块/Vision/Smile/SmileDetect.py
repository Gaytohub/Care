import os
import numpy as np
from PIL import Image
import tensorflow as tf
from Util.CNN import deep_CNN
import cv2

N_CLASSES = 2

img_dir = '../dataset/test/'
log_dir = '../model'
lists = ['neutral', 'happy']
facePath = "lbpcascade_frontalface.xml" # haarcascade_frontalface_default.xml



# # 从测试集中随机挑选一张图片看测试结果
# def get_one_image(image):
#     # imgs = os.listdir(img_dir)
#         # img_num = len(imgs)
#         # # print(imgs, img_num)
#         # idn = np.random.randint(0, img_num)
#         # image = imgs[idn]
#         # image_dir = img_dir + image
#         # print(image_dir)
#         # image = Image.open(image_dir)
#         # plt.imshow(image)
#         # plt.show()
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     face = faceCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=8,
#         minSize=(55, 55),
#         flags=cv2.CASCADE_SCALE_IMAGE
#     )
#     print(face)
#     image = image.resize([48, 48])
#     image_arr = np.array(image)
#     return image_arr

sess = None
def load_model():
    global sess
    x = tf.compat.v1.placeholder(tf.float32, shape=[48, 48, 3])
    saver = tf.compat.v1.train.Saver()
    sess = tf.compat.v1.Session()
    sess.run(tf.compat.v1.global_variables_initializer())
    ckpt = tf.train.get_checkpoint_state(log_dir)
    if ckpt and ckpt.model_checkpoint_path:
        # print(ckpt.model_checkpoint_path)
        saver.restore(sess, tf.train.latest_checkpoint(log_dir))

        # saver.restore(sess, ckpt.model_checkpoint_path)
        # 调用saver.restore()函数，加载训练好的网络模型
        print('Loading success')


#传入脸cv2格式
def test(image):
    # global sess
    with tf.Graph().as_default():
        # image = image.resize([48, 48])
        image_arr = np.array(image)
        # print(image_arr)
        image = tf.cast(image, tf.float32)
        image = tf.image.per_image_standardization(image)
        image = tf.reshape(image, [1, 48, 48, 3])
        # print(image.shape)
        p = deep_CNN(image, 1, N_CLASSES)
        logits = tf.nn.softmax(p)
        x = tf.compat.v1.placeholder(tf.float32, shape=[48, 48, 3])
        saver = tf.compat.v1.train.Saver()
        sess = tf.compat.v1.Session()
        sess.run(tf.compat.v1.global_variables_initializer())
        ckpt = tf.train.get_checkpoint_state(log_dir)
        if ckpt and ckpt.model_checkpoint_path:
            # print(ckpt.model_checkpoint_path)
            saver.restore(sess, tf.train.latest_checkpoint(log_dir))

            # saver.restore(sess, ckpt.model_checkpoint_path)
            # 调用saver.restore()函数，加载训练好的网络模型
            print('Loading success')
        prediction = sess.run(logits, feed_dict={x: image_arr})
        max_index = np.argmax(prediction)
        print('预测的标签为：', max_index, lists[max_index])
        print('预测的结果为：', prediction)
        return lists[max_index]


if __name__ == '__main__':
    import time
    from oldcare.facial import FaceUtil
    imgs = os.listdir(img_dir)
    for img in imgs:
        print(img)
        image = cv2.imread(img_dir + '/' + img)
        faceutil = FaceUtil()
        face_location_list = faceutil.get_face_location(image)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # print(gray)
        #
        # faceCascade = cv2.CascadeClassifier(facePath)
        # faces = faceCascade.detectMultiScale(
        #     image,
        #     scaleFactor=1.1,
        #     minNeighbors=8,
        #     minSize=(55, 55),
        #     flags=cv2.CASCADE_SCALE_IMAGE
        # )
        print(len(face_location_list))
        for (x, y, w, h) in face_location_list:
            face = image[y:h, x:w]
            face = cv2.resize(face, (48, 48))
            # cv2.imshow("smile", face)

            # print(len(face))
            # print(len(face[0]))
            # load_model()
            starttime = time.time()

            print(test(face))
            print(time.time()-starttime)
            # c = cv2.waitKey(0)
