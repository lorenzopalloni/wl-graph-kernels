cat Lexicon_NamedRockUnit.nt | grep hasLithogenesis\> | awk '{ print $3 }' | sort | uniq -c | sort -n | tail -n 2
