#!/bin/bash
# Quick reference: Check which manuscript files will be used by each script

echo "=========================================="
echo "Manuscript Input Auto-Detection"
echo "=========================================="
echo ""
echo "Current manuscript files in output/:"
echo "------------------------------------------"
ls -1t output/*.docx 2>/dev/null | grep -E "manuscript|kdp" | head -8
echo ""

echo "=========================================="
echo "Script Inputs"
echo "=========================================="
echo ""

# Check add_toc_and_index.py
echo "1. add_toc_and_index.py"
toc_input=$(ls -t output/travel-books-manuscript-[0-9]*.docx 2>/dev/null | grep -v "with-toc" | grep -v "kdp" | head -1)
if [ -n "$toc_input" ]; then
    echo "   Will use: $(basename $toc_input)"
else
    echo "   ⚠ No input found - run assemble_manuscript.py first"
fi
echo ""

# Check prepare_for_kdp.py
echo "2. prepare_for_kdp.py"
kdp_input=$(ls -t output/travel-books-manuscript-with-toc-*.docx 2>/dev/null | head -1)
if [ -n "$kdp_input" ]; then
    echo "   Will use: $(basename $kdp_input)"
else
    fallback=$(ls -t output/travel-books-manuscript-*.docx 2>/dev/null | head -1)
    if [ -n "$fallback" ]; then
        echo "   Will use: $(basename $fallback) (fallback - no TOC version found)"
    else
        echo "   ⚠ No input found"
    fi
fi
echo ""

echo "=========================================="
echo "To use a specific file instead:"
echo "  python3 ../../shared/scripts/add_toc_and_index.py --manuscript output/filename.docx"
echo "  python3 ../../shared/scripts/prepare_for_kdp.py --manuscript output/filename.docx"
echo "=========================================="
