#!/bin/bash

if [[ $(basename $(pwd)) != "data" ]]
then
    echo "This script must be run from ./data folder."
    exit 1
fi

if [[ ! -e "./aifbfixed_complete.n3" ]]
then
    echo ">>> Downloading aifbfixed_complete.n3"
    wget -q https://ndownloader.figshare.com/files/1118822 
    mv 1118822 aifbfixed_complete.n3
fi

if [[ ! -e "./Lexicon_NamedRockUnit.nt" ]]
then
    echo ">>> Downloading Lexicon_NamedRockUnit.nt"
    wget -q http://data.bgs.ac.uk/downloads/Lexicon_NamedRockUnit.nt
fi

exit 0
