import unittest

from strategy_lab import wrap_dist, bounded_space, decision_features, extract, markdown

def snake(i,name,pts,alive=True):
    return {"id":i,"name":name,"alive":alive,
            "body":[{"x":x,"y":y} for x,y in pts]}

class StrategyLabTests(unittest.TestCase):
    def test_toroidal_distance(self):
        self.assertEqual(wrap_dist((0,0),(8,0),9,9),1)
        self.assertEqual(wrap_dist((0,0),(8,8),9,9),2)

    def test_bounded_space(self):
        self.assertEqual(bounded_space((1,1),{(1,1)},7,7,30),0)
        self.assertEqual(bounded_space((1,1),set(),7,7,30),30)

    def test_policy_extraction(self):
        a=snake(0,"a",[(4,4),(4,5)])
        later=snake(0,"a",[(4,3),(4,4)])
        b={"turn":0,"snakes":[a],"food":[{"x":4,"y":1}],"obstacles":[]}
        t={"turn":1,"snakes":[later],"food":[{"x":4,"y":1}],"obstacles":[]}
        d=decision_features(b,t,a,later,9,9)
        self.assertEqual(d["choice"],"UP")
        self.assertEqual(d["greedy"],1)
        self.assertEqual(d["greedy_applicable"],1)
        self.assertGreaterEqual(d["n_safe"],2)
        counts,cases=extract({"header":{"board":[9,9]},"frames":[b,t]})
        self.assertEqual(counts["a"]["greedy"],1)
        self.assertEqual(cases,[])

    def test_respawn_and_invalid_jumps_ignored(self):
        a=snake(0,"a",[(4,4),(4,5)],False)
        t=snake(0,"a",[(7,7),(7,8)],True)
        b={"turn":0,"snakes":[a],"food":[]}
        c={"turn":1,"snakes":[t],"food":[]}
        counts,_=extract({"header":{"board":[9,9]},"frames":[b,c]})
        self.assertEqual(dict(counts),{})

if __name__=="__main__":
    unittest.main()
