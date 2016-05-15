import json


AO_names = ["szao", "sao", "svao", "vao", "uvao", "uao", "uzao", "zao", "cao", "new-msk"]
output_data = \
    {
        "szao" : [],
        "sao" : [],
        "svao" : [],
        "vao" : [],
        "uvao" : [],
        "uao" : [],
        "uzao": [],
        "zao" : [],
        "cao" : [],
        "new-msk" : []
    }

def parse_json(file_path):
    json_data = open(file_path)
    data = json.load(json_data)
    return data


def count_distance(w,l, Cl, Cw):
    return (w - Cw)*(w - Cw) + (l - Cl)*(l - Cl)


def find_nearest(data, Cl, Cw):
    result = None
    cur_distance = float('inf')
    min_index = 0
    for i, obj in enumerate(data):
        temp = count_distance(obj["Cells"]["geoData"]["coordinates"][0][1], obj["Cells"]["geoData"]["coordinates"][0][0], Cl, Cw)
        if temp < cur_distance:
            result = obj
            cur_distance = temp
            min_index = i

    data.pop(min_index)
    return result


def clasterize(input_data):
    print "Clasterizing total: " + str(len(input_data)) + " objects"
    ao_centres_data = parse_json("./app/static/AO_centres.json")
    while len(input_data) > 0:
        for name in AO_names:
            if len(input_data) == 0:
                break
            else:
                res = find_nearest(input_data, ao_centres_data[name]["coord_length"], ao_centres_data[name]["coord_width"])
                output_data[name].append(res)

    for name in AO_names:
        print name + ": " +  str(len(output_data[name]))

    result = json.loads(json.dumps([output_data]))
    return result



AO_centres = parse_json("./app/static/AO_centres.json")
data = parse_json("./app/static/Polyclinics.json")



#print data[1]["Cells"]["ShortName"]
#print data[1]["Cells"]["geoData"]["coordinates"][0]