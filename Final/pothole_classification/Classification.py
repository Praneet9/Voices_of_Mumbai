
import numpy as np
import cv2
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import *
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import colorsys as cs


trigger = False

global severity_graph, severity_sess, severity_model

severity_graph = tf.Graph()
severity_sess = tf.Session(graph = severity_graph)

with severity_graph.as_default():
	with severity_sess.as_default():
		severity_model = load_model(r'pothole_classification/training_result.h5')

def predict_severity(unique_id, coords):
    level_pred = []
    for coord in coords:
        x, y, w, h = coord
        img = cv2.imread('temp/' + unique_id + '.jpg')
        cv2.imwrite('cropped_potholes/' + unique_id + '.jpg', img[y:h, x:w])
        
        result = predict_level('cropped_potholes/' + unique_id + '.jpg', 'temp/' + unique_id + '.jpg', trigger)
        level_pred.append(result)
    return level_pred

# def _init_(graph, sess):
# 	global new_model,training_set
# 	with graph.as_default():
# 		with sess.as_default():

# 			new_model = load_model(r'training_result.h5')

def detect_level_4(crop_image):
	image = cv2.resize(crop_image, (300, 300))
	median = cv2.medianBlur(image, 7)
	# cv2.imshow('blur', median)
	lower_range = np.array([0,0,0])
	upper_range = np.array([15,15,15])

	mask = cv2.inRange(median, lower_range, upper_range)
	# cv2.imshow('mask', mask)
	contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	area = 0
	if len(contours) != 0:
		cv2.drawContours(image, contours, -1, 255, 3)
		# cv2.imwrite('contours.jpg', image)
		c = max(contours, key = cv2.contourArea )

		area = cv2.contourArea(c)
		print('area', area)
		x, y, w, h = cv2.boundingRect(c)
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		# cv2.imwrite('contoursrect.jpg', image)
	else:
		print('no black detected')
		area = 0

	# cv2.imshow('detection', image)
	# cv2.waitKey(0)
	threshold = (300 * 300) * 0.03
	print('threshold', threshold)
	if(area < threshold):
		# print('not level 4')
		return False;
	else:
		# print('level 4')
		return True


def detect_level_1(crop_image):
    
    test_image = image.load_img(crop_image,target_size = (64,64))
    # cv2.imwrite('test_image.jpg', test_image)
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image,axis = 0)

    with severity_graph.as_default():
        with severity_sess.as_default():
            result = severity_model.predict(test_image)
    # print(result)
    # training_set.class_indices
    # print(training_set.class_indices)
    # print(result)
    # max_num = np.argmax(result)
    # print('max', max_num)
    if result <= 0.5:
        prediction = 'crack'
        return True
    else:
        prediction = 'not crack'
        return False


def find_histogram(clt):
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	# bins is the x-axis value
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# convert value to float
	hist = hist.astype("float")

	# value of each column divide by sum of all value
	hist /= hist.sum()

	return hist

def plot_colors2(hist, centroids):
	# print(centroids)
	bar = np.zeros((50, 300, 3), dtype = 'uint8')
	startX = 0

	# print(list(zip(hist, centroids)))
	results = []
	for(percent, color) in zip(hist, centroids):
		results.append([percent, color])
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype('uint8').tolist(), -1) 
		startX = endX

	return bar, results

def verify_pothole(results):
	# 128 128 128
	# print('verifyinnggg')
	# print(results)
	
	final_h = 0.0
	final_s = 0.0
	final_v = 0.0
	depth_score = 0
	for i in results:
		# print('x')
		# print(i)
		area = i[0]
		r_temp = i[1][0] / 255
		g_temp = i[1][1] / 255
		b_temp = i[1][2] / 255
		# print(r_temp, g_temp, b_temp)
		h, s, v = cs.rgb_to_hsv(r_temp, g_temp, b_temp)
		# print('h = %s, s = %s, v = %s'%(h, s, v))
		temp_depth_score = (1 - s) + (1 - v) * 2 
		# print('temp_depth_score', temp_depth_score)
		if(temp_depth_score > depth_score):
			depth_score = temp_depth_score


	# print('xxxxxxxxxxxxxxxxxxxxxxxxxx')
	# print(depth_score)
	
	depth_score /= 3 #normalise
	return depth_score

def predict_level(crop_image, original_image, trigger):
    
	# if(trigger == True):
	# 	isLevel1 = detect_level_1(graph, sess, crop_image)
	# 	if(isLevel1 == True):
	# 		prediction = 'Level 1'
	# 		return prediction
	# 	else:
	# 		prediction = 'Nothing detected'
	# 		return prediction

    image = cv2.imread(crop_image)
    original_image = cv2.imread(original_image)
    # cv2.imshow('ori', original_image)
    # cv2.imshow('crop', image)
    # cv2.waitKey(0)
    # detect level 4 ( black )
    isLevel1 = detect_level_1(crop_image)
    if(isLevel1 == True):
        prediction = 1
        return prediction
    isLevel4 = detect_level_4(image.copy())
    if(isLevel4 == True):
        prediction = 4
        return prediction

    n_cluster = 3
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3))
    clt = KMeans(n_cluster)
    clt.fit(img)
    hist = find_histogram(clt)
    bar, color = plot_colors2(hist, clt.cluster_centers_)
    # plt.axis('off')
    # plt.imshow(bar)
    # plt.show()
    depth_score = verify_pothole(color)
    # print('depth: ', depth_score)
    # print('image size', image.size)
    # print('original size', original_image.size)
    ratio = image.size / original_image.size
    # print('ratio:', ratio)

    final_ratio = ratio + depth_score
    # print('final ratio', final_ratio)
    if(final_ratio <= 1.0):
        prediction = 2
    else:
        prediction = 3
    # print(prediction)
    return prediction

		

		




# graph = tf.Graph()
# sess = tf.Session(graph = graph)
# with graph.as_default():
# 	with sess.as_default():
# 		#predict._init_(graph, sess)
# 		_init_(graph, sess)
# 		predict_level(graph, sess, crop_image, original_image, trigger)