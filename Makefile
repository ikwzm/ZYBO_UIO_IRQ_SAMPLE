
target  : sample1 sample2

sample1 : sample1.c sample_common.h
	gcc sample1.c -o sample1

sample2 : sample2.c sample_common.h
	gcc sample2.c -o sample2

DTC=dtc
DEVICETREE_SOURCE=./devicetrees/Linux-Digilent-Dev/devicetree.dts

devicetree.dtb : $(DEVICETREE_SOURCE)
	$(DTC) -I dts -O dtb -o $@ $<
