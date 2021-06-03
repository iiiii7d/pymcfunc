import re
import pymcfunc.internal as internal

def rawtext(text: str, edition: str, special="§"):
    internal.options(edition, ['j', 'b'])
    formatting = {
        'obfuscated': 'k',
        'bold': 'l',
        'strikethrough': 'm',
        'underlined': 'n',
        'italic': 'o'
    }
    colour = {
        '0': 'black',
        '1': 'dark_blue',
        '2': 'dark_green',
        '3': 'dark_aqua',
        '4': 'dark_red',
        '5': 'dark_purple',
        '6': 'gold',
        '7': 'gray',
        '8': 'dark_gray',
        '9': 'blue',
        'a': 'green',
        'b': 'aqua',
        'c': 'red',
        'd': 'light_purple',
        'e': 'yellow',
        'f': 'white'
    }

    cursor = 0
    out = ["", {'text': ''}]

    def append_out(k, v):
        if out[-1]['text'] != '':
            out.append({'text': '', k: v})
        else:
            out[-1][k] = v

    def catchparam(c):
        # c is where [ is
        if text[c] != '[':
            return None, None
        catcher = ''
        orig_c = int(c)
        c += 1
        pc = c-1
        ppc = c-2
        while text[c] != ']' and (text[pc] != '\\' or (text[pc] == '\\' and text[ppc] == '\\')) and c < len(text):
            catcher += text[c]
            c += 1
            pc += 1
            ppc += 1
        if c == len(text):
            return None, None
        
        params = ['']
        for i in range(len(catcher)):
            ch = catcher[i]
            prev_ch = catcher[i-1] if i-1 > 0 else None
            prevprev_ch = catcher[i-2] if i-2 > 0 else None
            if ch == '|' and (prev_ch != '\\' or (prev_ch == '\\' and prevprev_ch == '\\')):
                params.append('')
                continue
            params[-1] += ch
        return params, c-orig_c+1

    while cursor < len(text):
        char = text[cursor]
        next_char = text[cursor+1] if cursor+1 >= len(text) else None
        if char == special:
            params, length = catchparam(cursor+2)
            if next_char in formatting.keys(): #klmno
                append_out(formatting[next_char], True)
                cursor += 2
                continue
            elif next_char in colour.keys(): #0-9a-f
                append_out('color', next_char)
                cursor += 2
                continue
            elif next_char == '#': #hex
                hexc = text[cursor+2:cursor+2+6]
                if re.search(r'^[0-9a-f]{6}$', hexc) is not None:
                    append_out('color', '#'+hexc)
                cursor += 7
                continue
            elif next_char == '@':
                out.append({'selector': text[cursor+2]})
                out.append({'text': ''})
                cursor += 3
                continue
            elif next_char == 'h':
                if params == None or len(params) < 2:
                    cursor += 1
                    continue
                out.append({'score': {'name': params[0], 'objective': params[1]}})
                if len(params) > 2:
                    append_out('value', params[2])
                out.append({'text': ''})
                cursor += 2 + length
                continue
            elif next_char == 'i':
                if params == None or len(params) < 1:
                    cursor += 1
                    continue
                out.append({'keybind': params[0]})
                cursor += 2 + length
                continue
            elif next_char == 'j':
                pass
            elif next_char == 'r': #reset
                if not out[-1] == {'text': ''}:
                    out.append({'text': ''})
                    cursor += 2
                    continue
            cursor += 1
        out[-1]['text'] += char
        cursor += 1
                
                    
