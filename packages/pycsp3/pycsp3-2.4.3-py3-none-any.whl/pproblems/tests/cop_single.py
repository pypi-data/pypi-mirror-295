import os

from ppycsp3.pproblems.tests.tester import Tester, run

run(Tester("cop", "single")
    .add("DakotaFurniture")  # optimum 280
    .add("Photo")  # optimum 2
    .add("Photo", variant="aux")  # optimum 2
    .add("Recipe")  # optimum 1700
    .add("Witch")  # optimum 1300
    )
