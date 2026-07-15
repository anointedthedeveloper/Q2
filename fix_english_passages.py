import json
import os

def fix_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)

    fixed = 0
    for q in data:
        passage = q.get('passage', '').strip()
        question = q.get('question', '').strip()

        if not passage or not question:
            continue

        # Normalize passage for comparison (collapse whitespace)
        passage_normalized = ' '.join(passage.split())

        # Check if question starts with the passage text
        # Compare first 100 chars of normalized versions
        question_normalized = ' '.join(question.split())
        passage_start = passage_normalized[:100]

        if question_normalized.startswith(passage_start):
            # The question field contains the passage + actual question
            # Find where the passage ends in the question field and extract the real question
            # Strategy: the real question is whatever comes after the passage text
            # We'll strip the passage portion from the question

            # Find the last paragraph/sentence that is NOT part of the passage
            # The passage in question field uses \n as paragraph separator
            # Split question by newlines and find lines not in passage
            q_lines = question.split('\n')
            p_lines = passage.split('\n') if '\n' in passage else [passage]

            # The actual question is typically the last non-empty line(s) after the passage
            # Find lines in question that are not in the passage
            passage_text_flat = ' '.join(passage.split())

            # Rebuild: find the suffix of question that isn't part of passage
            # Try progressively shorter prefixes of question until we find the split point
            actual_question = None

            # Walk backwards through lines to find where passage ends
            for i in range(len(q_lines) - 1, -1, -1):
                candidate_passage = '\n'.join(q_lines[:i]).strip()
                candidate_q = '\n'.join(q_lines[i:]).strip()
                if not candidate_q:
                    continue
                candidate_passage_norm = ' '.join(candidate_passage.split())
                # Check if candidate_passage matches the passage
                if candidate_passage_norm == passage_normalized or passage_normalized.startswith(candidate_passage_norm[:min(len(candidate_passage_norm), len(passage_normalized))]):
                    # Check the other direction: does passage start with candidate_passage?
                    if len(candidate_passage_norm) > 50 and passage_normalized.startswith(candidate_passage_norm[:100]):
                        actual_question = candidate_q
                        break

            if actual_question is None:
                # Fallback: just take the last non-empty line
                non_empty = [l.strip() for l in q_lines if l.strip()]
                if non_empty:
                    # Check if last line looks like a question (not part of passage)
                    last_line = non_empty[-1]
                    last_line_norm = ' '.join(last_line.split())
                    if last_line_norm not in passage_normalized:
                        actual_question = last_line

            if actual_question and actual_question.strip() != question.strip():
                q['question'] = actual_question.strip()
                fixed += 1

    print(f"{os.path.basename(filepath)}: fixed {fixed} questions")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

fix_file(r'c:\Users\Admin\Desktop\Q2\Use of English.json')
