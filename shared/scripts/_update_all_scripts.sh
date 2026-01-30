#!/bin/bash
# Batch update all Python scripts to add book_utils import at the top

SCRIPTS=(
    "update_status.py"
    "check_book.py"
    "change_status.py"
    "organize_books.py"
    "validate_manuscript.py"
    "create_honorable_mentions_files.py"
    "write_honorable_mentions_descriptions.py"
)

for script in "${SCRIPTS[@]}"; do
    echo "Updating $script..."

    # Check if already has book_utils import
    if grep -q "from book_utils import" "$script"; then
        echo "  Already has book_utils import, skipping"
        continue
    fi

    # Add import after the last import line
    sed -i '/^from\|^import/a\from book_utils import find_book_root, load_config, get_book_path' "$script" || true

    echo "  ✓ Added book_utils import"
done

echo "Done!"
