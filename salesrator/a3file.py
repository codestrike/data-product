import os

class touch:
  def touchdir(self, to_touch):
    # temp_path = os.path.join(to_touch, extenstion)
    if not os.path.exists(to_touch):
      os.makedirs(to_touch)
    else :
      pass

  def populate(self, userid):
    bp = os.getcwd() + '/files/' + userid
    # file_path = a3file.touchdir(basepath ,'files')
    # file_path = a3file.touchdir(file_path ,userid)
    # csv_path = a3file.touchdir(file_path, 'csv' )
    # img_path = a3file.touchdir(file_path, 'img')
    # pickle_path = a3file.touchdir(file_path, 'pickle')
    paths = [bp+'/csv', bp+'/img', bp+'/pickle']
    for x in paths:
      self.touchdir(x)
    return paths




