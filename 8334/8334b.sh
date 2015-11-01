echo "First do ./8334.sh  > /tmp/8334-raw.md"
wc -w /tmp/8334-raw.md


echo "<div class=\"pagebreak\"></div>" > appendix.md
echo "## Appendix" >> appendix.md
echo "" >> appendix.md

for FILENAME in 8334.sh randomsentencebot.py 8334b.sh 8334.css
do
    echo "### $FILENAME" >> appendix.md
    echo "<pre>" >> appendix.md
    cat $FILENAME >> appendix.md
    echo "</pre>" >> appendix.md
    echo "" >> appendix.md
    echo "<div class=\"pagebreak\"></div>" >> appendix.md
done

cat frontmatter.md /tmp/8334-raw.md appendix.md > 8334.md

multimarkdown 8334.md > 8334.html
open 8334.html

echo "Print to PDF using Chrome"
