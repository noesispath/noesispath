pythonquestions = [
    {
        "id": 1,
        "title": "Two Sum",
        "description": """Given an array of integers nums and an integer target, \nreturn indices of the two numbers that add up to target.\nYou may assume each input has exactly one solution.""",
        "difficulty": "easy",
        "topic": "hashmap",
        "expected_time": 15,
        "test_cases": [
            {"input": "4\n2 7 11 15\n9", "expected_output": "[0, 1]"},
            {"input": "3\n3 2 4\n6", "expected_output": "[1, 2]"},
            {"input": "2\n3 3\n6", "expected_output": "[0, 1]"},
        ],
        "hints": {
            "level_1": "What data structure lets you check if a value exists in O(1)?",
            "level_2": "For each number, check if target minus that number exists in a hashmap.",
            "level_3": "Iterate once. For each nums[i], check if (target - nums[i]) is already in your hashmap. If yes, return indices. If no, store nums[i] with its index."
        },
        "examples": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0, 1]",
                "explanation": "nums[0] + nums[1] = 2 + 7 = 9"
            },
            {
                "input": "nums = [3,2,4], target = 6",
                "output": "[1, 2]",
                "explanation": "nums[1] + nums[2] = 2 + 4 = 6"
            },
            {
                "input": "nums = [3,3], target = 6",
                "output": "[0, 1]",
                "explanation": "nums[0] + nums[1] = 3 + 3 = 6"
            }
        ],
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists"
        ],
        "follow_up": "Can you come up with an algorithm that is less than O(n²) time complexity?",
        "learn": {
            "concept": "Hashmap lookup",
            "explanation": "The fastest way to solve this is by storing numbers as you iterate and checking whether the complement to the target already exists. A hashmap lets you do that lookup in constant time, so you can solve it in one pass.",
            "analogy": "It is like keeping a list of groceries and checking whether the item you need is already on the shelf before you buy a second one.",
            "key_properties": [
                "Maps values to indices for O(1) lookup",
                "Builds incrementally while scanning the array",
                "Stops as soon as the target pair is found",
                "Avoids nested loops and O(n²) time"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Hashmap practice", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python dictionary documentation", "url": "https://docs.python.org/3/tutorial/datastructures.html#dictionaries", "type": "article"}
            ]
        },
        "starter_code": """n = int(input())\nnums = list(map(int, input().split()))\ntarget = int(input())\n\ndef two_sum(nums, target):\n    # Write your code here\n    return []\n\nresult = two_sum(nums, target)\nprint(result)\n"""
    },
    {
        "id": 2,
        "title": "Valid Anagram",
        "description": """Given two strings s and t, return true if t is an anagram of s, and false otherwise.""",
        "difficulty": "easy",
        "topic": "hashmap",
        "expected_time": 10,
        "test_cases": [
            {"input": "anagram\nnagaram", "expected_output": "true"},
            {"input": "rat\ncar", "expected_output": "false"},
            {"input": "a\na", "expected_output": "true"},
        ],
        "hints": {
            "level_1": "How can you count the frequency of each character?",
            "level_2": "Use a hashmap to count characters in both strings and compare.",
            "level_3": "Sort both strings or use collections.Counter to compare character counts."
        },
        "examples": [
            {
                "input": "s = 'anagram', t = 'nagaram'",
                "output": "true",
                "explanation": "Both strings have the same characters and frequencies."
            },
            {
                "input": "s = 'rat', t = 'car'",
                "output": "false",
                "explanation": "Different characters: 'r','a','t' vs 'c','a','r'."
            },
            {
                "input": "s = 'a', t = 'a'",
                "output": "true",
                "explanation": "Identical single-character strings."
            }
        ],
        "constraints": [
            "1 <= s.length, t.length <= 5 * 10^4",
            "s and t consist of lowercase English letters"
        ],
        "follow_up": "What if the inputs contain Unicode characters?",
        "learn": {
            "concept": "Frequency counting with hashmaps",
            "explanation": "Valid Anagram is about comparing how many times each character appears in both strings. A hashmap is ideal for counting character frequency and then checking whether the two strings have the same counts.",
            "analogy": "It is like counting the number of red and blue marbles in two jars to see if both jars have the same collection.",
            "key_properties": [
                "Counts characters in O(n) time",
                "Uses a hashmap to compare frequency maps",
                "Handles different string lengths quickly",
                "Can use one pass with incremental counting"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Hashmap practice", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python dictionary documentation", "url": "https://docs.python.org/3/tutorial/datastructures.html#dictionaries", "type": "article"}
            ]
        },
        "starter_code": """s = input()\nt = input()\n\ndef is_anagram(s, t):\n    # Write your code here\n    return False\n\nresult = is_anagram(s, t)\nprint(result)\n"""
    },
    {
        "id": 3,
        "title": "Best Time to Buy Stock",
        "description": """You are given an array prices where prices[i] is the price of a stock on the ith day.\nFind the maximum profit you can achieve from one transaction.""",
        "difficulty": "easy",
        "topic": "sliding window",
        "expected_time": 15,
        "test_cases": [
            {"input": "6\n7 1 5 3 6 4", "expected_output": "5"},
            {"input": "5\n7 6 4 3 1", "expected_output": "0"},
            {"input": "5\n1 2 3 4 5", "expected_output": "4"},
        ],
        "hints": {
            "level_1": "Track the minimum price so far as you iterate.",
            "level_2": "At each step, calculate profit if you sold today.",
            "level_3": "Use two pointers or a single pass to keep track of min price and max profit."
        },
        "examples": [
            {
                "input": "prices = [7,1,5,3,6,4]",
                "output": "5",
                "explanation": "Buy on day 2 (price=1), sell on day 5 (price=6). Profit = 6-1 = 5."
            },
            {
                "input": "prices = [7,6,4,3,1]",
                "output": "0",
                "explanation": "Prices only decrease, so no transaction is profitable."
            },
            {
                "input": "prices = [1,2,3,4,5]",
                "output": "4",
                "explanation": "Buy on day 1 (price=1), sell on day 5 (price=5). Profit = 5-1 = 4."
            }
        ],
        "constraints": [
            "1 <= prices.length <= 10^5",
            "0 <= prices[i] <= 10^4"
        ],
        "follow_up": "Can you solve this problem in a single pass with O(1) extra space?",
        "learn": {
            "concept": "Single-pass max profit",
            "explanation": "The key idea is to remember the lowest price seen so far and calculate the profit if you sold at the current price. That way you can find the maximum profit in one sweep through the array.",
            "analogy": "It is like watching stock prices and always remembering the cheapest day so you can sell later for the biggest gain.",
            "key_properties": [
                "Tracks a running minimum price",
                "Updates the best profit at each step",
                "Uses O(1) extra space",
                "Avoids nested comparisons by scanning once"
            ],
            "resources": [
                {"title": "NeetCode YouTube — One-pass trading problems", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python built-in min() documentation", "url": "https://docs.python.org/3/library/functions.html#min", "type": "article"}
            ]
        },
        "starter_code": """n = int(input())\nprices = list(map(int, input().split()))\n\ndef max_profit(prices):\n    # Write your code here\n    return 0\n\nresult = max_profit(prices)\nprint(result)\n"""
    },
    {
        "id": 4,
        "title": "Contains Duplicate",
        "description": """Given an integer array nums, return true if any value appears at least twice.""",
        "difficulty": "easy",
        "topic": "array",
        "expected_time": 8,
        "test_cases": [
            {"input": "4\n1 2 3 1", "expected_output": "true"},
            {"input": "4\n1 2 3 4", "expected_output": "false"},
            {"input": "3\n1 1 1", "expected_output": "true"},
        ],
        "hints": {
            "level_1": "What data structure can check for duplicates in O(1)?",
            "level_2": "Use a set to track seen numbers.",
            "level_3": "If a number is already in the set, return true. Otherwise, add it to the set."
        },
        "examples": [
            {
                "input": "nums = [1,2,3,1]",
                "output": "true",
                "explanation": "1 appears at index 0 and 3."
            },
            {
                "input": "nums = [1,2,3,4]",
                "output": "false",
                "explanation": "All elements are distinct."
            },
            {
                "input": "nums = [1,1,1]",
                "output": "true",
                "explanation": "1 appears three times."
            }
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^9 <= nums[i] <= 10^9"
        ],
        "follow_up": "Can you solve this with O(n) time and O(n) extra space?",
        "learn": {
            "concept": "Duplicate detection with a set",
            "explanation": "The fastest way to detect duplicates is to track seen values in a set while you scan the array. If a value is already present, you can return true immediately.",
            "analogy": "It is like checking a guest list by crossing names off as people arrive and spotting the first repeated name.",
            "key_properties": [
                "Uses set membership for O(1) checks",
                "Scans the array once",
                "Can exit early on first duplicate",
                "Requires O(n) extra space in the worst case"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Hashmap practice", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python set documentation", "url": "https://docs.python.org/3/library/stdtypes.html#set", "type": "article"}
            ]
        },
        "starter_code": """n = int(input())\nnums = list(map(int, input().split()))\n\ndef contains_duplicate(nums):\n    # Write your code here\n    return False\n\nresult = contains_duplicate(nums)\nprint(result)\n"""
    },
    {
        "id": 5,
        "title": "Maximum Subarray",
        "description": """Given an integer array nums, find the contiguous subarray with the largest sum.""",
        "difficulty": "medium",
        "topic": "array",
        "expected_time": 20,
        "test_cases": [
            {"input": "9\n-2 1 -3 4 -1 2 1 -5 4", "expected_output": "6"},
            {"input": "1\n1", "expected_output": "1"},
            {"input": "5\n-1 -2 -3 -4 -5", "expected_output": "-1"},
        ],
        "hints": {
            "level_1": "What algorithm finds max subarray sum in O(n)?",
            "level_2": "Use a running sum and reset if it drops below zero.",
            "level_3": "Kadane's algorithm: max_sum = max(max_sum, current_sum); current_sum = max(current_sum + num, num)."
        },
        "examples": [
            {
                "input": "nums = [-2,1,-3,4,-1,2,1,-5,4]",
                "output": "6",
                "explanation": "Subarray [4,-1,2,1] has the largest sum = 6."
            },
            {
                "input": "nums = [1]",
                "output": "1",
                "explanation": "Single element is the only subarray."
            },
            {
                "input": "nums = [-1,-2,-3,-4,-5]",
                "output": "-1",
                "explanation": "All negatives — the least negative element -1 is the maximum subarray."
            }
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4"
        ],
        "follow_up": "Can you do this in O(n) time and O(1) space?",
        "learn": {
            "concept": "Kadane's algorithm",
            "explanation": "Maximum Subarray is solved by keeping a running sum and resetting whenever the sum drops below zero. The maximum sum seen during the scan is the answer.",
            "analogy": "It is like tracking your best winning streak: if your current streak becomes negative, start a new streak from the next game.",
            "key_properties": [
                "Maintains a running current sum",
                "Resets when the current sum is negative",
                "Keeps track of the maximum sum seen",
                "Works in one linear pass"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Kadane's algorithm", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python max() documentation", "url": "https://docs.python.org/3/library/functions.html#max", "type": "article"}
            ]
        },
        "starter_code": """n = int(input())\nnums = list(map(int, input().split()))\n\ndef max_subarray(nums):\n    # Write your code here\n    return 0\n\nresult = max_subarray(nums)\nprint(result)\n"""
    },
    {
        "id": 6,
        "title": "Valid Parentheses",
        "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.""",
        "difficulty": "easy",
        "topic": "stack",
        "expected_time": 10,
        "test_cases": [
            {"input": "()[]{}", "expected_output": "true"},
            {"input": "(]", "expected_output": "false"},
            {"input": "([{}])", "expected_output": "true"},
        ],
        "hints": {
            "level_1": "What data structure can help match opening and closing brackets?",
            "level_2": "Push opening brackets to a stack, pop for closing.",
            "level_3": "If the stack is empty or mismatched on pop, return false."
        },
        "examples": [
            {
                "input": "s = '()[]{}'",
                "output": "true",
                "explanation": "Every opening bracket has a matching closing bracket in order."
            },
            {
                "input": "s = '(]'",
                "output": "false",
                "explanation": "'(' expects ')' but gets ']'."
            },
            {
                "input": "s = '([{}])'",
                "output": "true",
                "explanation": "Nested brackets are all properly matched."
            }
        ],
        "constraints": [
            "1 <= s.length <= 10^4",
            "s consists only of '()[]{}'"
        ],
        "follow_up": "Can you solve this with O(n) time and O(n) space?",
        "learn": {
            "concept": "Stack-based bracket matching",
            "explanation": "A stack lets you match brackets in the correct nested order. Push opening characters and pop when a matching closing bracket appears.",
            "analogy": "It is like nesting boxes: the last box you put on top must be the first one you take off.",
            "key_properties": [
                "Push opening brackets onto the stack",
                "Pop and compare when encountering closers",
                "Reject mismatches immediately",
                "The stack must be empty at the end"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Stack problems", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python list as stack documentation", "url": "https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks", "type": "article"}
            ]
        },
        "starter_code": """s = input()\n\ndef is_valid_parentheses(s):\n    # Write your code here\n    return False\n\nresult = is_valid_parentheses(s)\nprint(result)\n"""
    },
    {
        "id": 7,
        "title": "Reverse Linked List",
        "description": """Given the head of a singly linked list, reverse the list and return the reversed list.""",
        "difficulty": "easy",
        "topic": "linked list",
        "expected_time": 15,
        "test_cases": [
            {"input": "5\n1 2 3 4 5", "expected_output": "[5, 4, 3, 2, 1]"},
            {"input": "3\n1 2 3", "expected_output": "[3, 2, 1]"},
            {"input": "1\n1", "expected_output": "[1]"},
        ],
        "hints": {
            "level_1": "What pointers do you need to reverse a linked list?",
            "level_2": "Iterate and reverse the next pointers one by one.",
            "level_3": "Use prev, curr, and next pointers to reverse the list in-place."
        },
        "examples": [
            {
                "input": "head = [1,2,3,4,5]",
                "output": "[5,4,3,2,1]",
                "explanation": "Each node's next pointer is reversed."
            },
            {
                "input": "head = [1,2,3]",
                "output": "[3,2,1]",
                "explanation": "Three-node list reversed."
            },
            {
                "input": "head = [1]",
                "output": "[1]",
                "explanation": "Single-node list stays the same."
            }
        ],
        "constraints": [
            "0 <= n <= 5000",
            "-10^5 <= node.val <= 10^5"
        ],
        "follow_up": "Can you implement this iteratively and recursively?",
        "learn": {
            "concept": "In-place linked list reversal",
            "explanation": "Reverse the linked list by walking through it with pointers and rewiring each node's next reference to point backward. No extra list structure is needed.",
            "analogy": "It is like reversing a line of dominoes by turning each one to face the opposite direction, one at a time.",
            "key_properties": [
                "Use prev, curr, and next pointers",
                "Reverse links in place without extra storage",
                "Move forward through the list exactly once",
                "Return the new head when finished"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Linked list problems", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Real Python linked list guide", "url": "https://realpython.com/linked-lists-python/", "type": "article"}
            ]
        },
        "starter_code": """n = int(input())
        
head = list(map(int, input().split()))\n\ndef reverse_linked_list(head):\n    # Write your code here\n    return []\n\nresult = reverse_linked_list(head)\nprint(result)\n"""
    },
    {
        "id": 8,
        "title": "Binary Search",
        "description": """Given a sorted array of integers nums and a target value, return the index if the target is found. If not, return -1.""",
        "difficulty": "easy",
        "topic": "binary search",
        "expected_time": 12,
        "test_cases": [
            {"input": "6\n-1 0 3 5 9 12\n9", "expected_output": "4"},
            {"input": "6\n-1 0 3 5 9 12\n2", "expected_output": "-1"},
            {"input": "1\n1\n1", "expected_output": "0"},
        ],
        "hints": {
            "level_1": "What is the time complexity of binary search?",
            "level_2": "Use two pointers (left, right) and check the middle element.",
            "level_3": "If nums[mid] == target, return mid. If nums[mid] < target, search right. Else, search left."
        },
        "examples": [
            {
                "input": "nums = [-1,0,3,5,9,12], target = 9",
                "output": "4",
                "explanation": "9 is at index 4."
            },
            {
                "input": "nums = [-1,0,3,5,9,12], target = 2",
                "output": "-1",
                "explanation": "2 does not exist in the array."
            },
            {
                "input": "nums = [1], target = 1",
                "output": "0",
                "explanation": "Target 1 is at index 0."
            }
        ],
        "constraints": [
            "1 <= nums.length <= 10^4",
            "-10^4 <= nums[i] <= 10^4",
            "-10^4 <= target <= 10^4"
        ],
        "follow_up": "Can you implement this iteratively?",
        "learn": {
            "concept": "Divide-and-conquer search",
            "explanation": "Binary search repeatedly halves the searchable range in a sorted list until the target is found or the range is empty. It runs in logarithmic time.",
            "analogy": "It is like finding a word in a dictionary by opening near the middle and deciding whether to look left or right.",
            "key_properties": [
                "Requires sorted input",
                "Uses left/right pointers around mid",
                "Halves the search range each step",
                "Returns index or -1 if not found"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Binary search", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python bisect module documentation", "url": "https://docs.python.org/3/library/bisect.html", "type": "article"}
            ]
        },
        "starter_code": """n = int(input())\nnums = list(map(int, input().split()))\ntarget = int(input())\n\ndef binary_search(nums, target):\n    # Write your code here\n    return -1\n\nresult = binary_search(nums, target)\nprint(result)\n"""
    },
    {
        "id": 9,
        "title": "Climbing Stairs",
        "description": """You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. In how many distinct ways can you climb to the top?""",
        "difficulty": "easy",
        "topic": "recursion/dp",
        "expected_time": 10,
        "test_cases": [
            {"input": "2", "expected_output": "2"},
            {"input": "3", "expected_output": "3"},
            {"input": "5", "expected_output": "8"},
        ],
        "hints": {
            "level_1": "What is the recurrence relation for this problem?",
            "level_2": "f(n) = f(n-1) + f(n-2)",
            "level_3": "Use dynamic programming or recursion with memoization."
        },
        "examples": [
            {
                "input": "n = 2",
                "output": "2",
                "explanation": "Two ways: (1+1) or (2)."
            },
            {
                "input": "n = 3",
                "output": "3",
                "explanation": "Three ways: (1+1+1), (1+2), or (2+1)."
            },
            {
                "input": "n = 5",
                "output": "8",
                "explanation": "Follows the Fibonacci sequence: f(5) = f(4)+f(3) = 5+3 = 8."
            }
        ],
        "constraints": [
            "1 <= n <= 45"
        ],
        "follow_up": "Can you implement this using O(1) space?",
        "learn": {
            "concept": "Recursive dynamic programming",
            "explanation": "Climbing Stairs follows the Fibonacci recurrence: the number of ways to reach step n is the sum of ways to reach the two previous steps. Use DP or memoization to avoid repeated work.",
            "analogy": "It is like counting how many paths you can take up a small staircase when you can move one or two steps at a time.",
            "key_properties": [
                "Uses the recurrence f(n) = f(n-1) + f(n-2)",
                "Has base cases for n = 1 and n = 2",
                "Avoids exponential recursion with memo or iteration",
                "Runs in linear time"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Dynamic programming basics", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Wikipedia dynamic programming overview", "url": "https://en.wikipedia.org/wiki/Dynamic_programming", "type": "article"}
            ]
        },
        "starter_code": """n = int(input())\n\ndef climb_stairs(n):\n    # Write your code here\n    return 0\n\nresult = climb_stairs(n)\nprint(result)\n"""
    },
    {
        "id": 10,
        "title": "Merge Two Sorted Lists",
        "description": """Merge two sorted linked lists and return it as a new sorted list.""",
        "difficulty": "easy",
        "topic": "two pointers",
        "expected_time": 15,
        "test_cases": [
            {"input": "3\n1 2 4\n3\n1 3 4", "expected_output": "[1, 1, 2, 3, 4, 4]"},
            {"input": "2\n1 3\n2\n2 4", "expected_output": "[1, 2, 3, 4]"},
            {"input": "1\n1\n1\n2", "expected_output": "[1, 2]"},
        ],
        "hints": {
            "level_1": "What approach lets you merge two sorted lists efficiently?",
            "level_2": "Use two pointers to compare the heads of both lists.",
            "level_3": "Iterate through both lists, always taking the smaller node next."
        },
        "examples": [
            {
                "input": "l1 = [1,2,4], l2 = [1,3,4]",
                "output": "[1,1,2,3,4,4]",
                "explanation": "Interleave both lists in sorted order."
            },
            {
                "input": "l1 = [1,3], l2 = [2,4]",
                "output": "[1,2,3,4]",
                "explanation": "Elements alternate between lists."
            },
            {
                "input": "l1 = [1], l2 = [2]",
                "output": "[1,2]",
                "explanation": "Single elements merge trivially."
            }
        ],
        "constraints": [
            "0 <= l1.length, l2.length <= 50",
            "-100 <= node.val <= 100"
        ],
        "follow_up": "Can you do this in-place with O(1) extra space?",
        "learn": {
            "concept": "Merging sorted lists",
            "explanation": "To merge two sorted linked lists, walk both lists with two pointers and attach the smaller current node to the merged list. This preserves sorted order using linear time.",
            "analogy": "It is like merging two sorted decks of cards by always taking the lower card from the top of each deck.",
            "key_properties": [
                "Compares the current node from both lists",
                "Advances the pointer on the chosen list",
                "Attaches the remaining tail when one list is done",
                "Runs in O(n + m) time"
            ],
            "resources": [
                {"title": "NeetCode YouTube — Merge sorted list problems", "url": "https://www.youtube.com/@NeetCode", "type": "video"},
                {"title": "Python heapq.merge documentation", "url": "https://docs.python.org/3/library/heapq.html#heapq.merge", "type": "article"}
            ]
        },
        "starter_code": """n1 = int(input())\nl1 = list(map(int, input().split()))\nn2 = int(input())\nl2 = list(map(int, input().split()))\n\ndef merge_two_lists(l1, l2):\n    # Write your code here\n    return []\n\nresult = merge_two_lists(l1, l2)\nprint(result)\n"""
    }
]