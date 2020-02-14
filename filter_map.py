from lxml import etree
import config
import re
import json
import os


class Record_dev_xml:

    def __init__(
        self,
        id_dev=None,
        name=None,
        ip_address=None,
        description=None
                ):

        self.id = id_dev
        self.name = name
        self.ip = ip_address.split(':')[0]
        self.description = description
        self.model = self.set_model()

    def set_model(self):
        model = self.description.split('\n')[0]
        model = re.sub('[ ]', '-', model).upper()
        return model


def main():

    smart_map = reader()
    filtred_map = filter(smart_map)


    return filtred_map


def format_smart(smart):
    smart_formatted = {}
    doubles = []
    for dev_map in smart:
        if dev_map.ip not in smart_formatted:
            smart_formatted.update({dev_map.ip: dev_map})
        else:
            doubles.append(dev_map.__dict__)
    return smart_formatted, doubles


def into_json(obj, fname=config.OUTPUTJSONMAP):
    if (os.path.isfile(fname)):
        os.remove(fname)

    with open(fname, 'a+', encoding='utf-8-sig', newline='\n') as output_file:
        json.dump(obj, output_file, indent='\t')


def create_model_list(filtred_map):
    model_list = {}
    for record in filtred_map:
        if record.model not in model_list:
            model_list.update({record.model: []})
        model_list[record.model].append(record.__dict__)
    return model_list


def filter(smart_map):
    filter_map = []
    for record in smart_map:
        if record.tag == 'Devices':
            for dev in record:
                if dev.attrib['type-id'] == 'Modem':
                    modem = dev.attrib
                    desc = dev.getchildren()

                    if len(desc) == 1:
                        desc = desc[0].text
                    else:
                        desc = ''

                    filter_map.append(Record_dev_xml(
                            modem['id'],
                            modem['name'],
                            modem['address'],
                            desc
                        ))
    return filter_map


def reader():
    with open(config.MAPPATH, 'r', encoding='utf-8-sig') as smart:
        smart = smart.read()
        parser = etree.XMLParser(strip_cdata=False)
        smart_map = etree.fromstring(smart, parser=parser)
    return smart_map


if __name__ == "__main__":
    modem_list = {}

    filtred_map = main()

    into_json(create_model_list(filtred_map), config.GROUPMODEL)

    smart_map, doubles = format_smart(filtred_map)

    if len(doubles) == 0:
        for record in filtred_map:
            modem_list.update({record.ip: record.__dict__})

    into_json(modem_list)

    print('done')
