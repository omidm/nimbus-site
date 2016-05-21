
TARGET = docs
CSSFILE = buttondown.css

.PHONY: default clean $(TARGET)

default: $(TARGET)

MDFILES = $(wildcard *.md)
HTMLFILES = $(subst .md,.html,$(MDFILES))

$(TARGET): $(HTMLFILES)

%.html: %.md
	pandoc -s -S --toc -c $(CSSFILE) $< -o $@

clean:
	rm *.html

