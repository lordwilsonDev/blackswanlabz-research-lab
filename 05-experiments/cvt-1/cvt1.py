# CVT-1: does cheap verification beat expensive generation?  Single-file harness for free Google Colab.
# Cells are separated by "# %%". Pre-registration: ./README.md. Do not edit CONFIG after the first real run.
# %% [markdown]
# Setup (Colab): Runtime > Change runtime type > T4 GPU, then run the cells in order.
# %%
import json, os, random, re, subprocess, sys, tempfile, textwrap, time
from dataclasses import dataclass, field

CONFIG = {
    "local_model": "Qwen/Qwen2.5-Coder-1.5B-Instruct",   # arm B / B-n / C
    "cloud_model": "claude-haiku-4-5-20251001",           # arm A / D, only if ANTHROPIC_API_KEY is set
    "cloud_price_per_mtok": {"in": 1.00, "out": 5.00},    # USD per million tokens; CHECK the current price page and edit BEFORE the run
    "seeds": [0, 1, 2],
    "max_attempts": 4,            # attempt 1 plus up to 3 more (retries or feedback fixes)
    "max_new_tokens": 384,
    "temperature": 0.7,
    "top_p": 0.95,
    "test_timeout_s": 5,
    "margin": 0.10,               # registered: C must beat B-n by at least this much on hidden tests
    "bootstrap_resamples": 5000,
    "out_file": "cvt1_results.jsonl",
}

# %% [markdown]
# Tasks. `visible` tests are shown to the model and drive the retry loop. `hidden` tests are never shown and judge the
# final answer; a pass on visible but fail on hidden is a FALSE PASS. `ref` is a reference solution used only by the self-check.
# %%
def T(id, sig, prompt, visible, hidden, ref):
    return dict(id=id, sig=sig, prompt=prompt, visible=visible.strip(), hidden=hidden.strip(), ref=textwrap.dedent(ref).strip())

TASKS = [
T("roman_to_int", "roman_to_int(s: str) -> int", "Convert a Roman numeral (I V X L C D M, with subtractive pairs like IV and CM) to an integer.",
  "assert roman_to_int('III') == 3\nassert roman_to_int('IV') == 4\nassert roman_to_int('LVIII') == 58",
  "assert roman_to_int('MCMXCIV') == 1994\nassert roman_to_int('CDXLIV') == 444\nassert roman_to_int('MMMCMXCIX') == 3999\nassert roman_to_int('IX') == 9",
  """
  def roman_to_int(s):
      v = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
      t = 0
      for i, c in enumerate(s):
          if i + 1 < len(s) and v[c] < v[s[i+1]]: t -= v[c]
          else: t += v[c]
      return t
  """),
T("int_to_roman", "int_to_roman(n: int) -> str", "Convert an integer from 1 to 3999 to a Roman numeral using subtractive notation.",
  "assert int_to_roman(3) == 'III'\nassert int_to_roman(9) == 'IX'\nassert int_to_roman(58) == 'LVIII'",
  "assert int_to_roman(1994) == 'MCMXCIV'\nassert int_to_roman(444) == 'CDXLIV'\nassert int_to_roman(3999) == 'MMMCMXCIX'\nassert int_to_roman(40) == 'XL'",
  """
  def int_to_roman(n):
      pairs = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
      out = ''
      for v, s in pairs:
          while n >= v:
              out += s; n -= v
      return out
  """),
T("is_balanced", "is_balanced(s: str) -> bool", "Return True if every bracket in s, from the set ()[]{} , is correctly matched and nested. Other characters are ignored.",
  "assert is_balanced('()[]{}') is True\nassert is_balanced('(]') is False\nassert is_balanced('') is True",
  "assert is_balanced('([{}])') is True\nassert is_balanced('((') is False\nassert is_balanced('a(b)c[d]') is True\nassert is_balanced(')(') is False\nassert is_balanced('{[}]') is False",
  """
  def is_balanced(s):
      pairs = {')':'(',']':'[','}':'{'}
      st = []
      for c in s:
          if c in '([{': st.append(c)
          elif c in pairs:
              if not st or st.pop() != pairs[c]: return False
      return not st
  """),
T("merge_intervals", "merge_intervals(iv: list[list[int]]) -> list[list[int]]", "Merge overlapping or touching closed intervals [a, b] (touching means one ends exactly where the next starts). Return the result sorted by start. The input may be unsorted and must not be mutated.",
  "assert merge_intervals([[1,3],[2,6],[8,10]]) == [[1,6],[8,10]]\nassert merge_intervals([]) == []\nassert merge_intervals([[1,4],[4,5]]) == [[1,5]]",
  "assert merge_intervals([[5,6],[1,2],[2,3]]) == [[1,3],[5,6]]\nassert merge_intervals([[1,10],[2,3]]) == [[1,10]]\nx=[[3,4],[1,2]]\nmerge_intervals(x)\nassert x == [[3,4],[1,2]]\nassert merge_intervals([[1,1]]) == [[1,1]]",
  """
  def merge_intervals(iv):
      out = []
      for a, b in sorted(iv):
          if out and a <= out[-1][1]: out[-1][1] = max(out[-1][1], b)
          else: out.append([a, b])
      return out
  """),
T("top_words", "top_words(text: str, k: int) -> list[tuple[str, int]]", "Return the k most frequent words as (word, count) tuples. A word is a maximal run of letters or digits, compared case-insensitively and returned lowercase. Break ties alphabetically.",
  "assert top_words('a b a', 1) == [('a', 2)]\nassert top_words('The the THE cat', 2) == [('the', 3), ('cat', 1)]\nassert top_words('', 3) == []",
  "assert top_words('b a b a c', 2) == [('a', 2), ('b', 2)]\nassert top_words('hi, hi! ho-ho', 3) == [('hi', 2), ('ho', 2)]\nassert top_words('x1 x1 y', 5) == [('x1', 2), ('y', 1)]",
  """
  import re
  from collections import Counter
  def top_words(text, k):
      c = Counter(re.findall(r'[a-z0-9]+', text.lower()))
      return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
  """),
T("flatten", "flatten(x) -> list", "Flatten arbitrarily nested lists into one flat list, preserving order. Strings and tuples are NOT lists and stay as items.",
  "assert flatten([1,[2,3]]) == [1,2,3]\nassert flatten([]) == []\nassert flatten([[[1]]]) == [1]",
  "assert flatten([1,[2,[3,[4,[5]]]]]) == [1,2,3,4,5]\nassert flatten(['ab',['cd']]) == ['ab','cd']\nassert flatten([(1,2),[3]]) == [(1,2),3]\nassert flatten([[],[[]]]) == []",
  """
  def flatten(x):
      out = []
      for i in x:
          if isinstance(i, list): out.extend(flatten(i))
          else: out.append(i)
      return out
  """),
T("rle_encode", "rle_encode(s: str) -> str", "Run-length encode: each run of the same character becomes the character followed by the run length, e.g. 'aaabcc' -> 'a3b1c2'. Empty string gives empty string.",
  "assert rle_encode('aaabcc') == 'a3b1c2'\nassert rle_encode('') == ''\nassert rle_encode('z') == 'z1'",
  "assert rle_encode('a'*12) == 'a12'\nassert rle_encode('abab') == 'a1b1a1b1'\nassert rle_encode('aabbbaa') == 'a2b3a2'",
  """
  def rle_encode(s):
      out = []; i = 0
      while i < len(s):
          j = i
          while j < len(s) and s[j] == s[i]: j += 1
          out.append(s[i] + str(j - i)); i = j
      return ''.join(out)
  """),
T("rle_decode", "rle_decode(s: str) -> str", "Inverse of run-length encoding where each run is one non-digit character followed by a decimal count, e.g. 'a3b1c2' -> 'aaabcc'. Counts can have several digits.",
  "assert rle_decode('a3b1c2') == 'aaabcc'\nassert rle_decode('') == ''\nassert rle_decode('z1') == 'z'",
  "assert rle_decode('a12') == 'a'*12\nassert rle_decode('a1b1a1b1') == 'abab'\nassert rle_decode('x10y2') == 'x'*10 + 'yy'",
  """
  import re
  def rle_decode(s):
      return ''.join(c * int(n) for c, n in re.findall(r'(\\D)(\\d+)', s))
  """),
T("common_prefix", "common_prefix(strs: list[str]) -> str", "Return the longest common prefix of a list of strings, or '' if there is none or the list is empty.",
  "assert common_prefix(['flower','flow','flight']) == 'fl'\nassert common_prefix([]) == ''\nassert common_prefix(['a']) == 'a'",
  "assert common_prefix(['dog','car']) == ''\nassert common_prefix(['abc','abc']) == 'abc'\nassert common_prefix(['', 'abc']) == ''\nassert common_prefix(['interview','internet','interval']) == 'inter'",
  """
  def common_prefix(strs):
      if not strs: return ''
      p = strs[0]
      for s in strs[1:]:
          while not s.startswith(p): p = p[:-1]
      return p
  """),
T("is_anagram", "is_anagram(a: str, b: str) -> bool", "Return True if a and b are anagrams of each other, ignoring case and ignoring spaces (but not other punctuation).",
  "assert is_anagram('listen','silent') is True\nassert is_anagram('a','b') is False\nassert is_anagram('','') is True",
  "assert is_anagram('Dormitory','dirty room') is True\nassert is_anagram('abc','abcc') is False\nassert is_anagram('a-b','ab') is False\nassert is_anagram('Astronomer','Moon starer') is True",
  """
  def is_anagram(a, b):
      f = lambda s: sorted(s.lower().replace(' ', ''))
      return f(a) == f(b)
  """),
T("spiral_order", "spiral_order(m: list[list[int]]) -> list[int]", "Return the elements of a rectangular matrix in clockwise spiral order starting at the top-left. Empty matrix gives [].",
  "assert spiral_order([[1,2],[3,4]]) == [1,2,4,3]\nassert spiral_order([]) == []\nassert spiral_order([[1,2,3]]) == [1,2,3]",
  "assert spiral_order([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]\nassert spiral_order([[1],[2],[3]]) == [1,2,3]\nassert spiral_order([[1,2,3,4],[5,6,7,8],[9,10,11,12]]) == [1,2,3,4,8,12,11,10,9,5,6,7]",
  """
  def spiral_order(m):
      m = [r[:] for r in m]; out = []
      while m:
          out += m.pop(0)
          m = [list(r) for r in zip(*m)][::-1]
      return out
  """),
T("rotate_matrix", "rotate_matrix(m: list[list[int]]) -> list[list[int]]", "Return a new square matrix rotated 90 degrees clockwise. The input must not be mutated.",
  "assert rotate_matrix([[1,2],[3,4]]) == [[3,1],[4,2]]\nassert rotate_matrix([[1]]) == [[1]]\nassert rotate_matrix([]) == []",
  "assert rotate_matrix([[1,2,3],[4,5,6],[7,8,9]]) == [[7,4,1],[8,5,2],[9,6,3]]\nx=[[1,2],[3,4]]\nrotate_matrix(x)\nassert x == [[1,2],[3,4]]",
  """
  def rotate_matrix(m):
      return [list(r) for r in zip(*m[::-1])]
  """),
T("gcd_list", "gcd_list(nums: list[int]) -> int", "Return the greatest common divisor of a list of integers (negative numbers allowed, result is never negative). An empty list gives 0.",
  "assert gcd_list([12, 18]) == 6\nassert gcd_list([]) == 0\nassert gcd_list([7]) == 7",
  "assert gcd_list([0, 5]) == 5\nassert gcd_list([-12, 18]) == 6\nassert gcd_list([0, 0]) == 0\nassert gcd_list([8, 12, 20]) == 4\nassert gcd_list([-7]) == 7",
  """
  from math import gcd
  def gcd_list(nums):
      g = 0
      for n in nums: g = gcd(g, n)
      return g
  """),
T("prime_factors", "prime_factors(n: int) -> list[int]", "Return the prime factors of n in ascending order, with multiplicity. Return [] for n < 2.",
  "assert prime_factors(12) == [2,2,3]\nassert prime_factors(1) == []\nassert prime_factors(13) == [13]",
  "assert prime_factors(0) == []\nassert prime_factors(-5) == []\nassert prime_factors(360) == [2,2,2,3,3,5]\nassert prime_factors(9973) == [9973]\nassert prime_factors(2**10) == [2]*10",
  """
  def prime_factors(n):
      out = []; d = 2
      while n >= 2 and d * d <= n:
          while n % d == 0:
              out.append(d); n //= d
          d += 1
      if n >= 2: out.append(n)
      return out
  """),
T("first_index", "first_index(arr: list[int], x: int) -> int", "arr is sorted ascending and may contain duplicates. Return the index of the FIRST occurrence of x, or -1 if absent. Use binary search (O(log n)).",
  "assert first_index([1,2,3], 2) == 1\nassert first_index([], 5) == -1\nassert first_index([1,3], 2) == -1",
  "assert first_index([1,2,2,2,3], 2) == 1\nassert first_index([2,2,2], 2) == 0\nassert first_index([1,2,3,4,5], 5) == 4\nassert first_index([1,2,3,4,5], 0) == -1\nassert first_index([1,1,1,1], 1) == 0",
  """
  def first_index(arr, x):
      lo, hi = 0, len(arr)
      while lo < hi:
          mid = (lo + hi) // 2
          if arr[mid] < x: lo = mid + 1
          else: hi = mid
      return lo if lo < len(arr) and arr[lo] == x else -1
  """),
T("valid_ipv4", "valid_ipv4(s: str) -> bool", "Return True if s is a valid dotted-quad IPv4 address: exactly four decimal parts, each 0-255, no leading zeros (except '0' itself), digits only.",
  "assert valid_ipv4('192.168.1.1') is True\nassert valid_ipv4('256.1.1.1') is False\nassert valid_ipv4('1.2.3') is False",
  "assert valid_ipv4('0.0.0.0') is True\nassert valid_ipv4('01.2.3.4') is False\nassert valid_ipv4('1.2.3.4.5') is False\nassert valid_ipv4('1.2.3.a') is False\nassert valid_ipv4('255.255.255.255') is True\nassert valid_ipv4('') is False\nassert valid_ipv4('1..2.3') is False",
  """
  def valid_ipv4(s):
      p = s.split('.')
      if len(p) != 4: return False
      for x in p:
          if not x.isdigit() or not x.isascii(): return False
          if len(x) > 1 and x[0] == '0': return False
          if int(x) > 255: return False
      return True
  """),
T("camel_to_snake", "camel_to_snake(s: str) -> str", "Convert CamelCase or camelCase to snake_case. Acronyms stay together: 'HTTPServerError' -> 'http_server_error'. Digits attach to the preceding word.",
  "assert camel_to_snake('camelCase') == 'camel_case'\nassert camel_to_snake('Simple') == 'simple'\nassert camel_to_snake('') == ''",
  "assert camel_to_snake('HTTPServerError') == 'http_server_error'\nassert camel_to_snake('getHTTPResponse') == 'get_http_response'\nassert camel_to_snake('already_snake') == 'already_snake'\nassert camel_to_snake('ABC') == 'abc'\nassert camel_to_snake('version2Beta') == 'version2_beta'",
  """
  import re
  def camel_to_snake(s):
      s = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', s)
      s = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', '_', s)
      return s.lower()
  """),
T("parse_duration", "parse_duration(s: str) -> int", "Parse a duration like '1h30m15s' into seconds. Units are h, m, s, each optional, but they must appear in that order at most once each. Raise ValueError for an empty string, an unknown unit, a missing number, or out-of-order units.",
  "assert parse_duration('1h') == 3600\nassert parse_duration('90s') == 90\nassert parse_duration('1h30m15s') == 5415",
  "assert parse_duration('2m') == 120\nassert parse_duration('0s') == 0\nfor bad in ['', 'h', '5', '5x', '1s2m', '1h1h', '1 h']:\n    try:\n        parse_duration(bad)\n        raise SystemExit('no error for ' + repr(bad))\n    except ValueError:\n        pass",
  """
  import re
  def parse_duration(s):
      m = re.fullmatch(r'(?:(\\d+)h)?(?:(\\d+)m)?(?:(\\d+)s)?', s)
      if not s or not m: raise ValueError(s)
      h, mi, se = (int(x) if x else 0 for x in m.groups())
      return h * 3600 + mi * 60 + se
  """),
T("chunk", "chunk(lst: list, n: int) -> list[list]", "Split lst into consecutive chunks of size n; the last chunk may be shorter. Raise ValueError if n <= 0.",
  "assert chunk([1,2,3,4], 2) == [[1,2],[3,4]]\nassert chunk([], 3) == []\nassert chunk([1,2,3], 2) == [[1,2],[3]]",
  "assert chunk([1,2,3], 5) == [[1,2,3]]\nassert chunk([1,2,3], 1) == [[1],[2],[3]]\nfor bad in (0, -1):\n    try:\n        chunk([1], bad)\n        raise SystemExit('no error')\n    except ValueError:\n        pass",
  """
  def chunk(lst, n):
      if n <= 0: raise ValueError(n)
      return [lst[i:i+n] for i in range(0, len(lst), n)]
  """),
T("dedupe", "dedupe(lst: list) -> list", "Remove duplicates keeping the first occurrence of each item and the original order. Items may be unhashable (such as lists).",
  "assert dedupe([1,2,1,3]) == [1,2,3]\nassert dedupe([]) == []\nassert dedupe(['a','a']) == ['a']",
  "assert dedupe([[1],[2],[1]]) == [[1],[2]]\nassert dedupe([1, 1.0, True]) == [1]\nassert dedupe([3,2,3,2,1]) == [3,2,1]",
  """
  def dedupe(lst):
      out = []
      for x in lst:
          if x not in out: out.append(x)
      return out
  """),
T("max_subarray", "max_subarray(nums: list[int]) -> int", "Return the maximum sum of a non-empty contiguous subarray. For an empty list return 0.",
  "assert max_subarray([1,2,3]) == 6\nassert max_subarray([]) == 0\nassert max_subarray([-1]) == -1",
  "assert max_subarray([-2,1,-3,4,-1,2,1,-5,4]) == 6\nassert max_subarray([-3,-2,-5]) == -2\nassert max_subarray([5,-9,6]) == 6\nassert max_subarray([0,0]) == 0",
  """
  def max_subarray(nums):
      if not nums: return 0
      best = cur = nums[0]
      for x in nums[1:]:
          cur = max(x, cur + x); best = max(best, cur)
      return best
  """),
T("eval_rpn", "eval_rpn(tokens: list[str]) -> int", "Evaluate a Reverse Polish Notation expression with integer tokens and the operators + - * /. Division truncates toward zero (so -7/2 is -3).",
  "assert eval_rpn(['2','1','+','3','*']) == 9\nassert eval_rpn(['4','13','5','/','+']) == 6\nassert eval_rpn(['5']) == 5",
  "assert eval_rpn(['7','-2','/']) == -3\nassert eval_rpn(['-7','2','/']) == -3\nassert eval_rpn(['3','4','-']) == -1\nassert eval_rpn(['10','6','9','3','+','-11','*','/','*','17','+','5','+']) == 22",
  """
  def eval_rpn(tokens):
      st = []
      for t in tokens:
          if t in '+-*/' and len(t) == 1:
              b, a = st.pop(), st.pop()
              st.append(a + b if t == '+' else a - b if t == '-' else a * b if t == '*' else int(a / b))
          else: st.append(int(t))
      return st[0]
  """),
T("count_islands", "count_islands(grid: list[list[int]]) -> int", "Count islands in a grid of 0s and 1s. An island is a group of 1s connected up, down, left or right (not diagonally). The input must not be mutated.",
  "assert count_islands([[1,0],[0,1]]) == 2\nassert count_islands([]) == 0\nassert count_islands([[1,1],[1,1]]) == 1",
  "assert count_islands([[1,1,0,0],[0,1,0,1],[0,0,0,1]]) == 2\nassert count_islands([[0,0],[0,0]]) == 0\ng=[[1,0],[0,1]]\ncount_islands(g)\nassert g == [[1,0],[0,1]]\nassert count_islands([[1,0,1],[0,1,0],[1,0,1]]) == 5",
  """
  def count_islands(grid):
      if not grid: return 0
      seen = set(); n = 0
      for i in range(len(grid)):
          for j in range(len(grid[0])):
              if grid[i][j] == 1 and (i, j) not in seen:
                  n += 1; st = [(i, j)]; seen.add((i, j))
                  while st:
                      a, b = st.pop()
                      for da, db in ((1,0),(-1,0),(0,1),(0,-1)):
                          x, y = a + da, b + db
                          if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 1 and (x, y) not in seen:
                              seen.add((x, y)); st.append((x, y))
      return n
  """),
T("is_palindrome", "is_palindrome(s: str) -> bool", "Return True if s reads the same forwards and backwards, considering only letters and digits and ignoring case. An empty or punctuation-only string is a palindrome.",
  "assert is_palindrome('racecar') is True\nassert is_palindrome('hello') is False\nassert is_palindrome('') is True",
  "assert is_palindrome('A man, a plan, a canal: Panama') is True\nassert is_palindrome('0P') is False\nassert is_palindrome('.,') is True\nassert is_palindrome('ab_a') is True",
  """
  def is_palindrome(s):
      t = [c.lower() for c in s if c.isalnum()]
      return t == t[::-1]
  """),
]

# %% [markdown]
# Sandbox and self-check. The self-check runs every reference solution through its tests, so a broken task fails loudly
# before any model time is spent.
# %%
def run_tests(code, tests, timeout):
    """Run code then tests in a fresh subprocess. Returns (passed, message)."""
    src = code + "\n\n" + tests + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(src); path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        msg = (r.stderr or r.stdout).strip()
        return r.returncode == 0, msg[-600:]
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s"
    finally:
        os.unlink(path)

def selfcheck():
    bad = []
    for t in TASKS:
        ok_v, m1 = run_tests(t["ref"], t["visible"], 10)
        ok_h, m2 = run_tests(t["ref"], t["hidden"], 10)
        if not (ok_v and ok_h): bad.append((t["id"], m1 or m2))
        # a task is only useful if a plausible wrong answer fails hidden: stub must fail visible
        stub_ok, _ = run_tests(f"def {t['sig'].split('(')[0]}(*a, **k):\n    return None", t["visible"], 10)
        if stub_ok: bad.append((t["id"], "stub passes visible tests"))
    ids = [t["id"] for t in TASKS]
    if len(ids) != len(set(ids)): bad.append(("ids", "duplicate task ids"))
    if bad: raise SystemExit(f"SELF-CHECK FAILED: {bad}")
    print(f"self-check OK: {len(TASKS)} tasks, references pass visible+hidden, stubs fail visible")

# %% [markdown]
# Models. LocalModel needs a GPU runtime with transformers. CloudModel is optional (set ANTHROPIC_API_KEY).
# %%
SYSTEM = "You are a careful Python programmer. Reply with exactly one ```python code block that defines the requested function and nothing else: no tests, no prints, no explanations."

def first_prompt(t):
    return (f"Write `{t['sig']}`.\n{t['prompt']}\n\nIt will be checked with tests like these (more cases exist that you cannot see):\n"
            f"```python\n{t['visible']}\n```")

def feedback_prompt(t, code, failure):
    return (first_prompt(t) + f"\n\nYour previous attempt:\n```python\n{code}\n```\nIt failed with:\n```\n{failure}\n```\n"
            "Fix the function. Think about the cases the visible tests do not cover. Reply with the full corrected code block.")

def extract_code(text):
    m = re.findall(r"```(?:python)?\n(.*?)```", text, re.S)
    return (m[-1] if m else text).strip()

@dataclass
class Gen:
    text: str
    tokens_out: int
    tokens_in: int
    seconds: float

class LocalModel:
    def __init__(self, name):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float16, device_map="auto")
    def generate(self, user, seed):
        torch = self.torch
        msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
        ids = self.tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt").to(self.model.device)
        torch.manual_seed(seed)
        t0 = time.time()
        out = self.model.generate(ids, max_new_tokens=CONFIG["max_new_tokens"], do_sample=True,
                                  temperature=CONFIG["temperature"], top_p=CONFIG["top_p"], pad_token_id=self.tok.eos_token_id)
        new = out[0][ids.shape[1]:]
        return Gen(self.tok.decode(new, skip_special_tokens=True), int(new.shape[0]), int(ids.shape[1]), time.time() - t0)

class CloudModel:
    def __init__(self, name):
        import anthropic
        self.client = anthropic.Anthropic()
        self.name = name
    def generate(self, user, seed):
        t0 = time.time()
        r = self.client.messages.create(model=self.name, max_tokens=CONFIG["max_new_tokens"], temperature=CONFIG["temperature"],
                                        system=SYSTEM, messages=[{"role": "user", "content": user}])
        return Gen("".join(b.text for b in r.content if b.type == "text"), r.usage.output_tokens, r.usage.input_tokens, time.time() - t0)

# %% [markdown]
# Arms. Attempt 1 is generated once per (task, seed) and shared by every arm for that model, which pairs the comparison.
#  B   = attempt 1 only.
#  B-n = attempt 1, then independent fresh samples until one passes the VISIBLE tests (verifier, no feedback).
#  C   = attempt 1, then fixes that see the failure message, until one passes the VISIBLE tests (verifier plus feedback).
# Hidden tests judge every arm's final answer. Cloud arms A and D mirror B and C with the cloud model.
# %%
def judge(task, code):
    v, vmsg = run_tests(code, task["visible"], CONFIG["test_timeout_s"])
    h, _ = (run_tests(code, task["visible"] + "\n" + task["hidden"], CONFIG["test_timeout_s"]) if v else (False, ""))
    return v, h, vmsg

def run_arm(model, task, seed, arm, first):
    """Returns dict. `first` is the shared attempt-1 Gen."""
    gens = [first]; code = extract_code(first.text)
    v, h, msg = judge(task, code)
    if arm in ("single",) :
        return pack(gens, v, h)
    attempts = 1
    while not v and attempts < CONFIG["max_attempts"]:
        s = seed * 1000 + attempts
        user = first_prompt(task) if arm == "resample" else feedback_prompt(task, code, msg)
        g = model.generate(user, s); gens.append(g); attempts += 1
        code = extract_code(g.text)
        v, h, msg = judge(task, code)
    return pack(gens, v, h)

def pack(gens, v, h):
    return dict(visible_pass=v, hidden_pass=h, false_pass=bool(v and not h), attempts=len(gens),
                tokens_out=sum(g.tokens_out for g in gens), tokens_in=sum(g.tokens_in for g in gens),
                seconds=round(sum(g.seconds for g in gens), 2))

def run_all(local, cloud=None):
    rows = []
    with open(CONFIG["out_file"], "a") as f:
        for task in TASKS:
            for seed in CONFIG["seeds"]:
                for who, model in (("local", local), ("cloud", cloud)):
                    if model is None: continue
                    first = model.generate(first_prompt(task), seed * 1000)
                    arms = {"local": (("B", "single"), ("B-n", "resample"), ("C", "feedback")),
                            "cloud": (("A", "single"), ("D", "feedback"))}[who]
                    for label, kind in arms:
                        r = run_arm(model, task, seed, kind, first)
                        r.update(task=task["id"], seed=seed, arm=label)
                        rows.append(r); f.write(json.dumps(r) + "\n"); f.flush()
            print("done", task["id"])
    return rows

# %% [markdown]
# Analysis. Decision rule (registered): CVT-1 SUPPORTS the hypothesis only if mean hidden pass of C exceeds B-n by at least
# CONFIG["margin"] AND the 95% bootstrap CI (over tasks) of that difference excludes 0. Anything else counts as NOT supported.
# A tie counts as not supported. All other numbers are descriptive.
# %%
def analyze(rows):
    import statistics
    arms = sorted({r["arm"] for r in rows})
    by = {}
    for r in rows: by.setdefault((r["arm"], r["task"]), []).append(r)
    tasks = sorted({r["task"] for r in rows})
    def task_mean(arm, task, key): 
        v = by.get((arm, task), []); return sum(1 if x[key] is True else (0 if x[key] is False else x[key]) for x in v) / max(1, len(v))
    print(f"{'arm':5} {'hidden':>7} {'visible':>8} {'false-pass':>11} {'attempts':>9} {'tok_out':>8} {'sec':>7}")
    for a in arms:
        n = [x for x in rows if x["arm"] == a]
        m = lambda k: sum(float(x[k]) for x in n) / len(n)
        print(f"{a:5} {m('hidden_pass'):7.3f} {m('visible_pass'):8.3f} {m('false_pass'):11.3f} {m('attempts'):9.2f} {m('tokens_out'):8.0f} {m('seconds'):7.1f}")
    if {"C", "B-n"} <= set(arms):
        diffs = [task_mean("C", t, "hidden_pass") - task_mean("B-n", t, "hidden_pass") for t in tasks]
        rnd = random.Random(12345)
        boots = sorted(statistics.fmean(rnd.choice(diffs) for _ in diffs) for _ in range(CONFIG["bootstrap_resamples"]))
        lo, hi = boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots)) - 1]
        d = statistics.fmean(diffs)
        ok = d >= CONFIG["margin"] and lo > 0
        print(f"\nC minus B-n on hidden tests: {d:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]  margin {CONFIG['margin']}")
        print("REGISTERED DECISION:", "SUPPORTED" if ok else "NOT SUPPORTED")
    if {"A", "C"} <= set(arms):
        p = CONFIG["cloud_price_per_mtok"]
        ca = [x for x in rows if x["arm"] == "A"]; cd = [x for x in rows if x["arm"] == "D"]
        cost = lambda rs: sum(x["tokens_in"] * p["in"] + x["tokens_out"] * p["out"] for x in rs) / 1e6
        print(f"\ncloud cost: A ${cost(ca):.4f}, D ${cost(cd):.4f}. Local arms ran on free Colab: dollar cost 0, which is NOT an energy cost; compare tokens and seconds too.")

# %%
if __name__ == "__main__":
    selfcheck()
    if "--selfcheck" in sys.argv: sys.exit(0)
    local = LocalModel(CONFIG["local_model"])
    cloud = CloudModel(CONFIG["cloud_model"]) if os.environ.get("ANTHROPIC_API_KEY") else None
    print("cloud arms:", "ON" if cloud else "OFF (no ANTHROPIC_API_KEY); only the loop-vs-resample question is tested")
    analyze(run_all(local, cloud))
