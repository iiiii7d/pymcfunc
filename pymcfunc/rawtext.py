import re
import pymcfunc.internal as internal
#from traceback import format_exc

def _compress(out):
    out = [i for i in out if isinstance(i, str) or 'text' not in i.keys() or ('text' in i.keys() and i['text'] != "")]
    return out

def _catchparam(c, text):
        # c is where [ is
        if c >= len(text) or text[c] != '[':
            return None, None
        catcher = ''
        orig_c = int(c)
        c += 1
        pc = c-1
        ppc = c-2
        indent = 0
        while not (text[c] == ']' and indent == 0) or (text[c] == ']' and (text[pc] == '\\' and text[ppc] != '\\')) and c < len(text):
            catcher += text[c]
            if text[c] == '[' and (text[pc] != '\\' or (text[pc] == '\\' and text[ppc] == '\\')): indent += 1
            if text[c] == ']' and (text[pc] != '\\' or (text[pc] == '\\' and text[ppc] == '\\')): indent -= 1
            c += 1
            pc += 1
            ppc += 1
        if c == len(text):
            return None, None

        indent = 0
        params = ['']
        for i in range(len(catcher)):
            ch = catcher[i]
            prev_ch = catcher[i-1] if i-1 > 0 else None
            prevprev_ch = catcher[i-2] if i-2 > 0 else None
            next_ch = catcher[i+1] if i+1 < len(catcher) else None
            if ch == '[' and (prev_ch != '\\' or (prev_ch == '\\' and prevprev_ch == '\\')): indent += 1
            if ch == ']' and (prev_ch != '\\' or (prev_ch == '\\' and prevprev_ch == '\\')): indent -= 1
            if ch == '|' and indent == 0 and (prev_ch != '\\' or (prev_ch == '\\' and prevprev_ch == '\\')):
                params.append('')
                continue
            if ch == '\\' and (next_ch == '|' or next_ch == '\\') and (prev_ch != '\\' or (prev_ch == '\\' and prevprev_ch == '\\')) and indent == 0:
                continue
            params[-1] += ch
        return params, c-orig_c+2

def java(text: str, format_symbol="§", content_symbol="¶"):
    """Converts a string of text into Java raw JSON text.\n
    **Formatting symbols**
    * **§#XXXXXX** - Hex code
    * **§0-9, a-f** - Colours
    * **§h[text]** - Extras to append after the segment of text
    * **§i[text]** - String to be inserted into chat when clicked
    * **§j[text]** - Sets the font
    * **§k** - Obfuscate
    * **§l** - Bold
    * **§m** - Strikethrough
    * **§n** - Underline
    * **§o** - Italics
    * **§p[url]** - Opens URL when text is clicked
    * **§q[file]** - Opens file (might not work) when text is clicked
    * **§r** - Reset all formatting
    * **§s[command]** - Sends a command to chat input / runs the command when text is clicked
    * **§t[value]** - Appends a value to chat input when text is clicked
    * **§u[page]** - Changes the page in books when text is clicked
    * **§v[value]** - Copies value to clipboard when text is clicked
    * **§w[text]** - Shows text when text is hovered
    * **§xX** - Removes formatting of X
    * **§y[item id|optional count|optional tag]** - Shows item when hovered
    * **§z[entity type|entity uuid|optional entity name]** - Shows entity when hovered
 
    **Content symbols**
    * **¶t[identifier|params...|...]** - Translated text
    * **¶s[name|objective|optional value]** - Value from scoreboard
    * **¶e[selector|optional separator text]** - Entity name
    * **¶k[identifier]** - Keybind
    * **¶n[path|type|val|optional interpret|optional separator text]** - NBT value (choose 'type' from block, entity, storage, 'interpet' from true, false)\n
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.rt.java"""
    format_codes = {
        '#': ('color', None),
        '0': ('color', 'black'),
        '1': ('color', 'dark_blue'),
        '2': ('color', 'dark_green'),
        '3': ('color', 'dark_aqua'),
        '4': ('color', 'dark_red'),
        '5': ('color', 'dark_purple'),
        '6': ('color', 'gold'),
        '7': ('color', 'gray'),
        '8': ('color', 'dark_gray'),
        '9': ('color', 'blue'),
        'a': ('color', 'green'),
        'b': ('color', 'aqua'),
        'c': ('color', 'red'),
        'd': ('color', 'light_purple'),
        'e': ('color', 'yellow'),
        'f': ('color', 'white'),
        'h': ('extra', []),
        'i': ('insertion', ''),
        'j': ('font', ''),
        'k': ('obfuscated', True),
        'l': ('bold', True),
        'm': ('strikethrough', True),
        'n': ('underlined', True),
        'o': ('italic', True),
        'p': ('clickEvent', {'action': 'open_url', 'value': ''}),
        'q': ('clickEvent', {'action': 'open_file', 'value': ''}),
        'r': None,
        's': ('clickEvent', {'action': 'run_command', 'value': ''}),
        't': ('clickEvent', {'action': 'suggest_command', 'value': ''}),
        'u': ('clickEvent', {'action': 'change_page', 'value': ''}),
        'v': ('clickEvent', {'action': 'copy_clipboard', 'value': ''}),
        'w': ('hoverEvent', {'action': 'show_text', 'contents': {}}),
        'x': None,
        'y': ('hoverEvent', {'action': 'show_item', 'contents': {}}),
        'z': ('hoverEvent', {'action': 'show_entity', 'contents': {}})
    }
    format_params_required = 'hijpqstuvwyz'

    cursor = 0
    kwargs = {}
    out = ["", {'text': ''}]

    def append_out(d):
        if out[-1]['text'] != '':
            out.append({'text': '', **d})
        else:
            for k, v in d.items():
                out[-1][k] = v

    while cursor < len(text):
        char = text[cursor]
        next_char = text[cursor+1] if cursor+1 < len(text) else None
        if char == format_symbol:
            if next_char == format_symbol:
                out[-1]['text'] += char
                cursor += 2
                continue
            params, length = _catchparam(cursor+2, text)
            if (params is None and next_char in format_params_required.split()) \
               or next_char not in format_codes.keys():
                out[-1]['text'] += char
                cursor += 1
                continue

            if next_char == '#': #hex
                hexc = text[cursor+2:cursor+2+6]
                if re.search(r'^[0-9a-f]{6}$', hexc) is not None:
                    kwargs['color'] = '#'+hexc
                    append_out(kwargs)
                    cursor += 8
                    continue
                else:
                    out[-1]['text'] += char
                    cursor += 1
                    continue
            elif next_char == 'r': #reset
                kwargs = {}
                append_out(kwargs)
                cursor += 2
                continue
            elif next_char == 'x': #clear
                nextnext_char = text[cursor+2] if cursor+2 < len(text) else None
                k, _ = format_codes[nextnext_char]
                try: 
                    del kwargs[k]
                    append_out(kwargs)
                except KeyError: 
                    #print(format_exc())
                    pass
                
                cursor += 3
                continue
            
            k, v = format_codes[next_char]
            if k == 'clickEvent':
                v['value'] = params[0]
            elif k == 'hoverEvent':
                if v['action'] == 'show_text':
                    v['content'] = java(params[0], format_symbol, content_symbol)
                elif v['action'] == 'show_item':
                    v['content'] = {'id': params[0]}
                    if len(params) >= 2: v['content']['count'] = int(params[1])
                    if len(params) >= 3: v['content']['tag'] = params[2]
                elif v['action'] == 'show_entity':
                    if len(params) < 2:
                        if length is None: length = 0
                        cursor += 2 + length
                        continue
                    v['content'] = {'type': params[0], 'id': params[1]}
                    if len(params) >= 3: v['content']['name'] = java(params[2], format_symbol, content_symbol)
            elif next_char in 'ij':
                v = params[0]
            elif next_char == 'h':
                v = java(params[0], format_symbol, content_symbol)
            kwargs[k] = v
            append_out(kwargs)
            if length is None: length = 0
            cursor += 2 + length
            continue
        
        elif char == content_symbol:
            if next_char == content_symbol:
                out[-1]['text'] += char
                cursor += 2
                continue
            params, length = _catchparam(cursor+2, text)
            if params is None:
                out[-1]['text'] += char
                cursor += 1
                continue
            
            if next_char == 't':
                out.append({
                    'translate': params[0],
                    **kwargs
                })
                if len(params) > 1: out[-1]['with'] = [java(i, format_symbol, content_symbol) for i in params[1:]]
            elif next_char == 's':
                if len(params) < 2:
                    if length is None: length = 0
                    cursor += 2 + length
                    continue
                out.append({'score': {
                    'name': params[0],
                    'objective': params[1]},
                    **kwargs
                })
                if len(params) > 2: out[-1]['score']['value'] = params[2]
            elif next_char == 'e':
                out.append({
                    'selector': params[0],
                    **kwargs
                })
                if len(params) > 1: out[-1]['separator'] = java(params[1], format_symbol, content_symbol)
            elif next_char == 'k':
                out.append({
                    'keybind': params[0],
                    **kwargs
                })
            elif next_char == 'n':
                if len(params) < 3:
                    if length is None: length = 0
                    cursor += 2 + length
                    continue
                out.append({
                    'nbt': params[0],
                    params[1]: params[2],
                    **kwargs
                })
                if len(params) > 3: out[-1]['interpret'] = params[3]
                if len(params) > 4: out[-1]['separator'] = java(params[4], format_symbol, content_symbol)
            else:
                out[-1]['text'] += char
                cursor += 1
                continue

            out.append({'text': ''})
            cursor += 2 + length
            continue
            
        out[-1]['text'] += char
        cursor += 1
                
    out = _compress(out)
    if len(out) == 2: out = out[1]
    return out

def bedrock(text: str, content_symbol="¶"):
    """Converts a string of text into Bedrock raw JSON text.\n
    **Content symbols**
    * **¶t[identifier|params...|...]** - Translated text
    * **¶s[name|objective|optional value]** - Value from scoreboard
    * **¶e[selector|optional separator text]** - Entity name\n
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.rt.bedrock"""
    cursor = 0
    kwargs = {}
    out = [{'text': ''}]

    while cursor < len(text):
        char = text[cursor]
        next_char = text[cursor+1] if cursor+1 < len(text) else None

        if char == content_symbol:
            if next_char == content_symbol:
                out[-1]['text'] += char
                cursor += 2
                continue
            params, length = _catchparam(cursor+2, text)
            if params is None:
                out[-1]['text'] += char
                cursor += 1
                continue
            
            if next_char == 't':
                out.append({
                    'translate': params[0],
                    **kwargs
                })
                if len(params) > 1: out[-1]['with'] = [bedrock(i, content_symbol)['rawtext'][0] for i in params[1:]]
            elif next_char == 's':
                if len(params) < 2:
                    if length is None: length = 0
                    cursor += 2 + length
                    continue
                out.append({'score': {
                    'name': params[0],
                    'objective': params[1]},
                    **kwargs
                })
                if len(params) > 2: out[-1]['score']['value'] = params[2]
            elif next_char == 'e':
                out.append({
                    'selector': params[0],
                    **kwargs
                })
            else:
                out[-1]['text'] += char
                cursor += 1
                continue

            out.append({'text': ''})
            cursor += 2 + length
            continue
            
        out[-1]['text'] += char
        cursor += 1

    out = _compress(out)
    return {'rawtext': out}