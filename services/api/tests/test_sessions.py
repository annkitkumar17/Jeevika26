import pytest
from app.models import Beneficiary

def test_start_voice_session(client, beneficiary_token, db_session):
    ben = db_session.query(Beneficiary).first()

    response = client.post(
        "/api/v1/sessions",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={
            "beneficiary_id": ben.id,
            "channel": "web_voice",
            "language": "hi"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["current_question_index"] == 0
    assert len(data["messages"]) >= 1
    assert "id" in data

def test_upload_session_transcript_and_complete(client, beneficiary_token, db_session):
    ben = db_session.query(Beneficiary).first()

    # 1. Start session
    session_res = client.post(
        "/api/v1/sessions",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={"beneficiary_id": ben.id, "channel": "web_voice", "language": "hi"}
    )
    session_id = session_res.json()["id"]

    # 2. Upload question 1 transcript
    trans_res = client.post(
        f"/api/v1/sessions/{session_id}/transcript",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={
            "question_key": "currentWork",
            "transcript_text": "मैं सोलर और कृषि पंप की मरम्मत का काम करता हूँ।",
            "audio_duration_seconds": 4.5,
            "is_confirmed": True
        }
    )
    assert trans_res.status_code == 200
    session_data = trans_res.json()
    assert session_data["answers"]["currentWork"] == "मैं सोलर और कृषि पंप की मरम्मत का काम करता हूँ।"
    assert session_data["current_question_index"] == 1

    # 3. Get session details
    get_res = client.get(
        f"/api/v1/sessions/{session_id}",
        headers={"Authorization": f"Bearer {beneficiary_token}"}
    )
    assert get_res.status_code == 200
    assert get_res.json()["id"] == session_id

    # 4. Complete session
    comp_res = client.put(
        f"/api/v1/sessions/{session_id}/complete",
        headers={"Authorization": f"Bearer {beneficiary_token}"},
        json={"extract_profile": True}
    )
    assert comp_res.status_code == 200
    assert comp_res.json()["status"] == "completed"
    assert comp_res.json()["completed_at"] is not None
