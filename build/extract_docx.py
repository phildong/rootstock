#%% imports
import re
from difflib import Differ, HtmlDiff

#%% functions and constants
SRC_FILE = "output/manuscript_docx.md"
DST_FILE = "content/02.delete-me.md"
OUTPUT_FILE = "output/manuscript_docx_clean.md"
DIFF_FILE = "output/diff.html"


def semantic_lining(str_ls):
    res_ls = []
    for line in str_ls:
        s_ls = re.split(r"(\w+ \w+ \w+\.|\].|\.\*|\.\*\*) ", line)
        s_ls_merge = [s_ls[i] + s_ls[i + 1] for i in range(0, len(s_ls) - 1, 2)]
        if len(s_ls) % 2 == 1:
            s_ls_merge.append(s_ls[-1])
        res_ls.extend(s_ls_merge)
    return res_ls


def normalize_links(line):
    return re.sub(r"\[(\[.*?\])\{\.underline\}\](\(.*?\))", r"\1\2", line)


def normalize_figure_captions(str_ls):
    res_ls = []
    skip_idx = []
    for iline, line in enumerate(str_ls):
        if iline in skip_idx:
            continue
        if re.search(r"\!\[Figure.*\]\(media.*\)", line):
            caption = re.search(r"Figure \d+\: (.*)", str_ls[iline + 2]).group(1)
            line = re.sub(r"\!\[Figure.*?\]", "\n".join(["![", caption, "]"]), line)
            res_ls.extend(line.rstrip("\n").split("\n"))
            skip_idx.extend([iline + 1, iline + 2])
        else:
            res_ls.extend([line])
    return res_ls


def anchor_figure(line):
    return re.sub(
        r"\[\]\{(\#fig\:.*) \.anchor\}\!\[(.*)\]\((.*)\)\{(.*)\}",
        r"![\2](\3){\1 \4}",
        line,
    )


def ref_internal(line):
    return re.sub(r"\[\d+\]\(\#(tbl\:.*|fig\:.*|eq\:.*)\)", r"@\1", line)


#%% merge files
if __name__ == "__main__":
    with open(SRC_FILE) as f:
        src_ls = f.readlines()
    with open(DST_FILE) as f:
        dst_ls = f.readlines()
    src_ls = list(map(anchor_figure, src_ls))
    src_ls = list(map(ref_internal, src_ls))
    src_ls = normalize_figure_captions(src_ls)
    src_ls = semantic_lining(src_ls)
    src_ls = list(map(normalize_links, src_ls))
    diff = HtmlDiff(wrapcolumn=90)
    dhtml = diff.make_file(src_ls, dst_ls)
    with open(DIFF_FILE, mode="w") as f:
        f.write(dhtml)
    with open(OUTPUT_FILE, mode="w") as f:
        f.writelines(src_ls)