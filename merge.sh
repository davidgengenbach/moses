combine() {
    IN=$1
    OUT="$IN/all.pdf"
    /System/Library/Automator/Combine\ PDF\ Pages.action/Contents/Resources/join.py --output $OUT $IN/*.pdf 2>/dev/null
}

for el in \
    "exercises"\
    "exercises/solutions"\
    "modules"; do
    echo "Merging: $el"
    rm -f $el/all.pdf
    combine $el
done