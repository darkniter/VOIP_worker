from filter_map import main as xml_map
from xlsx_file_uploading import main as excel_file
from filter_map import into_json
import config


def main():
    excel = excel_file()
    smart_map = xml_map()
    smart_map, doubles = format_smart(smart_map)
    into_json(doubles, config.DOUBLES)

    found, not_found, double_record, not_found_ip = comparsion(
                                                    smart_map,
                                                    excel
                                                    )

    into_json(found, config.FOUNDED)
    into_json(not_found, config.NOTFOUNDED)
    into_json(double_record, config.DOUBLERECORDS)
    into_json(not_found_ip, config.NOTFOUNDED_IP)
    print('done')


def format_smart(smart):
    smart_formatted = {}
    doubles = []
    for dev_map in smart:
        if dev_map.ip not in smart_formatted:
            smart_formatted.update({dev_map.ip: dev_map})
        else:
            doubles.append(dev_map.__dict__)
    return smart_formatted, doubles


def comparsion(smart, xl):
    found = {}
    not_found_ip = []
    not_found = []
    double_record = []

    for record in xl:

        if record.new_ip in smart:
            if record.new_ip not in found:
                found.update({
                    record.new_ip: [
                        record.__dict__,
                        smart[record.new_ip].__dict__
                                ]
                            })
            else:
                double_record.append({
                    record.new_ip: [
                        record.__dict__,
                        smart[record.new_ip].__dict__
                            ]
                        })

        elif record.old_ip in smart:
            if record.old_ip not in found:
                found.update({
                    record.old_ip: [
                        record.__dict__,
                        smart[record.old_ip].__dict__
                            ]
                        })
            else:
                double_record.append({
                    record.old_ip: [
                        record.__dict__,
                        smart[record.old_ip].__dict__
                            ]
                        })

        else:
            not_found_ip.append({
                'new_ip': record.new_ip,
                'old_ip': record.old_ip
                })
            not_found.append(record.__dict__)

    return found, not_found, double_record, not_found_ip


if __name__ == "__main__":
    main()
