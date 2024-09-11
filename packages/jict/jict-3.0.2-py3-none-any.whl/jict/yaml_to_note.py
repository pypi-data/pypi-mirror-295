import yaml


class Qnote:
    def __init__(self, value , children = []):
        self.value = value
        self.children = children

    def has_children(self):
        return len(self.children) != 0

    def __repr__(self):
        return f"Qnote({self.value},{len(self.children)})"

def parse_note( note ):
    if isinstance(note ,str ):
        return Qnote(note)
    elif isinstance(note,list):
        if len(note) == 0:
            return None
        elif len(note) == 1:
            return Qnote(note[0])
        return Qnote('...',[
            parse_note(n) for n in note if n is not None
        ])

    elif isinstance(note,dict):
        keys = list(note.keys())

        if len(keys) == 1:
            val = note[keys[0]]

            cls = []
            if isinstance(val,list):
                cls = val
            elif isinstance(val,dict):
                cls = [val]
            else:
                cls = [str(val)]

            return Qnote(
                keys[0],[
                    parse_note(c) for c in cls
                ]
            )

        nts = dict_list(note)
        if len(nts) == 0:
            return None

        return Qnote('...' , nts )

    return None

def dict_list( dc ):
    keys = dc.keys()

    if len(keys) == 0:
        return []

    out = []
    for k,v in dc.items():
        cl = []

        if isinstance(v,dict):
            cl = dict_list(v)
        elif isinstance(v,list):
            cl = v
        elif isinstance(v,str):
            cl = [v]
        else:
            cl = [str(v)]

        out.append(Qnote(k,[
            parse_note(c) for c in cl if c is not None
        ]))

    return out


def yaml_to_note( value ):
    notes = []
    try:
        notes = yaml.safe_load( value )
    except yaml.YAMLError:
        return [Qnote(value)]

    if isinstance(notes,list):
        return [
            parse_note(n) for n in notes if n is not None
        ]
    elif isinstance(notes,dict):
        return [
            n for n in dict_list(notes) if n is not None
        ]
    elif isinstance(notes,str):
        return [parse_note(notes)]

    return []
