from mykatlas.analysis import AnalysisResult
from nose.tools import assert_raises


class TestAnalysis():

    def setUp(self):
        pass

    def test_simple_analysis(self):
        assert_raises(NotImplementedError, AnalysisResult.create)
