#!/usr/bin/env bash

set -x

wget -P data/ https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.id.300.vec.gz
wget -P data/ http://ilps.science.uva.nl/ilps/wp-content/uploads/sites/6/files/bahasaindonesia/kompas.zip
wget -P data/ http://ilps.science.uva.nl/ilps/wp-content/uploads/sites/6/files/bahasaindonesia/tempo.zip