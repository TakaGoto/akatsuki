"""Tests for pipeline creation and structure."""

from my_ai_team.agents.pipeline import Pipeline, Stage
from my_ai_team.agents.teams import dev_pipeline, full_pipeline
from my_ai_team.agents.presets import kisame, itachi, hidan
from my_ai_team.cli import build_custom_pipeline


def test_dev_pipeline_structure():
    pipeline = dev_pipeline()
    assert len(pipeline.stages) == 2

    # Stage 1: Kisame alone
    assert len(pipeline.stages[0].agents) == 1
    assert pipeline.stages[0].agents[0].name == "Kisame"

    # Stage 2: Sasori + Itachi + Hidan in parallel
    assert len(pipeline.stages[1].agents) == 3
    names = {a.name for a in pipeline.stages[1].agents}
    assert names == {"Sasori", "Itachi", "Hidan"}


def test_full_pipeline_structure():
    pipeline = full_pipeline()
    assert len(pipeline.stages) == 3

    # Stage 1: Kisame
    assert len(pipeline.stages[0].agents) == 1
    assert pipeline.stages[0].agents[0].name == "Kisame"

    # Stage 2: 4 agents in parallel
    assert len(pipeline.stages[1].agents) == 4
    names = {a.name for a in pipeline.stages[1].agents}
    assert names == {"Sasori", "Itachi", "Hidan", "Deidara"}

    # Stage 3: Konan
    assert len(pipeline.stages[2].agents) == 1
    assert pipeline.stages[2].agents[0].name == "Konan"


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
    assert len(pipeline.stages) == 2

    # First agent solo
    assert pipeline.stages[0].agents[0].name == "Kisame"

    # Rest in parallel
    assert len(pipeline.stages[1].agents) == 2
    names = {a.name for a in pipeline.stages[1].agents}
    assert names == {"Itachi", "Hidan"}


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
