import walk_test1
import walk_test2
import run_test1
import run_test2
import run_test3
import dodge_test1
import dodge_test2
import dodge_test3
import dodge_test4

passed = 0
failed = 0

print("\nTesting...\n")

w1 = walk_test1.walk_test1()
passed += w1[0]
failed += w1[1]

w2 = walk_test2.walk_test2()
passed += w2[0]
failed += w2[1]

r1 = run_test1.run_test1()
passed += r1[0]
failed += r1[1]

r2 = run_test2.run_test2()
passed += r2[0]
failed += r2[1]

r3 = run_test3.run_test3()
passed += r3[0]
failed += r3[1]

d1 = dodge_test1.dodge_test1()
passed += d1[0]
failed += d1[1]

d2 = dodge_test2.dodge_test2()
passed += d2[0]
failed += d2[1]

d3 = dodge_test3.dodge_test3()
passed += d3[0]
failed += d3[1]

d4 = dodge_test4.dodge_test4()
passed += d4[0]
failed += d4[1]

print(f"\n\nRESULTS:\n{passed} tests PASSED.\n{failed} tests FAILED.")