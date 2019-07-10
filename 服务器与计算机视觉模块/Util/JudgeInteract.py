import datetime

from Util import GlobalVar
from Util import MonitorUtil
import numpy
invaded_time = datetime.datetime.now()
interact_time = datetime.datetime.now()
smile_time = datetime.datetime.now()
fall_time = datetime.datetime.now()
def faceRegniZation(image=None):
    global invaded_time, interact_time, smile_time, fall_time
    data = numpy.array(image)
    # print(type(image))
    # print(type(data))
    face_location_list, names, types = GlobalVar.faceutil.get_face_location_name_and_type(
        data)

    if (datetime.datetime.now() - invaded_time).seconds > 10:
        GlobalVar.is_invaded = MonitorUtil.is_Invaded(types, GlobalVar.is_invaded, image)
        invaded_time=datetime.datetime.now()

    if (datetime.datetime.now() - interact_time).seconds > 10:
        GlobalVar.is_interact = MonitorUtil.is_Interact(types,names, GlobalVar.is_interact, data)
        interact_time = datetime.datetime.now()

    # if(datetime.datetime.now() - fall_time).seconds > 10:
    #     GlobalVar.is_fall = MonitorUtil.is_Fall(types, names, GlobalVar.is_fall, data)
    #     fall_time = datetime.datetime.now()

    if (datetime.datetime.now() - smile_time).seconds > 10:
        MonitorUtil.is_Smile(face_location_list, names, types, data)
        smile_time = datetime.datetime.now()

    MonitorUtil.is_FallDown(face_location_list, names, types, data)
