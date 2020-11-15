#!/usr/bin/env python3
import requests
import os
import time


def test_winnie_pooh_tutorial():
    qna_api = crud_api = "https://api.autofaq.ai"
    service_setup_api = crud_api + "/v1/setup"
    qna_api = qna_api + "/v1"
    user_token = os.environ.get("USER_TOKEN", "secret")

    print("=" * 80)
    print("crud_api {}".format(crud_api))
    print("qna_api {}".format(qna_api))
    print("CRUD API user_token {}".format(user_token))
    print("=" * 80)

    # создаем базу через CRUD API с авторизацией по user_token
    service_json = {
        "name": "ЧаВо",
        "documents": [
            {
                "question": "А не пойти ли нам в гости, немного подкрепиться?",
                "answer": "Кто ходит в гости по утрам, тот поступает мудро!",
            },
            {
                "question": "А зачем на свете пчёлы?",
                "answer": "Для того, чтобы делать мёд. По-моему, так.",
            },
        ],
    }
    url = service_setup_api + "/services"
    print(url)
    response = requests.post(
        url, json=service_json, headers={"AUTOFAQ-User-Token": user_token}
    )
    print(response.text)

    # В ответ получаем id сервиса и его токен для доступа к QnA API
    service_id = response.json()["service_id"]
    service_token = response.json()["tokens"][0]

    # Публикуем сервис в онлайн
    url = service_setup_api + "/services/{}/actions/publish".format(service_id)
    print(url)
    response = requests.post(url, json={}, headers={"AUTOFAQ-User-Token": user_token})
    print(response.text)

    # Ждем старта сервиса
    status = None
    while status != "Serving":
        time.sleep(5)
        url = service_setup_api + "/services/{}/status".format(service_id)
        print(url)
        response = requests.get(url, headers={"AUTOFAQ-User-Token": user_token})
        status = response.json()["status"]
        print("status {} ..".format(status))

    #
    # QnA Use case #1
    # формулируем известный базе вопрос в новой форме другой
    # обращаемся в QnA API с авторизацией по service_token
    #
    query2 = "Пойдем в гости?"
    url = qna_api + "/query"
    print(url)
    response = requests.post(
        url,
        json={
            "query": query2,
            "service_id": service_id,
            "service_token": service_token,
        },
    )
    print(response.text)
    # утверждаем ожидаемый результат
    assert (
        response.json()["results"][0]["answer"]
        == service_json["documents"][0]["answer"]
    )

    # опционально (для дообучения) подкрепляем корректность top1 ответа
    top1_document_id = response.json()["results"][0]["document_id"]
    query_id = response.json()["query_id"]
    session_id = response.json()["session_id"]
    feedback_click_params = dict(
        service_token=service_token,
        query=query2,
        query_id=query_id,
        service_id=service_id,
        document_id=top1_document_id,
        session_id=session_id,
    )
    url = qna_api + "/click"
    print(url)
    response = requests.post(url, json=feedback_click_params)
    print(response.text)
    response = response.json()
    assert response["message"] == "OK" and "error" not in response

    #
    # QnA Use case #2
    # задаем новый (неизвестный базе) вопрос и рекомендуем ответ
    # обращаемся в QnA API с авторизацией по service_token
    #
    query2 = "который час?"
    answer2 = "время обедать"
    url = qna_api + "/query"
    print(url)
    response = requests.post(
        url,
        json={
            "query": query2,
            "service_id": service_id,
            "service_token": service_token,
        },
    )
    print(response.text)
    # ожидаем ответ низкой уверенности
    assert response.json()["results"][0]["score"] < 0.5

    # (для дообучения) рекомендуем "правильный ответ"
    query_id = response.json()["query_id"]
    session_id = response.json()["session_id"]
    feedback_click_params = dict(
        service_token=service_token,
        query=query2,
        query_id=query_id,
        service_id=service_id,
        document_id=-1,  # в базе не ответа на такой вопрос
        suggested_answer=answer2,
        session_id=session_id,
    )
    url = qna_api + "/click"
    print(url)
    response = requests.post(url, json=feedback_click_params)
    print(response.text)
    response = response.json()
    assert response["message"] == "OK" and "error" not in response

    # останавливаем сервис
    url = service_setup_api + "/services/{}/actions/stop".format(service_id)
    print(url)
    response = requests.post(url, json={}, headers={"AUTOFAQ-User-Token": user_token})
    print(response.text)
    assert "message" in response.json()

    # удаляем сервис
    url = service_setup_api + "/services/{}".format(service_id)
    print(url)
    response = requests.delete(url, headers={"AUTOFAQ-User-Token": user_token})
    print(response.text)
    assert "message" in response.json()


if __name__ == "__main__":
    test_winnie_pooh_tutorial()
