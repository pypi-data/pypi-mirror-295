from typing import Union

from integral_deid.spacy_sentencizer import SpacySentencizer
from integral_deid.clinical_spacy_tokenizer import ClinicalSpacyTokenizer


class PreprocessingLoader(object):
    @staticmethod
    def get_sentencizer(sentencizer: str) -> SpacySentencizer:
        """
        Get the desired the sentencizer
        We can either use the sci-spacy (en_core_sci_lg or en_core_web_sm) or
        consider the entire note as a single sentence.
        Args:
            sentencizer (str): Specify which sentencizer you want to use
        Returns:
            Union[SpacySentencizer, NoteSentencizer]: An object of the requested
                                                      sentencizer class
        """
        return SpacySentencizer(spacy_model=sentencizer)

    @staticmethod
    def get_tokenizer(tokenizer: str) -> ClinicalSpacyTokenizer:
        """
        Initialize the tokenizer based on the CLI arguments
        We can either use the default scipacy (en_core_sci_lg or en_core_web_sm)
        or the modified scipacy (with regex rule) tokenizer.
        It also supports the corenlp tokenizer
        Args:
            tokenizer (str): Specify which tokenizer you want to use
        Returns:
            Union[SpacyTokenizer, ClinicalSpacyTokenizer, CoreNLPTokenizer]: An object of the requested tokenizer class
        """

        return ClinicalSpacyTokenizer(tokenizer)
