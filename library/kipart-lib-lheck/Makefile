
kicad_lib = variscite.lib
kicad_dcm = $(kicad_lib:.lib=.dcm)

csv_files = $(shell find -maxdepth 1 -name "*.csv")
lib_files = $(csv_files:.csv=.lib)

all: $(lib_files) $(kicad_lib) fixes

%.lib: %.csv
	kipart -s row --overwrite $^ -o $@
	@ sed -i "/EESchema-LIBRARY/d" $@
	@ sed -i '1i##' $@
	@ sed -i '2i## $(@:.lib=)' $@
	@ sed -i '3i##' $@

$(kicad_lib): $(lib_files)
	@ echo "Compiling $(kicad_lib)"
	@ rm -rf $(kicad_lib)
	@ rm -rf $(kicad_dcm)
	@ echo "Total number of components = $$(find -maxdepth 1 -name "*.lib" | wc -l)"
	@ for lib_file in $(lib_files); do cat $${lib_file} >> $(kicad_lib); done
	@ echo "Total number of components in library = $$(grep ^DEF $(kicad_lib) | wc -l)"
	@ for dcm_file in $(lib_files:.lib=.dcm); do cat $${dcm_file} >> $(kicad_dcm); done

fixes:
	@ sed -i '1iEESchema-LIBRARY Version 2.3' $(kicad_lib)
	@ sed -i '2i#encoding utf-8' $(kicad_lib)
	@ sed -i "s/Y Y \(.*\) L N/Y Y \1 F N/g" $(kicad_lib) # force yellow background
	@ sed -i "s/S \(.*\) N/S \1 f/g" $(kicad_lib) # force yellow background
	@ #
	@ sed -i '1iEESchema-DOCLIB  Version 2.0' $(kicad_dcm)
	@ echo "#End Doc Library" >> $(kicad_dcm)
	@ sed -i "/^\s*$$/d" $(kicad_dcm)
clean:
	rm -rf $(kicad_lib)
