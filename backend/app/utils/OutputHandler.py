from typing import Union

def std_content(message: str='', data: Union[list,dict]={}, **kwargs) -> dict:
  ''' standard content containing message, data at least

    Args:
      message (str): message if the function fails (default = '')
      data (list | dict): data to be returned if the function contains (default = {})
    Returns:
      content (dict): message, data
  '''
  content = {'message': message, 'data': data}
  for k, v in kwargs.items():
    content.update({k : v})
  return content