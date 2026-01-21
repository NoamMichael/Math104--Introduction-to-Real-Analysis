.PHONY: all master clean

# Default: build master PDF and copy to root
all: master

# Build master.pdf and copy to root directory
master:
	cd notes/latex/master && pdflatex -interaction=nonstopmode master.tex
	cd notes/latex/master && pdflatex -interaction=nonstopmode master.tex  # Run twice for TOC
	cp notes/latex/master/master.pdf ./Math104-name "*.synctex.gz" -delete
