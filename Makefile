.PHONY: all master clean

# Default: build master PDF and copy to root
all: master

# Build master.pdf and copy to root directory
master:
	cd notes/latex/master && pdflatex -interaction=nonstopmode master.tex
	cd notes/latex/master && pdflatex -interaction=nonstopmode master.tex
	cp notes/latex/master/master.pdf ./Math104-Notes.pdf

# Build a specific lecture (usage: make lec01)
lec%:
	cd notes/latex/$@ && pdflatex -interaction=nonstopmode $@.tex

# Clean auxiliary files
clean:
	find notes/latex -name "*.aux" -delete
	find notes/latex -name "*.log" -delete
	find notes/latex -name "*.out" -delete
	find notes/latex -name "*.toc" -delete
	find notes/latex -name "*.fls" -delete
	find notes/latex -name "*.fdb_latexmk" -delete
	find notes/latex -name "*.synctex.gz" -delete
