"""
Dataset Generator
created by Ezra Anthony, 3/2026
GUI created and algorithm updated by Neha Jeyaram, 7/2026

CSV format:
    output symbols, input morpheme labels

contexts:
    blank = no restriction
    # on the left = word-initial
    # on the right = word-final

application modes:
    Simultaneous / input-local
    Iterative left-to-right
    Iterative right-to-left
"""

import ast
import csv
import itertools
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


SIMULTANEOUS = "Simultaneous / input-local"
LEFT_TO_RIGHT = "Iterative left-to-right"
RIGHT_TO_LEFT = "Iterative right-to-left"


def parse_symbols(text):
    return text.split() if text.strip() else []


def parse_context(text):

    text = text.strip()

    if text == "":
        return None

    if text == "#":
        return "#"

    return tuple(parse_symbols(text))


def parse_morphemes(text):
    """
    supports both:

    Line format
        A:t a t
        B:t a d t
        C:a

    Python-list format
        [('A', 't a t'), ('B', 't a d t'), ('C', 'a')]

    """
    text = text.strip()

    if not text:
        raise ValueError("Please enter at least one morpheme.")

    try:
        parsed = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        parsed = None

    if parsed is not None:
        if not isinstance(parsed, (list, tuple)):
            raise ValueError(
                "Python-format morphemes must be a list or tuple."
            )

        morphemes = []

        for item in parsed:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                raise ValueError(
                    "Each morpheme must contain exactly a label and a form."
                )

            label = str(item[0]).strip()
            form = str(item[1]).strip()

            if not label:
                raise ValueError("Morpheme labels cannot be empty.")

            morphemes.append((label, tuple(parse_symbols(form))))

        if not morphemes:
            raise ValueError("Please enter at least one morpheme.")

        return morphemes

    morphemes = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            raise ValueError(
                f"Invalid morpheme on line {line_number}: "
                "expected MORPHEMES:output."
            )

        label, form = line.split(":", 1)
        label = label.strip()
        form = form.strip()

        if not label:
            raise ValueError(
                f"Morpheme label is missing on line {line_number}."
            )

        morphemes.append((label, tuple(parse_symbols(form))))

    if not morphemes:
        raise ValueError("Please enter at least one valid morpheme.")

    return morphemes


def left_context_matches(symbols, start, left_context):

    if left_context is None:
        return True

    if left_context == "#":
        return start == 0

    context_length = len(left_context)

    if start < context_length:
        return False

    return tuple(symbols[start - context_length:start]) == left_context


def right_context_matches(symbols, end, right_context):

    if right_context is None:
        return True

    if right_context == "#":
        return end == len(symbols)

    context_length = len(right_context)

    if end + context_length > len(symbols):
        return False

    return tuple(symbols[end:end + context_length]) == right_context


def rule_matches_at(
    symbols,
    start,
    target,
    left_context,
    right_context
):
    
    end = start + len(target)

    if end > len(symbols):
        return False

    if target and tuple(symbols[start:end]) != target:
        return False

    return (
        left_context_matches(symbols, start, left_context)
        and right_context_matches(symbols, end, right_context)
    )


def apply_simultaneously(symbols, target, replacement, left_context, right_context):

    symbols = list(symbols)

    # insertion
    if not target:
        matching_positions = {position for position in range(len(symbols) + 1) if rule_matches_at(symbols, position, target, left_context, right_context)}

        result = []

        for position in range(len(symbols) + 1):
            if position in matching_positions:
                result.extend(replacement)

            if position < len(symbols):
                result.append(symbols[position])

        return result

    matches = []
    position = 0

    while position <= len(symbols) - len(target):
        if rule_matches_at(symbols, position, target, left_context, right_context):
            matches.append(position)
            position += len(target)
        else:
            position += 1

    result = []
    current_position = 0

    for match_position in matches:
        result.extend(symbols[current_position:match_position])
        result.extend(replacement)
        current_position = match_position + len(target)

    result.extend(symbols[current_position:])
    return result


def apply_left_to_right(symbols, target, replacement, left_context, right_context):

    result = list(symbols)

    # insertion
    if not target:
        position = 0

        while position <= len(result):
            if rule_matches_at(result, position, target, left_context, right_context):
                result[position:position] = replacement
                position += len(replacement) + 1
            else:
                position += 1

        return result

    position = 0

    while position <= len(result) - len(target):
        if rule_matches_at(result, position, target, left_context, right_context):
            result[position:position + len(target)] = replacement

            # moving on
            if replacement:
                position += len(replacement)
        else:
            position += 1

    return result


def apply_right_to_left(symbols, target, replacement, left_context, right_context):

    result = list(symbols)

    # insertion
    if not target:
        position = len(result)

        while position >= 0:
            if rule_matches_at(result, position, target, left_context, right_context):
                result[position:position] = replacement

            position -= 1

        return result

    position = len(result) - len(target)

    while position >= 0:
        if rule_matches_at(result, position, target, left_context, right_context):
            result[position:position + len(target)] = replacement

        position -= 1

    return result


def apply_rule(symbols, target, replacement, left_context, right_context, application_mode):

    if application_mode == SIMULTANEOUS:
        return apply_simultaneously(symbols, target, replacement, left_context, right_context)

    if application_mode == LEFT_TO_RIGHT:
        return apply_left_to_right(symbols, target, replacement, left_context, right_context)

    if application_mode == RIGHT_TO_LEFT:
        return apply_right_to_left(symbols, target, replacement, left_context, right_context)

    raise ValueError("Invalid rule-application mode.")


def dataset_generator(left_context, right_context, morphemes, target, replacement, maximum_length, application_mode):

    dataset = []

    for sequence_length in range(1, maximum_length + 1):
        for morpheme_sequence in itertools.product(
            morphemes,
            repeat=sequence_length
        ):
            labels = tuple(
                morpheme[0] for morpheme in morpheme_sequence
            )

            underlying_symbols = []

            for _, form in morpheme_sequence:
                underlying_symbols.extend(form)

            output_symbols = apply_rule(
                underlying_symbols,
                target,
                replacement,
                left_context,
                right_context,
                application_mode
            )

            dataset.append((tuple(output_symbols), labels))

    return dataset


def write_to_csv(filename, dataset):

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        for output_symbols, morpheme_labels in dataset:
            writer.writerow([
                " ".join(output_symbols),
                " ".join(morpheme_labels)
            ])


def generate_dataset():

    try:
        morphemes = parse_morphemes(
            morphemes_input.get("1.0", tk.END)
        )

        left_context = parse_context(
            left_context_entry.get()
        )
        right_context = parse_context(
            right_context_entry.get()
        )

        target = tuple(parse_symbols(target_entry.get()))
        replacement = tuple(parse_symbols(output_entry.get()))

        maximum_text = maximum_length_entry.get().strip()

        if not maximum_text:
            raise ValueError(
                "Please enter a maximum morpheme sequence length."
            )

        try:
            maximum_length = int(maximum_text)
        except ValueError as error:
            raise ValueError(
                "Maximum sequence length must be a whole number."
            ) from error

        if maximum_length < 1:
            raise ValueError(
                "Maximum sequence length must be at least 1."
            )

        application_mode = application_mode_box.get()

        if application_mode not in {
            SIMULTANEOUS,
            LEFT_TO_RIGHT,
            RIGHT_TO_LEFT
        }:
            raise ValueError(
                "Please select a rule-application mode."
            )

        # prevents empty rule
        if not target and not replacement:
            raise ValueError(
                "The target and output cannot both be empty. "
                "For deletion, enter a target and leave the output empty."
            )

        number_of_morphemes = len(morphemes)
        number_of_examples = sum(
            number_of_morphemes ** length
            for length in range(1, maximum_length + 1)
        )

        # size warning
        if number_of_examples > 100000:
            proceed = messagebox.askyesno(
                "Large Dataset",
                f"This will generate {number_of_examples:,} examples. "
                "Do you want to continue?"
            )

            if not proceed:
                return

        filename = filedialog.asksaveasfilename(
            title="Save Dataset",
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if not filename:
            return

        dataset = dataset_generator(
            left_context=left_context,
            right_context=right_context,
            morphemes=morphemes,
            target=target,
            replacement=replacement,
            maximum_length=maximum_length,
            application_mode=application_mode
        )

        write_to_csv(filename, dataset)

        messagebox.showinfo(
            "Success",
            f"Dataset written to:\n{filename}\n\n"
            f"Examples generated: {len(dataset):,}"
        )

    except (ValueError, OSError, csv.Error) as error:
        messagebox.showerror("Error", str(error))


def add_labeled_entry(parent, label_text, default=""):

    tk.Label(parent, text=label_text).pack(anchor="w")

    entry = tk.Entry(parent, width=60)
    entry.insert(0, default)
    entry.pack(fill="x", pady=(0, 8))

    return entry

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Dataset Generator")
    root.geometry("650x750")

    main_frame = tk.Frame(root, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

    tk.Label(
        main_frame,
        text=(
            "Morphemes\n"
            "Use A:t a t on separate lines, or Python-list format."
        ),
        justify="left"
    ).pack(anchor="w")

    morphemes_input = tk.Text(main_frame, height=9, width=60)
    morphemes_input.pack(fill="x", pady=(0, 10))

    # default example
    morphemes_input.insert(
        "1.0",
        "A:t a t\n"
        "B:t a d t\n"
        "C:a\n"
        "D:t a d\n"
    )

    left_context_entry = add_labeled_entry(main_frame, "Left context (blank = unrestricted; # = word boundary):")
    right_context_entry = add_labeled_entry(main_frame, "Right context (blank = unrestricted; # = word boundary):")
    target_entry = add_labeled_entry(main_frame, "Target symbol(s) (leave empty for insertion):")
    output_entry = add_labeled_entry(main_frame, "Output symbol(s) (leave empty for deletion):")
    maximum_length_entry = add_labeled_entry(main_frame, "Maximum morpheme sequence length:", default="3")

    tk.Label(main_frame, text="Rule-application mode:").pack(anchor="w")

    application_mode_box = ttk.Combobox(
        main_frame,
        values=[
            SIMULTANEOUS,
            LEFT_TO_RIGHT,
            RIGHT_TO_LEFT
        ],
        state="readonly",
        width=40
    )
    application_mode_box.set(SIMULTANEOUS)
    application_mode_box.pack(anchor="w", pady=(0, 12))

    tk.Button(main_frame, text="Generate and Save Dataset", command=generate_dataset).pack(pady=10)

    root.mainloop()