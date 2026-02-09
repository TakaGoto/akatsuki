"""Tests for pipeline creation and structure."""

from my_ai_team.agents.pipeline import Pipeline, Stage, _build_message
from my_ai_team.agents.teams import dev_pipeline, full_pipeline
from my_ai_team.agents.presets import kisame, itachi, hidan
from my_ai_team.cli import build_custom_pipeline


def test_dev_pipeline_structure():
    pipeline = dev_pipeline()
    assert len(pipeline.stages) == 3

    # Stage 1: Kisame alone
    assert len(pipeline.stages[0].agents) == 1
    assert pipeline.stages[0].agents[0].name == "Kisame"
    assert pipeline.stages[0].fix is False

    # Stage 2: Sasori + Itachi + Hidan in parallel
    assert len(pipeline.stages[1].agents) == 3
    names = {a.name for a in pipeline.stages[1].agents}
    assert names == {"Sasori", "Itachi", "Hidan"}
    assert pipeline.stages[1].fix is False

    # Stage 3: Kisame fix stage
    assert len(pipeline.stages[2].agents) == 1
    assert pipeline.stages[2].agents[0].name == "Kisame"
    assert pipeline.stages[2].fix is True


def test_full_pipeline_structure():
    pipeline = full_pipeline()
    assert len(pipeline.stages) == 4

    # Stage 1: Kisame
    assert len(pipeline.stages[0].agents) == 1
    assert pipeline.stages[0].agents[0].name == "Kisame"
    assert pipeline.stages[0].fix is False

    # Stage 2: 4 agents in parallel
    assert len(pipeline.stages[1].agents) == 4
    names = {a.name for a in pipeline.stages[1].agents}
    assert names == {"Sasori", "Itachi", "Hidan", "Deidara"}
    assert pipeline.stages[1].fix is False

    # Stage 3: Kisame fix stage
    assert len(pipeline.stages[2].agents) == 1
    assert pipeline.stages[2].agents[0].name == "Kisame"
    assert pipeline.stages[2].fix is True

    # Stage 4: Konan docs
    assert len(pipeline.stages[3].agents) == 1
    assert pipeline.stages[3].agents[0].name == "Konan"


def test_dev_pipeline_with_context():
    pipeline = dev_pipeline(extra_instructions="Stack: Next.js")
    assert "Next.js" in pipeline.context


def test_custom_pipeline_single_agent():
    config = {"context": "", "agents": {}}
    pipeline = build_custom_pipeline(["kisame"], config)
    assert len(pipeline.stages) == 1
    assert len(pipeline.stages[0].agents) == 1


def test_custom_pipeline_multi_agent():
    config = {"context": "", "agents": {}}
    pipeline = build_custom_pipeline(["kisame", "itachi", "hidan"], config)
    assert len(pipeline.stages) == 3

    # First agent solo
    assert pipeline.stages[0].agents[0].name == "Kisame"
    assert pipeline.stages[0].fix is False

    # Rest in parallel
    assert len(pipeline.stages[1].agents) == 2
    names = {a.name for a in pipeline.stages[1].agents}
    assert names == {"Itachi", "Hidan"}
    assert pipeline.stages[1].fix is False

    # Fix stage — first agent again
    assert len(pipeline.stages[2].agents) == 1
    assert pipeline.stages[2].agents[0].name == "Kisame"
    assert pipeline.stages[2].fix is True


def test_pipeline_dataclass():
    p = Pipeline(
        context="test",
        stages=[
            Stage(agents=[kisame()]),
            Stage(agents=[itachi(), hidan()]),
        ],
    )
    assert p.context == "test"
    assert len(p.stages) == 2
    assert len(p.stages[1].agents) == 2


def test_stage_fix_default():
    stage = Stage(agents=[kisame()])
    assert stage.fix is False


def test_stage_fix_true():
    stage = Stage(agents=[kisame()], fix=True)
    assert stage.fix is True


def test_build_message_normal():
    msg = _build_message(
        context="Stack: Python",
        task="Add login",
        previous_outputs=[("Kisame", "Done implementing")],
        is_fix=False,
    )
    assert "Stack: Python" in msg
    assert "Add login" in msg
    assert "Kisame" in msg
    assert "Your mission" not in msg


def test_build_message_fix():
    msg = _build_message(
        context="",
        task="Add login",
        previous_outputs=[("Itachi", "Found 2 issues"), ("Hidan", "SQL injection risk")],
        is_fix=True,
    )
    assert "Your mission" in msg
    assert "EVERY issue" in msg
    assert "Itachi" in msg
    assert "Hidan" in msg
