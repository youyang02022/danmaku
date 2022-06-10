import sys
import json
from collections import defaultdict

ann_file = sys.argv[1]
orig_file = sys.argv[2]
print(sys.argv[0])
print("reading files in...")
with open(ann_file, encoding="UTF-8") as in_ann:
    annotations = json.load(in_ann)

    with open(orig_file, encoding="UTF-8") as in_txt:
        orig_lines = in_txt.readlines()

print("done...")
if annotations is not None and orig_lines is not None:
    print("computing line to annotation map...")
    # get the list of (offset, id) tuple from the tagtok json
    offsets = [(int(e["offsets"][0]['start']), e["classId"]) for e in annotations["entities"]]
    # sort the list by character offset (first element of each pair in the list)
    offsets.sort(key=lambda t: t[0])
    # we'll build a map from line numbers to annotation id
    # the idea is : each character offset in the annotation file corresponds to an annotation.
    # so we will loop over the character offsets in the list 'offsets'
    # and advance in parallel through the lines of the original file.
    # For each offset we move forwards through the lines,
    # until we find the line which includes it in its span.
    # then we update the annotation map for this line and move to the next offset.
    # We continue advancing in parallel from the current line without reset,
    # as the next offset is necessarily contained in a subsequent line
    # since the offsets are sorted by increasing order.
    line_annotations = defaultdict(lambda: "None")
    # we need to keep track of the character offset we're currently looking for
    # we do this by remembering its index in the list 'offsets'
    c_offset_index = 0
    # we need to keep track of the character offset of the first character of the current line
    l_offset = 0
    # The loop over offsets. We need to stop whenever we've found all offsets
    # (or if we've seen all lines)
    # because this makes our stopping condition a bit complicated, we use a while loop
    line_index = 0
    while c_offset_index < len(offsets) and line_index < len(orig_lines):
        # retrieve the current line
        line = orig_lines[line_index]
        # retrieve the character offset we are currently looking for
        target = offsets[c_offset_index][0]
        # we get the character offset for the next line by adding the current line length to the current line offset
        l_offset = l_offset + len(line)
        # we check whether the line contains the character offset we're looking for
        if target < l_offset:
            # in that case we update the map with the relevant annotation
            line_annotations[line_index] = offsets[c_offset_index][1]
            # we'll now be looking for the next offset (if it exists)
            c_offset_index += 1
        # go to the next line (while loop, we mustn't forget to advance)
        line_index += 1
    print("...done")

    print("merging files...")
    # we loop over every line again
    data = []
    for (line_index, line) in enumerate(orig_lines):
        # we retrieve the columns
        columns = line.strip().split("\t")
        # we make a new entry containing the timestamp (column #9) text (column #10) and annotation id
        # to get the annotation id we use the offset to line map
        entry = (columns[6], columns[8], columns[9], line_annotations[line_index])
        # store the entry
        data.append(entry)
    print("...done")

    print("Writing result in {:s}".format(sys.argv[3]))
    with open(sys.argv[3], 'w', encoding="UTF-8") as f_out:
        f_out.write('\n'.join(['\t'.join(entry) for entry in data]))
    print('...done')
