import yaml

class InfoReader :
  """
  Holds info about the script.
  """

  def __init__(self) :
    self.title: str = ""
    self.author: str = ""
    self.repo: str = ""
    self.license: str = ""
    self.version: str = ""
    self.description: str = ""
    self.notice: str = ""

  def read(self, file_name: str) :
    """
    Reads the info file that is input.

    :param file_name: the file to read
    """

    with open(file=file_name, mode="r") as yam :
      info_data = yaml.safe_load(yam)

      self.title = info_data["title"]
      self.author = info_data["author"]
      self.repo = info_data["repo"]
      self.license = info_data["license"]
      self.version = info_data["version"]
      self.description = info_data["description"]
      self.notice = info_data["notice"]
