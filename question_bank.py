"""Deterministic, reviewable arithmetic/reasoning practice-question generator.

25 distinct questions per topic/level; answers are computed, not guessed. The
bank is seeded into the database only when the operator runs seed_questions.py.
"""
from fractions import Fraction

TOPICS = {
    'QA': ('Average', 'Profit & Loss', 'Ratio & Proportion'),
    'LR': ('Blood Relations', 'Coding-Decoding', 'Number/Letter Series'),
}


def _mcq(text, answer, wrong, explanation):
    answer = str(answer)
    options = [answer] + [str(v) for v in wrong if str(v) != answer]
    options = list(dict.fromkeys(options))
    if len(options) < 4:
        raise ValueError(f'Not enough distinct options: {text}')
    # Rotate the correct answer across A-D, deterministically per question.
    shift = sum(map(ord, text)) % 4
    options = options[:4]
    options = options[shift:] + options[:shift]
    return dict(question_text=text, option_a=options[0], option_b=options[1],
                option_c=options[2], option_d=options[3],
                correct_option='ABCD'[options.index(answer)], explanation=explanation)


def _numeric(text, answer, explanation, step=1):
    return _mcq(text, answer, (answer-step, answer+step, answer+2*step), explanation)


def _average(level, k, kind):
    n = 4 + k + level
    avg = 12 + 2*level + 3*k
    if kind == 0:
        return _numeric(f'The average of {n} values is {avg}. Find their sum.', n*avg,
                        f'Sum = count × average = {n} × {avg} = {n*avg}.', n)
    if kind == 1:
        x = avg + 2*k + level
        new = (n*avg + x)//(n+1)
        x = (n+1)*new-n*avg
        return _numeric(f'The average of {n} values is {avg}. A new value {x} is added. Find the new average.',
                        new, f'New average = ({n} × {avg} + {x}) / {n+1} = {new}.')
    if kind == 2:
        x = avg + n*(k+1)
        return _numeric(f'The average of {n} numbers is {avg}. If {x} is removed, find the average of the remaining {n-1} numbers.',
                        avg-(k+1), f'({n} × {avg} − {x}) / {n-1} = {avg-(k+1)}.')
    if kind == 3:
        delta = k+level+1
        return _numeric(f'The average of {n} numbers is {avg}. Each number increases by {delta}. Find the new average.',
                        avg+delta, f'Adding {delta} to each value increases the average by {delta}.')
    missing = avg + (n-1)*(k+1)
    known_avg = avg-(k+1)
    return _numeric(f'The average of {n} numbers is {avg}; the first {n-1} have average {known_avg}. Find the last number.',
                    missing, f'Last = {n} × {avg} − {n-1} × {known_avg} = {missing}.')


def _profit(level, k, kind):
    cp = 100*(level+k+5)
    pct = 5*(k+level+1)
    if kind == 0:
        ans = cp*(100+pct)//100
        return _numeric(f'An item costs Rs {cp} and is sold at {pct}% profit. Find the selling price in rupees.',
                        ans, f'SP = {cp} × (100 + {pct}) / 100 = {ans}.', 50)
    if kind == 1:
        ans = cp*(100-pct//2*2)//100
        loss = pct//2*2
        return _numeric(f'An item costs Rs {cp} and is sold at {loss}% loss. Find the selling price in rupees.',
                        ans, f'SP = {cp} × (100 − {loss}) / 100 = {ans}.', 50)
    if kind == 2:
        sp = cp*(100+pct)//100
        return _numeric(f'An article bought for Rs {cp} is sold for Rs {sp}. Find the profit percentage.',
                        pct, f'Profit % = ({sp} − {cp}) / {cp} × 100 = {pct}%.', 5)
    if kind == 3:
        sp = cp*(100+pct)//100
        return _numeric(f'A trader sells an article for Rs {sp} at {pct}% profit. Find its cost price in rupees.',
                        cp, f'CP = {sp} × 100 / (100 + {pct}) = {cp}.', 100)
    marked = cp*2
    discount = 5*(k+1)
    sp = marked*(100-discount)//100
    return _numeric(f'A product marked Rs {marked} is sold at {discount}% discount. Find the selling price in rupees.',
                    sp, f'SP = {marked} × (100 − {discount}) / 100 = {sp}.', 50)


def _ratio(level, k, kind):
    a = level+k+2
    b = a+k+1
    multiplier = level+k+3
    if kind == 0:
        total = (a+b)*multiplier
        return _numeric(f'Two amounts are in the ratio {a}:{b}; their sum is {total}. Find the first amount.',
                        a*multiplier, f'First = {total} × {a}/({a}+{b}) = {a*multiplier}.', multiplier)
    if kind == 1:
        total = (a+b)*multiplier
        return _numeric(f'Two amounts are in the ratio {a}:{b}; their sum is {total}. Find the second amount.',
                        b*multiplier, f'Second = {total} × {b}/({a}+{b}) = {b*multiplier}.', multiplier)
    if kind == 2:
        return _numeric(f'A:B = {a}:{b}. If A = {a*multiplier}, find B.',
                        b*multiplier, f'B = {a*multiplier} × {b}/{a} = {b*multiplier}.', multiplier)
    if kind == 3:
        c = b+level+1
        return _numeric(f'A:B = {a}:{b} and B:C = {b}:{c}. If A = {a*multiplier}, find C.',
                        c*multiplier, f'A:B:C = {a}:{b}:{c}; C = {c} × {multiplier} = {c*multiplier}.', multiplier)
    total = (a+b)*multiplier
    return _numeric(f'The ratio of boys to girls is {a}:{b}. There are {total} students. How many more girls than boys?',
                    (b-a)*multiplier, f'Difference = ({b} − {a}) × {multiplier} = {(b-a)*multiplier}.', multiplier)


def _series(level, k, kind):
    start = level*3+k+2
    d = level+k+2
    if kind == 0:
        seq = [start+i*d for i in range(5)]
        ans = start+5*d
        return _numeric(f'Find the next term: {", ".join(map(str,seq))}, ?', ans,
                        f'Add {d} each time; next = {seq[-1]} + {d} = {ans}.', d)
    if kind == 1:
        seq = [start+i*i*d for i in range(5)]
        ans = start+25*d
        return _numeric(f'Find the next term: {", ".join(map(str,seq))}, ?', ans,
                        f'Terms follow {start} + n² × {d}; for n=5, answer = {ans}.', d)
    if kind == 2:
        factor = 2+(k%2)
        seq = [start*factor**i for i in range(5)]
        ans = seq[-1]*factor
        return _numeric(f'Find the next term: {", ".join(map(str,seq))}, ?', ans,
                        f'Multiply each term by {factor}; next = {ans}.', start)
    if kind == 3:
        seq = [start+i*(i+1) for i in range(5)]
        ans = start+30
        return _numeric(f'Find the next term: {", ".join(map(str,seq))}, ?', ans,
                        f'Terms are {start} + n(n+1); n=5 gives {ans}.', 2)
    start_letter = (level+k)%12
    step = 1+(k%3)
    seq = [chr(65+start_letter+i*step) for i in range(5)]
    ans = chr(65+start_letter+5*step)
    wrong = [chr(65+start_letter+5*step+j) for j in (1,2,3)]
    return _mcq(f'Find the next letter: {", ".join(seq)}, ?', ans, wrong,
                f'Advance {step} letter(s) each time; next letter is {ans}.')


def _coding(level, k, kind):
    words = ('TRAIN', 'CLOUD', 'LOGIC', 'PLANT', 'BRAVE')
    word = words[k]
    shift = 1+(level+kind)%8
    def encode(w, n):
        return ''.join(chr(65+(ord(ch)-65+n)%26) for ch in w)
    if kind == 0:
        ans = encode(word, shift)
        return _mcq(f'In a code, every letter is shifted {shift} places forward (Z wraps to A). How is {word} coded?',
                    ans, (encode(word,shift+1),encode(word,shift+2),encode(word,shift+3)),
                    f'Shift each letter of {word} forward by {shift}: {ans}.')
    if kind == 1:
        coded = encode(word,shift)
        return _mcq(f'Each letter is shifted {shift} places forward to code a word. Decode {coded}.',
                    word, (encode(word,1),encode(word,2),encode(word,3)),
                    f'Shift each letter of {coded} backward by {shift}: {word}.')
    if kind == 2:
        ans = word[::-1]
        return _mcq(f'A code reverses the order of letters in a word. How is {word} coded?',
                    ans, (encode(ans,1),encode(ans,2),encode(ans,3)),
                    f'Read {word} from right to left: {ans}.')
    if kind == 3:
        ans = '-'.join(str(ord(c)-64) for c in word)
        wrong = ['-'.join(str(ord(c)-64+j) for c in word) for j in (1,2,3)]
        return _mcq(f'If A=1, B=2, ..., Z=26, write the code for {word} using hyphens.',
                    ans, wrong, f'Convert each letter of {word} to its alphabet position: {ans}.')
    ans = encode(word[::-1],shift)
    return _mcq(f'Reverse {word}, then shift each letter {shift} places forward (Z wraps to A). Find the code.',
                ans, (encode(word,shift),encode(word[::-1],shift+1),encode(word[::-1],shift+2)),
                f'Reverse to {word[::-1]}, then shift by {shift}: {ans}.')


def _blood(level, k, kind):
    names = ('Asha', 'Bina', 'Charu', 'Divya', 'Esha')
    x = names[k]
    y = ('Ravi', 'Mohan', 'Kiran', 'Nitin', 'Sagar')[k]
    z = ('Neha', 'Pooja', 'Rina', 'Tara', 'Uma')[k]
    # All genders and family relationships are explicitly specified.
    scenarios = (
        (f'{x} is the mother of {y}. {y} is the father of {z}. How is {x} related to {z}?', 'Grandmother',
         'Grandfather', 'Aunt', 'Mother', f'{x} is the mother of {z}’s father, so she is the grandmother.'),
        (f'{y} is the brother of {x}. {x} is the mother of {z}. How is {y} related to {z}?', 'Maternal uncle',
         'Father', 'Paternal grandfather', 'Brother', f'{y} is the brother of {z}’s mother, hence maternal uncle.'),
        (f'{x} is the sister of {y}. {y} is the father of {z}. How is {x} related to {z}?', 'Paternal aunt',
         'Mother', 'Maternal aunt', 'Grandmother', f'{x} is the sister of {z}’s father, hence paternal aunt.'),
        (f'{y} is the father of {x}. {x} is the mother of {z}. How is {y} related to {z}?', 'Maternal grandfather',
         'Paternal grandfather', 'Uncle', 'Brother', f'{y} is the father of {z}’s mother, hence maternal grandfather.'),
        (f'{z} is the daughter of {x}. {x} is the sister of {y}. How is {z} related to {y}?', 'Niece',
         'Nephew', 'Aunt', 'Sister', f'{z} is the daughter of {y}’s sister, hence niece.'),
    )
    q, answer, *rest = scenarios[kind]
    return _mcq(f'[Family reasoning, Level {level}] {q}', answer, rest[:3], rest[3])

GENERATORS = {
    ('QA', 'Average'): _average,
    ('QA', 'Profit & Loss'): _profit,
    ('QA', 'Ratio & Proportion'): _ratio,
    ('LR', 'Blood Relations'): _blood,
    ('LR', 'Coding-Decoding'): _coding,
    ('LR', 'Number/Letter Series'): _series,
}


def generate_questions(subject, topic, level):
    """Return 25 unique MCQs for a specific QA/LR topic and test level."""
    if not 1 <= level <= 10:
        raise ValueError('Level must be between 1 and 10.')
    generator = GENERATORS[(subject, topic)]
    questions = [generator(level, k, kind) for kind in range(5) for k in range(5)]
    texts = [q['question_text'] for q in questions]
    if len(texts) != len(set(texts)):
        raise ValueError(f'Duplicate questions in {subject}/{topic}/{level}')
    return questions
