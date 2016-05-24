
TARGET = docs
AFTER = after-body.html
BEFORE = before-body.html
CUSTCSS = ../css/custom.css
MAINCSS = ../css/bootstrap.css

.PHONY: default clean $(TARGET)

default: $(TARGET)

MDFILES = $(wildcard *.md)
HTMLFILES = $(subst .md,.html,$(MDFILES))

$(TARGET): $(HTMLFILES)

%.html: %.md $(BEFORE) $(AFTER) $(MAINCSS) $(CUSTCSS)
	pandoc -s -S --toc -c $(MAINCSS) -c $(CUSTCSS) -B $(BEFORE) -A $(AFTER) $< -o $@

clean:
	find . -type f -name '*.html' -not -name $(BEFORE) -not -name $(AFTER) | xargs rm

