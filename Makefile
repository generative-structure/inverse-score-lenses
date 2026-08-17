# Regenerate every statistic and every figure from the pinned inputs.
# Override the interpreter with:  make PY=/path/to/python

PY ?= python3

FIGS := fig1_design fig2_confusion fig3_information fig4_loco fig5_signatures

.PHONY: all macros figures clean

all: macros figures

macros:
	$(PY) ops/make_p2_macros.py

figures:
	cd figures/src && for f in $(FIGS); do $(PY) $$f.py || exit 1; done

clean:
	rm -f results_macros.tex figures/*.pdf
	rm -rf ops/__pycache__ figures/src/__pycache__ __pycache__
