from ctypes import *
import math
import random
import os
import cv2

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [('x', c_float),
                ('y', c_float),
                ('w', c_float),
                ('h', c_float)]

class DETECTION(Structure):
    _fields_ = [('bbox', BOX),
                ('classes', c_int),
                ('prob', POINTER(c_float)),
                ('mask', POINTER(c_float)),
                ('objectness', c_float),
                ('sort_class', c_int)]


class IMAGE(Structure):
    _fields_ = [('w', c_int),
                ('h', c_int),
                ('c', c_int),
                ('data', POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [('classes', c_int),
                ('names', POINTER(c_char_p))]


class Detector:
  def __init__(self, yolopath=None):
    yolopath = yolopath if yolopath else os.path.dirname(os.path.realpath(__file__)) + '/darknet'
    self.lib = CDLL(yolopath + '/libdarknet.so', RTLD_GLOBAL)
    self.lib.network_width.argtypes = [c_void_p]
    self.lib.network_width.restype = c_int
    self.lib.network_height.argtypes = [c_void_p]
    self.lib.network_height.restype = c_int

    self.predict = self.lib.network_predict
    self.predict.argtypes = [c_void_p, POINTER(c_float)]
    self.predict.restype = POINTER(c_float)

    self.set_gpu = self.lib.cuda_set_device
    self.set_gpu.argtypes = [c_int]

    self.get_network_boxes = self.lib.get_network_boxes
    self.get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
    self.get_network_boxes.restype = POINTER(DETECTION)

    self.free_detections = self.lib.free_detections
    self.free_detections.argtypes = [POINTER(DETECTION), c_int]

    self.free_ptrs = self.lib.free_ptrs
    self.free_ptrs.argtypes = [POINTER(c_void_p), c_int]

    self.network_predict = self.lib.network_predict
    self.network_predict.argtypes = [c_void_p, POINTER(c_float)]

    self.load_net = self.lib.load_network
    self.load_net.argtypes = [c_char_p, c_char_p, c_int]
    self.load_net.restype = c_void_p

    self.do_nms_obj = self.lib.do_nms_obj
    self.do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

    self.free_image = self.lib.free_image
    self.free_image.argtypes = [IMAGE]

    self.load_meta = self.lib.get_metadata
    self.lib.get_metadata.argtypes = [c_char_p]
    self.lib.get_metadata.restype = METADATA

    self.predict_image = self.lib.network_predict_image
    self.predict_image.argtypes = [c_void_p, IMAGE]
    self.predict_image.restype = POINTER(c_float)

    self.ndarray_image = self.lib.ndarray_to_image
    self.ndarray_image.argtypes = [POINTER(c_ubyte), POINTER(c_long), POINTER(c_long)]
    self.ndarray_image.restype = IMAGE

    previous = os.getcwd()
    os.chdir(yolopath)
    self.net = self.load_net('cfg/yolov3.cfg', 'yolov3.weights', 0)
    self.meta = self.load_meta('cfg/coco.data')
    os.chdir(previous)

  def classify(self, im):
    out = self.predict_image(self.net, im)
    res = []
    for i in range(self.meta.classes):
        res.append((self.meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

  def detect(self, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = self.nparray_to_image(image)
    num = c_int(0)
    pnum = pointer(num)
    self.predict_image(self.net, im)
    dets = self.get_network_boxes(self.net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): self.do_nms_obj(dets, num, self.meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(self.meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((self.meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    self.free_image(im)
    self.free_detections(dets, num)
    return res

  def nparray_to_image(self, img):
    data = img.ctypes.data_as(POINTER(c_ubyte))
    image = self.ndarray_image(data, img.ctypes.shape, img.ctypes.strides)

    return image

  def draw(self, img, detections):
    for detection in detections:
      c_x, c_y, w, h = detection[2]
      cv2.rectangle(
        img, 
        (int(c_x - w / 2), int(c_y - h / 2)),
        (int(c_x + w / 2), int(c_y + h / 2)),
        (0, 0, 255)
      )
      
    return img
    
if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    
    im = cv2.imread('people.jpg')

    detector = Detector()
    r = detector.detect(im)
    cv2.imshow('Detections', detector.draw(im, r))
    cv2.waitKey(0)
