from mis_ai.commentary.knowledge import retrieve_knowledge_query


def test_query_retrieval_is_ranked_and_transparent():
    hits = retrieve_knowledge_query("why did gross margin decline", metric="gross_margin")

    assert hits
    assert hits[0]["id"] == "finance.gross_margin"
    assert hits[0]["relevance_score"] >= 2
