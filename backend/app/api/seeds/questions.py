pythonquestions = [
    {
        "title": "Two Sum",
        "description": """Given an array of integers nums and an integer target, \nreturn indices of the two numbers that add up to target.\nYou may assume each input has exactly one solution.\nExample: nums = [2,7,11,15], target = 9 → [0,1]""",
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
        }
    },
    {
        "title": "Valid Anagram",
        "description": """Given two strings s and t, return true if t is an anagram of s, and false otherwise.\nExample: s = 'anagram', t = 'nagaram' → true\nExample: s = 'rat', t = 'car' → false""",
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
        }
    },
    {
        "title": "Best Time to Buy Stock",
        "description": """You are given an array prices where prices[i] is the price of a stock on the ith day.\nFind the maximum profit you can achieve from one transaction.\nExample: prices = [7,1,5,3,6,4] → 5""",
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
        }
    },
    {
        "title": "Contains Duplicate",
        "description": """Given an integer array nums, return true if any value appears at least twice.\nExample: nums = [1,2,3,1] → true\nExample: nums = [1,2,3,4] → false""",
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
        }
    },
    {
        "title": "Maximum Subarray",
        "description": """Given an integer array nums, find the contiguous subarray with the largest sum.\nExample: nums = [-2,1,-3,4,-1,2,1,-5,4] → 6""",
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
        }
    },
    {
        "title": "Valid Parentheses",
        "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\nExample: s = '()[]{}' → true\nExample: s = '(]' → false""",
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
        }
    },
    {
        "title": "Reverse Linked List",
        "description": """Given the head of a singly linked list, reverse the list and return the reversed list.\nExample: head = [1,2,3,4,5] → [5,4,3,2,1]""",
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
        }
    },
    {
        "title": "Binary Search",
        "description": """Given a sorted array of integers nums and a target value, return the index if the target is found. If not, return -1.\nExample: nums = [-1,0,3,5,9,12], target = 9 → 4""",
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
        }
    },
    {
        "title": "Climbing Stairs",
        "description": """You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. In how many distinct ways can you climb to the top?\nExample: n = 2 → 2\nExample: n = 3 → 3""",
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
        }
    },
    {
        "title": "Merge Two Sorted Lists",
        "description": """Merge two sorted linked lists and return it as a new sorted list.\nExample: l1 = [1,2,4], l2 = [1,3,4] → [1,1,2,3,4,4]""",
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
        }
    }
]

# Example usage: insert these into your questions table using your ORM or raw SQL.
