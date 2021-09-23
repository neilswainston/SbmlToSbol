#!/bin/bash

## CHECK INPUT FOLDER
if [ "$1" = "" ]; then
	echo "*** ERROR: $0 needs an input folder path."
    echo "Exiting..."
    exit
elif [ ${1::1} != "/" ]; then
    echo "*** ERROR: Input folder path must be absolute."
    echo "Exiting..."
    exit
else
    INPUT=$1
fi

## CHECK OUTFILE
if [ "$2" = "" ]; then
	echo "*** ERROR: $0 needs an output filename."
    echo "Exiting..."
    exit
elif [ ${2::1} != "/" ]; then
    echo "*** ERROR: Output filename must have absolute path."
    echo "Exiting..."
    exit
else
    OUTFILE=$2
    OUTPUT_DIR=$(dirname "$OUTFILE")
fi

## CHECK RBS
if [ "$3" = "" ]; then
    RBS="True"
else
    RBS=$3
fi

docker run --rm -v $INPUT:/data -v $OUTPUT_DIR:$OUTPUT_DIR sbml2sbol \
    --input /data \
    --outfile $OUTFILE \
    --rbs $RBS