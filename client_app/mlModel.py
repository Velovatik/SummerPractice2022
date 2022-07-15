import tensorflow as tf
import cv2
import numpy as np
from homografy import *
import socket
import pickle
from math import sqrt
from object_detection.utils import visualization_utils as vis_utils
from object_detection.utils import label_map_util as label_util
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()

category_id = label_util.create_category_index_from_labelmap('object_detection/data/tf_label_map.pbtxt',
                                                             use_display_name=True)
model = tf.saved_model.load('object_detection/training/export/saved_model/')

def get_frame_from_tensor(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_tensor = tf.convert_to_tensor(img_rgb)
    img_tensor = img_tensor[tf.newaxis,...]
    img_tensor = img_tensor[:,:,:, :3]
    result = model(img_tensor)
    result = {key:value.numpy() for key,value in result.items()}

    vis_utils.visualize_boxes_and_labels_on_image_array(
        img,
        result['detection_boxes'][0],
        (result['detection_classes'][0] + 0).astype(int),
        result['detection_scores'][0],
        category_id,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=.55,
        agnostic_mode=False
    )
    return img

def get_bbox_from_tensor(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_tensor = tf.convert_to_tensor(img_rgb)
    img_tensor = img_tensor[tf.newaxis,...]
    img_tensor = img_tensor[:,:,:, :3]
    result = model(img_tensor)
    result = {key:value.numpy() for key,value in result.items()}

    boxes = result['detection_boxes'][0]
    scores = result['detection_scores'][0]
    min_score_thresh = .50

    coordinates = []
    for i in range(len(boxes)):
        if scores[i] > min_score_thresh:
            boxes[i][0] = boxes[i][0]*img.shape[0]
            boxes[i][2] = boxes[i][2]*img.shape[0]
            boxes[i][1] = boxes[i][1]*img.shape[1]
            boxes[i][3] = boxes[i][3]*img.shape[1]
            coordinates.append({
                "name" : category_id[result['detection_classes'][0][i]]['name'],
                "boxes" : boxes[i]
            })
    
    return coordinates

def get_points_coordinates(coordinates):
    points = []
    for i in range(len(coordinates)):
        points.append({
            'name' : coordinates[i]['name'],
            'point' : [coordinates[i]['boxes'][1]+((coordinates[i]['boxes'][3]-coordinates[i]['boxes'][1]))/2,coordinates[i]['boxes'][0]+((coordinates[i]['boxes'][2]-coordinates[i]['boxes'][0])/2)]
        })

    return points

def get_real_coordinate(bboxes, points):
    new_points = []
    for i in  range(len(bboxes)):
        real = np.array([[37.5, 752.5],[37.5, 420.5],[462.5, 747.5], [462.5, 392.5]])
        old = np.array([[bboxes[i]['boxes'][1],bboxes[i]['boxes'][2]],
                        [bboxes[i]['boxes'][1],bboxes[i]['boxes'][0]],
                        [bboxes[i]['boxes'][3],bboxes[i]['boxes'][2]],
                        [bboxes[i]['boxes'][3],bboxes[i]['boxes'][0]]])
        new_ccor = np.array(points[i]['point'])
        homo = HomographyTranslate(real,old)
        homo.find_homo_array()
        new = np.array(homo.find_real_coordinate(new_ccor))
        new_points.append({
            'name' : points[i]['name'],
            'point' : [new[0],new[1]]
        })
    return new_points

def get_trajectory(first_vector, second_vector):
    trajectory = []
    trajectory.append(sqrt((second_vector[0]-first_vector[0])**2 + (second_vector[1]-first_vector[1])**2))
    return trajectory

def get_trajectories_for_movements(collors, frame):
    bboxes = get_bbox_from_tensor(frame)
    points = get_points_coordinates(bboxes)

    real_points = get_real_coordinate(bboxes, points)
    collor_count = 0
    trajectories = []
    for i in range(len(real_points)-1):
        first_vector = []
        second_vector = []
        for j in range(len(collors)):
            point = real_points[j]
            if point['name'] == collors[collor_count]:
                first_vector = point['point']
            if point['name'] == collors[collor_count + 1]:
                second_vector = point['point']
        traj = get_trajectory(first_vector,second_vector)
        trajectories.append(traj[0])
        collor_count = collor_count + 1
    return trajectories

def get_angle(trajectory, robot_trajectory):
    angle = []
    angle.append((trajectory[0]*robot_trajectory[0]+trajectory[1]*robot_trajectory[1])/(sqrt(trajectory[0]**2+trajectory[1]**2)*sqrt(robot_trajectory[0]**2+trajectory[1]**2)))
    return angle

def send_commands(trajectories, angles):
    HOST = 'localhost'
    PORT = 50007
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    commands = []
    for i in range(len(trajectories)):
        commands.append({
            'id' : 0,
            'val' : angles[i]
        })
        commands.append({
            'id' : 1,
            'val' : trajectories[i]
        })

    data_string = pickle.dumps(commands)
    sock.send(data_string)
    data = sock.recv(4096)
    sock.close()