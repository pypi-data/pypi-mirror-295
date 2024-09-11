from __future__ import annotations

from functools import partial as _partial

import mdit as _mdit


class ReporterException(Exception):
    """Base exception class with HTML reporting capabilities."""

    def __init__(
        self,
        report: _mdit.Document,
        sphinx_config: dict | None = None,
        sphinx_args: dict | None = None,
    ):
        console_text = report.render(target="ansi", filters="console")
        super().__init__(f"\n{console_text}")
        sphinx_args = {
            "status": None,
            "warning": None,
        } | (sphinx_args or {})
        target_config = _mdit.target.sphinx()
        target_config.renderer = _partial(
            _mdit.render.sphinx,
            config=sphinx_config,
            **sphinx_args
        )
        report.default_output_target = target_config
        self.report = report
        return
