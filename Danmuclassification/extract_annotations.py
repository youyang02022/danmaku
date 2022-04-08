import json

with open(
    "ann.json/master/pool/aI8Fw.Pydo23hL3pCu8Vt66e7jAO-Danmaku_______.txt.ann.json",
    encoding="UTF-8"
) as in_f:
    annotations = json.load(in_f)
    summary = []
    for entry in annotations['entities']:
        summary.append({'class_id': entry['classId'], 'text': entry['offsets'][0]['text']})

    #print('\n'.join([str(d) for d in summary]))

    with open("sample.csv", "w", encoding="UTF-8") as out_f:
        out_f.write("class_id\ttext\n")
        out_f.write("\n".join([d['class_id'] + "\t" + d['text'] for d in summary]))

