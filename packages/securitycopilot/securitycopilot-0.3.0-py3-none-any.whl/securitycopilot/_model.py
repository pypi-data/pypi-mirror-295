# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------

from collections import OrderedDict
from . import get_api, SecurityCopilotClientError


class Session:
    def __init__(self):
        self._id = None
        self._name = None
        self._created_raw = None
        self._updated_raw = None
        self._featureflags = []
        self._skillsets = []
        self._skillfilters = []
        self._tenant_id = None
        self._user_id = None
        self._prompts = OrderedDict()
        self._is_prompt_pending = False
        self._source = "api.python"

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source: str):
        self._source = source

    @property
    def created(self):
        return self._created_raw

    @property
    def updated(self):
        return self._updated_raw

    @property
    def tenant_id(self):
        return self._tenant_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def featureflags(self):
        return self._featureflags

    @featureflags.setter
    def featureflags(self, flags):
        self._featureflags = flags

    @property
    def skillsets(self) -> list:
        return self._skillsets

    @skillsets.setter
    def skillsets(self, sets: list):
        self._skillsets = sets

    @property
    def skillfilters(self) -> list:
        return self._skillfilters

    @skillfilters.setter
    def skillfilters(self, filters: list):
        self._skillfilters = filters

    @property
    def prompts(self):
        return self._prompts

    @property
    def is_prompt_pending(self) -> bool:
        return self._is_prompt_pending

    @property
    def most_recent_prompt(self) -> "Prompt":
        return list(self._prompts.values())[-1]

    @property
    def as_dict(self):
        return self.to_dictionary()

    def to_dictionary(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created": self.created,
            "updated": self.updated,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "featureflags": self._featureflags,
            "skillsets": self._skillsets,
            "skillfilters": self._skillfilters,
            "source": self._source,
            "prompts": [p.as_dict for p in list(self.prompts.values())],
        }

    def create(self, name: str = None, source: str = None):
        if self._id is not None:
            raise SecurityCopilotClientError("Cannot recreate an existing session")
        self._name = name or ""
        if source:
            self._source = source
        payload = {
            "name": self._name,
            "source": self._source,
            "featureflags": self._featureflags,
            "skillsets": self._skillsets,
            "skillFilters": self._skillfilters,
        }
        if self._tenant_id:
            payload["tenantId"] = self._tenant_id
        r = get_api()._POST("sessions", json=payload)
        r.raise_for_status()
        session = r.json()
        self._id = session["sessionId"]
        self._created_raw = session["createdAt"]
        self._updated_raw = session["updatedAt"]
        self._user_id = session["userId"]

    def submit_prompt(self, content: str, source: str = None) -> "Prompt":
        self._create_if_not_exists(content)
        self._ensure_prompt_not_pending()
        prompt = Prompt(self)
        prompt.submit_prompt(content, source)
        self._prompts[prompt.id] = prompt
        self._is_prompt_pending = True
        return prompt

    def run_skill(
        self, skillname, params: dict = None, content: str = None, source: str = None
    ) -> "Prompt":
        self._create_if_not_exists(skillname)
        self._ensure_prompt_not_pending()
        prompt = Prompt(self)
        prompt.run_skill(skillname, params, content, source)
        self._prompts[prompt.id] = prompt
        self._is_prompt_pending = True
        return prompt

    def refresh(self):
        if self._id is None:
            raise SecurityCopilotClientError(
                "Cannot refresh a session that has not been created"
            )
        prompt_updates = self.most_recent_prompt.refresh()
        if len(prompt_updates.values()) == 0:
            return
        eval_updates = self.most_recent_prompt.refresh_last_completed_evaluation()
        return (prompt_updates, eval_updates)

    def open_in_browser(self, dev=False):
        import webbrowser

        url = "https://{0}.microsoft.com/sessions/{1}".format(
            "medeina-dev.defender" if dev else "securitycopilot", self.id
        )
        webbrowser.open_new_tab(url)

    def _create_if_not_exists(self, title):
        if self._id is None:
            self.create(title)

    def _ensure_prompt_not_pending(self):
        if self._is_prompt_pending:
            raise SecurityCopilotClientError(
                "Cannot submit a new prompt while an existing prompt is pending completion"
            )


class Prompt:
    def __init__(self, session: Session, payload=None):
        self._session = session
        self._id = None
        self._type = "Prompt"
        self._source = "api.python"
        self._created_raw = None
        self._updated_raw = None
        self._content = None
        self._skillname = None
        self._inputs = None
        self._last_completed_eval_id = None
        self._latest_eval_id = None
        self._evaluations = OrderedDict()
        self._is_eval_pending = False
        if payload:
            self._parse_payload(payload)

    def _parse_payload(self, payload):
        self._id = payload.get("promptId", self._id)
        self._type = payload.get("promptType", self._type)
        self._created_raw = payload.get("createdAt", self._created_raw)
        self._updated_raw = payload.get("updatedAt", self._updated_raw)
        self._content = payload.get("content", self._content)
        self._skillname = payload.get("skillName", self._skillname)
        self._inputs = payload.get("inputs", self._inputs)
        self._source = payload.get("source", self._source)
        self._last_completed_eval_id = payload.get(
            "lastCompletedEvaluationId", self._last_completed_eval_id
        )
        self._latest_eval_id = payload.get("lastestEvaluationId", self._latest_eval_id)

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def created(self):
        return self._created_raw

    @property
    def updated(self):
        return self._updated_raw

    @property
    def content(self):
        return self._content

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source: str):
        self._source = source

    @property
    def skillname(self):
        return self._skillname

    @property
    def inputs(self):
        return self._inputs

    @property
    def last_completed_eval_id(self):
        return self._last_completed_eval_id

    @property
    def last_completed_eval(self) -> "Evaluation":
        return self._evaluations[self._last_completed_eval_id]

    @property
    def latest_eval_id(self):
        return self._latest_eval_id

    @property
    def is_eval_pending(self) -> bool:
        return self._is_eval_pending

    @property
    def session(self) -> Session:
        return self._session

    @property
    def evaluations(self) -> list["Evaluation"]:
        return self._evaluations

    @property
    def result(self):
        if self.is_eval_pending:
            raise SecurityCopilotClientError("Evaluation is still pending")
        return self.last_completed_eval.result

    @property
    def as_dict(self) -> dict:
        return self.to_dictionary()

    def to_dictionary(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "created": self.created,
            "session_id": self.session.id,
            "updated": self.updated,
            "content": self.content,
            "skillname": self.skillname,
            "source": self.source,
            "inputs": self.inputs,
            "last_completed_eval_id": self.last_completed_eval_id,
            "latest_eval_id": self.latest_eval_id,
        }

    def submit_prompt(self, content, source: str = None):
        self._ensure_is_unset()
        if source:
            self._source = source
        self._type = "Prompt"
        payload = {
            "content": content,
            "promptType": self._type,
            "sessionId": self.session.id,
            "source": self._source,
        }
        self._create(payload)

    def run_skill(
        self, skillname, params=None, content: str = None, source: str = None
    ):
        self._ensure_is_unset()
        if source:
            self._source = source
        self._type = "Skill"
        payload = {
            "skillName": skillname,
            "promptType": self._type,
            "sessionId": self.session.id,
            "source": self._source,
        }
        if params is not None:
            payload["inputs"] = params
        elif content is not None:
            payload["content"] = content
        else:
            payload["inputs"] = {}
        self._create(payload)

    def _ensure_is_unset(self):
        if self._id is not None:
            raise SecurityCopilotClientError("Cannot resend a prompt")

    def _create(self, payload):
        r = get_api()._POST(
            "sessions/{0.session.id}/prompts".format(self), json=payload
        )
        r.raise_for_status()
        prompt = r.json()
        self._parse_payload(prompt)
        self._session._is_prompt_pending = True

    def evaluate(self) -> "Evaluation":
        eval = Evaluation(self)
        eval.create()
        self._evaluations[eval.id] = eval
        return eval

    def refresh(self):
        if self._id is None:
            raise SecurityCopilotClientError(
                "Cannot refresh a prompt that has not been created"
            )
        baseline = self.as_dict
        r = get_api()._GET("sessions/{0.session.id}/prompts/{0.id}".format(self))
        r.raise_for_status()
        prompt = r.json()
        self._parse_payload(prompt)
        return {k: v for k, v in self.as_dict.items() if baseline[k] != v}

    def refresh_last_completed_evaluation(self):
        if self._id is None:
            raise SecurityCopilotClientError(
                "Cannot refresh an evaluation in a prompt that has not been created"
            )
        if self._last_completed_eval_id is None:
            raise SecurityCopilotClientError("No completed evaluation to refresh")
        return self.last_completed_eval.refresh()


class Evaluation:
    def __init__(self, prompt: Prompt, payload=None):
        self._prompt = prompt
        self._id = None
        self._completed_raw = None
        self._created_raw = None
        self._result = None
        self._state = None
        self._updated_raw = None
        if payload is not None:
            self._parse_payload(payload)

    def _parse_payload(self, payload):
        evaluation = payload.get(
            "evaluation", payload
        )  # because a POST returns 'evaluation' nested but a GET does not...
        self._id = evaluation.get("evaluationId", self._id)
        self._created_raw = evaluation.get("createdAt", self._created_raw)
        self._completed_raw = evaluation.get("completedRaw", self._completed_raw)
        self._updated_raw = evaluation.get("updatedRaw", self._updated_raw)
        self._state = evaluation.get("state", self._state)
        self._result = evaluation.get("result", self._result)

    @property
    def id(self):
        return self._id

    @property
    def result(self):
        return self._result

    @property
    def created(self):
        return self._created_raw

    @property
    def completed(self):
        return self._completed_raw

    @property
    def updated(self):
        return self._updated_raw

    @property
    def state(self):
        return self._state

    @property
    def prompt(self) -> Prompt:
        return self._prompt

    @property
    def content(self) -> str:
        if self._result is None:
            return ""
        return self._result.get("content", "")

    @property
    def as_dict(self) -> dict:
        return self.to_dictionary()

    def to_dictionary(self) -> dict:
        return {
            "id": self.id,
            "result": self.result,
            "created": self.created,
            "updated": self.updated,
            "completed": self.completed,
            "state": self.state,
            "prompt_id": self.prompt.id,
            "session_id": self.prompt.session.id,
        }

    def create(self):
        if self._id is not None:
            raise SecurityCopilotClientError("Cannot recreate an existing evaluation")
        payload = {
            "promptContent": self.prompt.content,
            "promptId": self.prompt.id,
            "sessionId": self.prompt.session.id,
        }
        r = get_api()._POST(
            "sessions/{0.prompt.session.id}/prompts/{0.prompt.id}/evaluations".format(
                self
            ),
            json=payload,
        )
        r.raise_for_status()
        eval = r.json()
        self._parse_payload(eval)
        self.prompt._is_eval_pending = True

    def refresh(self):
        if self._id is None:
            raise SecurityCopilotClientError(
                "Cannot refresh an evaluation that has not been created"
            )
        baseline = self.as_dict
        r = get_api()._GET(
            "sessions/{0.prompt.session.id}/prompts/{0.prompt.id}/evaluations/{0.id}".format(
                self
            )
        )
        r.raise_for_status()
        eval = r.json()
        self._parse_payload(eval)
        if self.state != "Running":
            self.prompt._is_eval_pending = False
            self.prompt.session._is_prompt_pending = False
        return {k: v for k, v in self.as_dict.items() if baseline[k] != v}


class SkillSet:
    def __init__(self, payload=None):
        self._name = None
        self._description = None
        self._enabled = False
        self._hidden = False
        self._prerequisites = None
        self._featureflags = []
        self._skills = SkillCollection(self)
        if payload:
            self._parse(payload)

    def _parse_payload(self, payload):
        self._name = payload["name"]
        self._enabled = payload["enabled"]
        self._hidden = payload["hidden"]
        self._prerequisites = payload["prerequisites"]
        self._featureflags = payload["featureFlags"]


class SkillCollection:
    def __init__(self, skillset, payload=None):
        self._skillset = skillset
        if payload:
            self._parse(payload)

    def _parse(self, payload):
        pass
