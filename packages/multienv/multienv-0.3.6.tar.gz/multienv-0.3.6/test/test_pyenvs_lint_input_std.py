"""Test module for pyenv lint input."""

import pytest

from multienv._pyenvs_lint_input_std import Rule, Section, Configuration

def test_lint_configuration_from_dict_classic():
    """Test configuration loading from dict."""

    i = {
        'configuration': {
            'formatters': 'pylint',
        },
        'environments': ['multienv', 'test'],
        'sections':[
            {
            'name': 'FORMAT',
            'rules':[
                {
                'key': 'max-line-length',
                'value': '120',
                'environments': ['multienv', 'test']
                }
            ]
            }
        ]
    }

    c = Configuration.from_dict(i)

    assert c.environments == ['multienv', 'test']

    sections = c.sections

    assert len(sections) == 1

    s = sections[0]

    assert s.name == 'FORMAT'

    rules = s.rules

    assert len(rules) == 1

    r = rules[0]

    assert r.key == 'max-line-length'
    assert r.value == '120'
    assert r.environments == ['multienv', 'test']


def test_lint_configuration_strict_rules():
    """Test configuration strict rules."""

    i = {
        'configuration': {
            'formatters': 'pylint',
        },
        'environments': ['multienv', 'test'],
        'sections':[
            {
            'name': 'FORMAT',
            'rules':[
                {
                'key': 'max-line-length',
                'value': '120',
                'environments': ['multienv', 'test']
                }
            ]
            }
        ]
    }

    c = Configuration.from_dict(i)

    r = c.strict_rules()
    assert len(r) == 0


def test_lint_configuration_strict_rules_2():
    """Test configuration strict rules."""

    i = {
        'configuration': {
            'formatters': 'pylint',
        },
        'environments': ['multienv', 'test'],
        'sections':[
            {
            'name': 'FORMAT',
            'rules':[
                {
                'key': 'max-line-length',
                'value': '120',
                'environments': ['multienv', 'test']
                }
            ]
            },
            {
            'name': 'DESIGN',
            'rules':[
                {
                'key': 'min-public-methods',
                'value': '1'
                }
            ]
            }
        ]
    }

    c = Configuration.from_dict(i)

    r = c.strict_rules()
    assert len(r) == 1


def test_lint_configuration_env_rules():
    """Test configuration strict rules."""

    i = {
        'configuration': {
            'formatters': 'pylint',
        },
        'environments': ['multienv', 'test'],
        'sections':[
            {
            'name': 'FORMAT',
            'rules':[
                {
                'key': 'max-line-length',
                'value': '120',
                'environments': ['multienv', 'test']
                }
            ]
            },
            {
            'name': 'DESIGN',
            'rules':[
                {
                'key': 'min-public-methods',
                'value': '1',
                'environments': ['test']
                }
            ]
            }
        ]
    }

    c = Configuration.from_dict(i)

    r = c.env_rules('test')
    assert len(r) == 2


def test_lint_configuration_env_rules_2():
    """Test configuration strict rules."""

    i = {
        'configuration': {
            'formatters': 'pylint',
        },
        'environments': ['multienv', 'test'],
        'sections':[
            {
            'name': 'FORMAT',
            'rules':[
                {
                'key': 'max-line-length',
                'value': '120',
                'environments': ['multienv', 'test']
                }
            ]
            },
            {
            'name': 'DESIGN',
            'rules':[
                {
                'key': 'min-public-methods',
                'value': '1',
                'environments': ['test']
                }
            ]
            }
        ]
    }

    c = Configuration.from_dict(i)

    r = c.env_rules('multienv')
    assert len(r) == 1

def test_lint_section_from_dict_classic():
    """Test section loading from dict."""

    i = {
        'name': 'FORMAT',
        'rules':[
            {
            'key': 'max-line-length',
            'value': '120',
            'environments': ['multienv', 'test']
            }
        ]
    }

    s = Section.from_dict(i)

    assert s.name == 'FORMAT'

    rules = s.rules

    assert len(rules) == 1

    r = rules[0]

    assert r.key == 'max-line-length'
    assert r.value == '120'
    assert r.environments == ['multienv', 'test']

def test_lint_rule_from_dict_classic():
    """Test rule loading from dict."""

    i = {
        'key': 'max-line-length',
        'value': '120',
        'environments': ['multienv', 'test']
    }

    r = Rule.from_dict(i)

    assert r.key == 'max-line-length'
    assert r.value == '120'
    assert r.environments == ['multienv', 'test']


def test_lint_rule_from_dict_without_environments():
    """Test rule loading from dict."""

    i = {
        'key': 'max-line-length',
        'value': '120'
    }

    r = Rule.from_dict(i)

    assert r.key == 'max-line-length'
    assert r.value == '120'
    assert r.environments is None


def test_lint_rule_from_dict_without_value():
    """Test rule loading from dict."""

    i = {
        'key': 'max-line-length',
        'environments': ['multienv', 'test']
    }

    with pytest.raises(AssertionError) as e:
        Rule.from_dict(i)

    assert e.value.args[0] == 'value is a mandatory section field'

def test_lint_rule_from_dict_without_key():
    """Test rule loading from dict."""

    i = {
        'value': '120',
        'environments': ['multienv', 'test']
    }

    with pytest.raises(AssertionError) as e:
        Rule.from_dict(i)

    assert e.value.args[0] == 'key is a mandatory section field'
