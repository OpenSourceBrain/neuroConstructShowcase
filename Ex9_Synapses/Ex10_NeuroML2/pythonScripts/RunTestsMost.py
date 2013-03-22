import RunTestsHH

report = RunTestsHH.testAll()
if not " 0 tests failed" in report: exit()

import RunTestsNML2ionChan

report = RunTestsNML2ionChan.testAll()
if not " 0 tests failed" in report: exit()

import RunTestsAbst

report = RunTestsAbst.testAll()
if not " 0 tests failed" in report: exit()


#import RunTestsDest

#report = RunTestsDest.testAll()
#if not " 0 tests failed" in report: exit()
