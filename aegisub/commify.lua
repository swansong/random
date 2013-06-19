-- Copyright (c) 2013, brainchild, brainchild AT commiesubs DOT com
--
-- Permission to use, copy, modify, and distribute this software for any
-- purpose with or without fee is hereby granted, provided that the above
-- copyright notice and this permission notice appear in all copies.
--
-- THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
-- WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
-- MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
-- ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
-- WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
-- ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
-- OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

local tr = aegisub.gettext

script_name = "Commify"
script_description = "Commify a script before initial work begins"
script_author = "brainchild"
script_version = "0.1"

-- a table of somewhat easily replaceable honorifics
honorifics = {
    ["-san"] = "{-san}",
    ["-kun"] = "{-kun}",
    ["-chan"] = "{-chan}",
    ["-senpai"] = "{-senpai}",
    ["-sempai"] = "{-sempai}",
    ["-shi"] = "{-shi}",
    ["-dono"] = "{-dono}",
    ["-tan"] = "{-tan}",
}

function commify(subs)
    for i=1, subs.n do
        local line = subs[i]
        if line.text ~= nil then
            line.text = remove_line_breaks(line.text)
            line.text = remove_honorifics(line.text)
            line.text = replace_double_hyphens(line.text)
            subs[i] = line
        end
    end
    aegisub.set_undo_point(tr"Commify")
end

function remove_line_breaks(text)
    text = text:gsub("\\N", " ")
    text = remove_double_spaces(text)
    
    return text
end

function remove_double_spaces(text)
    while string.find(text, "  ") do
        text = text:gsub("  ", " ")
    end
    
    return text
end

function remove_honorifics(text)
    for k, v in pairs(honorifics) do
        text = text:gsub(k, v)
    end
    
    return text
end

-- this shit better be encoded in UTF-8
function replace_double_hyphens(text)
    text = text:gsub("%-%-", "—")
    
    return text
end

aegisub.register_macro(script_name, script_description, commify)

