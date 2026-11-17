"""Additional educational tests for the unchanged CPython 3.13.5 textwrap.py."""
import pytest
from source import textwrap as tw


@pytest.mark.parametrize('text,width,expected', [
    ('one two three four', 7, ['one two', 'three', 'four']),
    ('Hello', 12, ['Hello']),
    ('', 10, []),
    ('abc def', 3, ['abc', 'def']),
    ('abcdefgh', 3, ['abc', 'def', 'gh']),
])
def test_wrap_basic(text, width, expected):
    assert tw.wrap(text, width=width) == expected


def test_fill_joins_with_newlines():
    assert tw.fill('one two three four', width=7) == 'one two\nthree\nfour'


def test_wrap_trims_whitespace():
    assert tw.wrap('  one   two  ', width=7) == ['  one', 'two']


def test_wrap_preserves_word_if_long_breaks_disabled():
    assert tw.wrap('extraordinary', width=5, break_long_words=False) == ['extraordinary']


def test_wrap_breaks_long_word_by_default():
    assert tw.wrap('extraordinary', width=5) == ['extra', 'ordin', 'ary']


def test_hyphen_is_break_location():
    assert tw.wrap('alpha-beta', width=6) == ['alpha-', 'beta']


def test_disable_hyphen_breaks():
    assert tw.wrap('alpha-beta', width=6, break_on_hyphens=False) == ['alpha-', 'beta']


def test_tabs_expanded_before_wrapping():
    assert tw.fill('A\tB', width=12) == 'A       B'


def test_fix_sentence_endings():
    assert tw.fill('One. Two!', width=30, fix_sentence_endings=True) == 'One.  Two!'


def test_indents_first_and_later_lines():
    result = tw.fill('one two three four', width=10,
                     initial_indent='> ', subsequent_indent='  ')
    assert result == '> one two\n  three\n  four'


def test_zero_width_raises_value_error():
    with pytest.raises(ValueError, match='invalid width'):
        tw.wrap('abc', width=0)


def test_negative_width_raises_value_error():
    with pytest.raises(ValueError, match='invalid width'):
        tw.wrap('abc', width=-5)


def test_large_placeholder_is_rejected():
    with pytest.raises(ValueError, match='placeholder too large'):
        tw.shorten('one two', width=2, placeholder='[...]')


def test_shorten_retains_fit_text():
    assert tw.shorten('  hello    world  ', width=20) == 'hello world'


def test_shorten_truncates_long_text():
    assert tw.shorten('hello world again', width=11) == 'hello [...]'


def test_shorten_with_custom_placeholder():
    assert tw.shorten('hello world again', width=9, placeholder='...') == 'hello...'


def test_max_lines_truncates_and_adds_placeholder():
    result = tw.fill('one two three four five six', width=10, max_lines=2)
    assert result == 'one two\n[...]'


def test_max_lines_allows_text_that_fits():
    assert tw.fill('hello', width=10, max_lines=1) == 'hello'


def test_dedent_removes_common_indent():
    assert tw.dedent('    first\n    second\n') == 'first\nsecond\n'


def test_dedent_preserves_relative_indent():
    assert tw.dedent('  first\n    second\n') == 'first\n  second\n'


def test_dedent_normalizes_blank_line():
    assert tw.dedent('  first\n    \n  second') == 'first\n\nsecond'


def test_dedent_rejects_non_string():
    with pytest.raises(TypeError, match='expected string or bytes-like object'):
        tw.dedent(None)


def test_indent_nonempty_lines_only_by_default():
    assert tw.indent('one\n\ntwo\n', '> ') == '> one\n\n> two\n'


def test_indent_custom_predicate_indents_every_line():
    assert tw.indent('one\n\ntwo\n', '> ', lambda _: True) == '> one\n> \n> two\n'


def test_indent_custom_predicate_skips_lines():
    assert tw.indent('apple\nbanana\n', '+', lambda line: line.startswith('a')) == '+apple\nbanana\n'


def test_indent_empty_text():
    assert tw.indent('', '> ') == ''


def test_wrapper_class_object_usage():
    wrapper = tw.TextWrapper(width=5)
    assert wrapper.wrap('one two three') == ['one', 'two', 'three']
    assert wrapper.fill('one two three') == 'one\ntwo\nthree'


def test_preserve_whitespace_at_line_start_when_disabled():
    result = tw.wrap('  alpha  beta', width=7, drop_whitespace=False)
    assert isinstance(result, list)
    assert ''.join(result).replace(' ', '') == 'alphabeta'


def test_max_lines_of_one_ellipsis_only():
    assert tw.shorten('far too long', width=5, placeholder='...') == '...'


def test_break_long_word_with_indentation():
    assert tw.fill('abcdef', width=4, initial_indent='> ') == '> ab\ncdef'
