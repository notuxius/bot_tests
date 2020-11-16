import pytest


@pytest.mark.api
def test_service(bot_chat_api):

    # create service
    service_params = {
        "name": "test",
        "documents": [
            {"question": "what?", "answer": "42"},
        ],
    }
    response = bot_chat_api.http_post("/services", params=service_params)
    service_id = response["service_id"]
    service_token = response["tokens"][0]

    # get document_id
    documents = bot_chat_api.http_get(f"/services/{service_id}/documents")

    assert len(documents) == 1

    document_id = documents[0]["document_id"]

    # CREATE
    # add paraphrase to given document_id of created service
    paraphrase_params = {
        "service_id": service_id,
        "document_id": document_id,
        "paraphrase": "what is the meaning?",
    }
    response = bot_chat_api.http_post("/paraphrases", params=paraphrase_params)
    paraphrase_id = response["paraphrase_id"]

    # READ
    response = bot_chat_api.http_get(f"/paraphrases/{paraphrase_id}")

    assert response["paraphrase_id"] == paraphrase_id
    assert response["paraphrase"] == paraphrase_params["paraphrase"]

    # UPDATE
    response = bot_chat_api.http_put(
        f"/paraphrases/{paraphrase_id}", params={"paraphrase": "what`s the point"}
    )

    assert "updated" in response["message"]

    # DELETE
    response = bot_chat_api.http_delete(f"/paraphrases/{paraphrase_id}")

    # cleanup
    bot_chat_api.http_delete(f"/services/{service_id}")
