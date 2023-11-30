from typing import List, Tuple
import xml.etree.ElementTree as ET

def get_time_from_attr(attributes: str) -> float:
    """
    从p属性获取该弹幕于视频的开始时间。
    :param attributes: 从parse中获取的p属性attribute字符串
    :return: 返回该弹幕的开始时间。
    """
    attrs = attributes.split(',')
    start_time = attrs[0]
    return float(start_time)

def parse_xml(xml_path: str, sort=True) -> List[Tuple[float, str]]:
    """
    将指定xml文件转为表示弹幕的列表。列表的每个元素是一个二元组(start_time: float, text: str),
    分别表示开始时间(秒)和文本。
    :param xml_path: xml文档路径
    :param sort: 是否按时间排序
    :return: List[Tuple[float, str]], 如上文所述
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    result = []
    for child in root:
        if 'p' in child.attrib:
            attributes = child.get('p')
            text = child.text
            result.append((get_time_from_attr(attributes), text))
    if sort:
        result.sort()
    return result