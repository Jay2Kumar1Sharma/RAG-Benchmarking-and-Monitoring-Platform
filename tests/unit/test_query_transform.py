from app.rag.query_transform import QueryTransformer


def test_query_transformer_normalizes_and_expands_queries() -> None:
    transformer = QueryTransformer()

    assert transformer.rewrite("  refund    policy  ") == "refund policy"
    assert len(transformer.multi_query("refund policy")) == 3
    assert transformer.decompose("refund policy and escalation process") == [
        "refund policy",
        "escalation process",
    ]

