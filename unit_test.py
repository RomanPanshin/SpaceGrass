import math
from alive_progress import alive_bar
from SpaceGrass import DayForGrow
from SpaceGrass import Cvt_T2Fuel

def test_DayForGrow():
    print("Testing DayForGrow...")
    # Test cases with expected results
    test_cases = [
        (1, 1),
        (8, 1),
        (9, math.log2((9+8)/8)),
        (16, math.log2((16+8)/8)),
        (100, math.log2((100+8)/8))
    ]
    
    # Perform tests and print results
    with alive_bar(len(test_cases)) as bar:
        for i, (input_val, expected_output) in enumerate(test_cases):
            result = DayForGrow(input_val)
            bar()
            if math.isclose(result, expected_output):
                print(f"PASS: Test {i+1}")
            else:
                print(f"FAIL: Test {i+1}: expected {expected_output}, but got {result}")

def test_Cvt_T2Fuel():
    print("Testing Cvt_T2Fuel...")
    test_cases = [(0, 0), (1, 1), (5, 2), (10, 6)]
    with alive_bar(len(test_cases)) as bar:
        for T, expected in test_cases:
            result = Cvt_T2Fuel(T)
            bar()
            if result == expected:
                print(f"PASS: T={T} -> Fuel={result}")
            else:
                print(f"FAIL: T={T} -> Expected Fuel={expected}, but got {result}")



test_DayForGrow()
test_Cvt_T2Fuel()
