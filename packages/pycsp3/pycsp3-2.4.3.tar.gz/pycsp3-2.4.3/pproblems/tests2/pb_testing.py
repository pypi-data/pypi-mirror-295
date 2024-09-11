from pycsp3.problems.tests3.tester import Tester, run

NAME = "pb_testing"

xcsp = (Tester(NAME)
        # .add("UnitTestingIntension")
        .add("TestAbscon")
        .add("TestChoco")
        .add("TestElement")
        .add("TestSlices")
        .add("TestSumConditions")
        .add("TestSums")
        .add("TestUnaryConditions")
        .add("UnitTestingExtension")
        .add("UnitTestingSum")
        .add("UnitTestingVariable")
        )

run(xcsp)
