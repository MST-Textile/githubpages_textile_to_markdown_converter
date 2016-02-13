import sys
import re

textileFileName = sys.argv[1]

fmCtr = 0
mdFileName = textileFileName.replace(".textile", ".md")

with open(mdFileName, 'w') as nuPost:
    f = open(textileFileName, 'r', encoding='utf-8', errors='replace')
    linesInPost = f.read().splitlines()
    for line in linesInPost:
        # move past front-matter, preserving it
        if fmCtr < 2:
            if line.startswith("---"):
                fmCtr = fmCtr +1
            nuPost.write(line + '\n')
            continue
        # numbered lists
        if line.startswith('# '):
            line = "1. " + line[len("# "):]

        # block quote
        if line.startswith('bq. '):
            line = "> " + line[len("bq. "):]

        # headings
        if line.startswith('h1. '):
            line = "# " + line[len("h1. "):]
        if line.startswith('h2. '):
            line = "## " + line[len("h2. "):]
        if line.startswith('h3. '):
            line = "### " + line[len("h3. "):]

        # paragraph, and those with deliberate indents
        if line.startswith('p. '):
            line = line[len("p. "):]
        if line.startswith('p(. '):
            line = line[len("p(. "):] + '\n{: style="padding-left: 15px"}'
        if line.startswith('p((. '):
            line = line[len("p((. "):] + '\n{: style="padding-left: 30px"}'
        if line.startswith('p(((. '):
            line = line[len("p(((. "):] + '\n{: style="padding-left: 45px"}'
        if line.startswith('p((((. '):
            line = line[len("p((((. "):] + '\n{: style="padding-left: 60px"}'
        if line.startswith('p(((((. '):
            line = line[len("p(((((. "):] + '\n{: style="padding-left: 75px"}'

        # bullet lists
        if line.startswith('* '):
            line = "- " + line[len("* "):]

        # inlined images
        if line.startswith('!') and line.endswith('!'):
            line = "![](" + line[1:len(line)-1] + ")"

        # convert Pygments sections to Rouge
        if line.startswith('{% highlight %}'):
            line = "```"
        if line.startswith('{% highlight '):
            line = "```" + line.split(" ")[2]
        if line.startswith('{% endhighlight %}'):
            line = "```"

        # hyperlinks
        while True:
            m = re.search('"([^"]|\\")*":http([^\s]*)', line)

            if m:
                found = m.group(0)
                parts = found.split('":')
                shouldBe = "[" + parts[0][1:] + "](" + parts[1] + ")"
                if shouldBe.endswith(".)"):
                    shouldBe = shouldBe[0:len(shouldBe)-2] + ")."
                if shouldBe.endswith(",)"):
                    shouldBe = shouldBe[0:len(shouldBe)-2] + "),"
                line = line.replace(found, shouldBe)
            else:
                break

        # @-delimited code blocks are backtick delimited in kramdown
        while True:
            m = re.search('(@\S*@)', line)
            if m:
                found = m.group(1)
                parts = found.split('@')
                shouldBe = "`" + parts[1] + "`"
                line = line.replace(found, shouldBe)
            else:
                break

        nuPost.write(line + '\n')
