from .abstract_evaluator import AbstractEvaluator


class MeteorEvaluator(AbstractEvaluator):
    r"""Bleu Evaluator. Now, we support metrics `'bleu'`
    """

    def __init__(self, config):
        super(MeteorEvaluator, self).__init__(config)
        self.meteor_type = config['meteor_type']

    def _calc_metrics_info(self, generate_corpus, reference_corpus):
        r"""get metrics result

        Args:
            generate_corpus: the generated corpus
            reference_corpus: the referenced corpus

        Returns:
            dict: a dict of metrics <metric> which record the results according to self.ngrams
        """
        results = {}
        if self.meteor_type == 'pycocoevalcap':
            from pycocoevalcap.meteor.meteor import Meteor
            
            refs = {idx: r for idx, r in enumerate(reference_corpus)}
            gen = {idx: [g] for idx, g in enumerate(generate_corpus)}
            score = Meteor().compute_score(refs, gen)[0]
            results['METEOR'] = score * 100
        else:
            from nltk.translate.meteor_score import meteor_score

            results['METEOR'] = []
            for gen, refs in zip(generate_corpus, reference_corpus):
                score = meteor_score(refs, gen)
                results['METEOR'].append(score * 100)
        return results
