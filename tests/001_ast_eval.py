import ast
import json
from pathlib import Path


def test_literal_eval_limit_memory(tests_settings):
    """
    literal_eval limitation is not really about string limit but more of memory
    allocation in AST parsing that will occurs with deep recursion in object to
    evaluate.

    Here We are just checking that some common complex object (list, dict) structure
    will work properly.
    """
    # A basic list with 200 strings of 11 characters
    sample_list = ["lorem ipsum" for i in range(200)]
    # Serialize list to string (3000 characters) for evaluation
    serialized = json.dumps(sample_list)
    # All expected items are there
    assert len(ast.literal_eval(serialized)) == 200

    # Try with a four levels dictionnary
    manifest_json = (
        Path(tests_settings.fixtures_path) / "json" / "sample_libsass.json"
    )
    manifest = json.loads(manifest_json.read_text())
    # Duplicate sample manifest three times
    sample_dict = {
        "first": manifest,
        "second": manifest,
        "third": manifest,
    }
    parsed = ast.literal_eval(json.dumps(sample_dict))
    assert len(parsed) == 3
