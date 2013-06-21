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

script_name = "Contractions"
script_description = "Apply valid contractions to a script"
script_author = "brainchild"
script_version = "0.1"

-- table of contractions
contractions = {
    -- lovely double contractions
    ["would have"] = "would've",
    ["would not have"] = "wouldn't've",
    ["wouldn't have"] = "wouldn't've",
    ["should have"] = "should've",
    ["should not have"] = "shouldn't've",
    ["shouldn't have"] = "shouldn't've",
    ["could have"] = "could've",
    ["could not have"] = "couldn't've",
    ["couldn't have"] = "couldn't've",
    
    ["Would have"] = "Would've",
    ["Would not have"] = "Wouldn't've",
    ["Wouldn't have"] = "Wouldn't've",
    ["Should have"] = "Should've",
    ["Should not have"] = "Shouldn't've",
    ["Shouldn't have"] = "Shouldn't've",
    ["Could have"] = "Could've",
    ["Could not have"] = "Couldn't've",
    ["Couldn't have"] = "Couldn't've",

    -- other commonly used contractions
    ["I am "] = "I'm ",
    ["I am$"] =  "I'm",
    ["cannot"] = "can't",
    ["can not"] = "can't",
    ["are not"] = "aren't",
    ["did not"] = "didn't",
    ["does not"] = "doesn't",
    ["do not"] = "don't",
    ["had not"] = "hadn't",
    ["has not"] = "hasn't",
    ["have not"] = "haven't",
    ["must not"] = "mustn't",
    ["let us"] = "let's",
    ["must have"] = "must've",
    
    ["Cannot"] = "Can't",
    ["Can not"] = "Can't",
    ["Are not"] = "Aren't",
    ["Did not"] = "Didn't",
    ["Does not"] = "Doesn't",
    ["Do not"] = "Don't",
    ["Had not"] = "Hadn't",
    ["Has not"] = "Hasn't",
    ["Have not"] = "Haven't",
    ["Must not"] = "Mustn't",
    ["Let us"] = "Let's",
    ["Must have"] = "Must've",
}

-- apply valid contractions to a subtitles object
function contract(subs)
    -- go through subtitles
    for i=1, subs.n do
        -- apply valid contractions
        for k, v in pairs(contractions) do
            local line = subs[i]
            if line.text ~= nil then
                line.text = line.text:gsub(k, v)
                subs[i] = line
            end
        end
    end
    aegisub.set_undo_point(tr"contractions")
end

aegisub.register_macro(script_name, script_description, contract)
