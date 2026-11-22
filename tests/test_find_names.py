"""Tests for doodad.find_names: names in code and in nested data."""

import ast

import pytest

from doodad.find_names import (
    dflt_value_normalizer,
    extract_names_from_code,
    find_names,
    parsed_ast,
    unique_kvs_from_mapping,
    yield_names_and_values_from_vk,
    yield_names_from_mapping,
    yield_names_from_vk,
)

CODE = """
x = 10
y, z = 5, 6
def func(a, b=10):
    local_var = 9
square = lambda p, q: p * q
"""


def test_extract_names_from_code():
    names = list(extract_names_from_code(CODE))
    assert sorted(names) == sorted(
        ["x", "y", "z", "func", "a", "b", "local_var", "square", "p", "q"]
    )
    assert names.index("x") < names.index("func")


def _sample(alpha, beta):
    return alpha + beta


def test_extract_names_accepts_an_object_with_source():
    names = list(extract_names_from_code(_sample))
    assert names[:3] == ["_sample", "alpha", "beta"]


def test_module_level_lambda_assignment_name_is_kept():
    assert "square" in list(extract_names_from_code(CODE))


def test_include_locals_false_excludes_function_locals():
    assert "local_var" not in list(extract_names_from_code(CODE, include_locals=False))


def test_parsed_ast_from_string_and_object():
    assert isinstance(parsed_ast("x = 1"), ast.Module)

    assert isinstance(parsed_ast(_sample), ast.Module)
    with pytest.raises(Exception):
        parsed_ast(object())


def test_find_names_dispatches_on_data_and_code():
    assert list(find_names({"c": 1, "b": {"a": 2}})) == ["c", "b", "a"]
    assert list(find_names("x = 1\ndef f(a): pass")) == ["x", "f", "a"]


def test_value_normalizer_cases():
    assert dflt_value_normalizer({"a": 1}) == {"a": 1}
    assert dflt_value_normalizer(3) == 3
    assert isinstance(dflt_value_normalizer("x = 1"), ast.AST)
    assert dflt_value_normalizer("not python )(") == "not python )("


def test_value_normalizer_dataframe():
    pd = pytest.importorskip("pandas")  # optional dependency
    assert dflt_value_normalizer(pd.DataFrame({"a": [1, 2]})) == {"a": 1}


def test_names_from_mapping_and_dicts():
    assert list(yield_names_from_vk({"c": 1, "b": {"a": 2}})) == ["c", "b", "a"]
    assert sorted(set(yield_names_from_mapping({"c": 1, "b": {"a": 2, "d": 3}}))) == ["a", "d"]
    assert list(yield_names_from_vk(5)) == []


def test_names_and_values():
    assert list(yield_names_and_values_from_vk({"c": 1, "b": {"a": 2, "d": 3}})) == [
        ("c", 1), ("a", 2), ("d", 3),
    ]
    assert list(yield_names_and_values_from_vk(5)) == []


def test_unique_kvs_keeps_first_example_value():
    out = unique_kvs_from_mapping({"r1": {"a": 1, "b": 2}, "r2": {"a": 9, "c": 3}})
    assert out == {"a": 1, "b": 2, "c": 3}


def test_names_from_a_list_of_dicts_are_flattened():
    assert list(yield_names_from_vk([{"a": 1}, {"b": 2}])) == ["a", "b"]
    assert list(yield_names_and_values_from_vk([{"a": 1}, {"b": 2}])) == [("a", 1), ("b", 2)]
