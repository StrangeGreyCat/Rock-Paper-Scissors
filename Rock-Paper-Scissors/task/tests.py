from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class RPSTest(StageTest):
    def generate(self) -> List[TestCase]:
        self.options = ["rock", "paper", "scissors"]
        return [TestCase(stdin=case, attach=case) for case in self.options]

    def check(self, reply: str, attach) -> CheckResult:
        try:
            if "Sorry" in reply:
                result = -1
                option = reply.split()[-1]
            elif "draw" in reply:
                result = 0
                if '(' not in reply or ')' not in reply:
                    return CheckResult.wrong(
                        "There are no '(' or ')' character when there is a draw"
                    )
                start = reply.index('(')
                end = reply.index(')')
                option = reply[start + 1: end]
            elif "Well" in reply:
                result = 1
                option = reply.split()[-3]
            else:
                raise IndexError
            res = self.solve(result, [attach.strip(), option.strip()])
            if res < 0:
                raise IndexError
        except IndexError:
            return CheckResult.wrong("Seems like your answer (\"{}\") does not fit in given templates".format(reply))
        return CheckResult(res, "Your answer on \"{}\" was \"{}\". That's pretty wrong".format(attach, option))

    def solve(self, result, options):
        if any(opt not in self.options for opt in options):
            return -1
        diff = self.options.index(options[0]) - self.options.index(options[1])
        if not diff:
            true_result = 0
        else:
            true_result = (-1) ** ((abs(diff) - (len(self.options) // 2) > 0) == (diff > 0))
        return true_result == result


RPSTest("rps.game").run_tests()
