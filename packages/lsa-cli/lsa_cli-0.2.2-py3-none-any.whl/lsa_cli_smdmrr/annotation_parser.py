import os

import structlog
from comment_parser import comment_parser  # type: ignore[import-untyped]
from comment_parser.parsers.common import Comment  # type: ignore[import-untyped]

from .models import Annotation, SourceFileAnnotations

logger: structlog.BoundLogger = structlog.get_logger()


class AnnotationParser:
    def __init__(
        self,
        parser_exclude: list[str],
        annotation_prefix: str,
        extensions_map: dict[str, str],
    ) -> None:
        self.parser_exclude: list[str] = parser_exclude
        self.annotation_prefix: str = annotation_prefix
        self.extensions_map: dict[str, str] = extensions_map

    def parse(self, path: str) -> list[SourceFileAnnotations]:
        if os.path.isfile(path):
            if any(ex in path for ex in self.parser_exclude):
                return []
            return []

        elif os.path.isdir(path):
            model: list[SourceFileAnnotations] = []
            for root, dirs, files in os.walk(path):
                if any(ex in root for ex in self.parser_exclude):
                    continue
                for file in files:
                    if any(ex == file for ex in self.parser_exclude):
                        continue
                    try:
                        annotation: SourceFileAnnotations = self._parse_file(
                            os.path.join(root, file)
                        )
                        if annotation.annotations:
                            model.append(annotation)
                    except Exception as e:
                        logger.debug(f"Error parsing file: {os.path.join(root, file)}: {e}")
                for dir in dirs:
                    if any(ex == dir for ex in self.parser_exclude):
                        continue
            return model
        else:
            raise ValueError(f"Invalid path: {path}")

    def _parse_file(self, path: str) -> SourceFileAnnotations:
        annotations: list[Annotation] = []
        for comment in self._parse_comments(path):
            annotation: Annotation | None = self._convert_comment_to_annotation(comment)
            if annotation:
                annotations.append(annotation)
        return SourceFileAnnotations(relative_file_path=path, annotations=annotations)

    def _parse_comments(self, path: str) -> list[Comment]:
        file_extension: str = os.path.splitext(path)[1].lstrip(".")
        mime: str | None = self.extensions_map.get(file_extension, None)
        comments: list[Comment] = comment_parser.extract_comments(path, mime)
        return comments

    def _convert_comment_to_annotation(self, comment: Comment) -> Annotation | None:
        tokens: list[str] = comment.text().strip().split(" ")
        if len(tokens) < 1 or len(tokens) > 2:
            return None

        annotation: str = tokens[0].strip()
        if not annotation.startswith(self.annotation_prefix):
            return None

        annotation_name: str = annotation[len(self.annotation_prefix) :]
        value: str | None = tokens[1].strip() if len(tokens) == 2 else None
        return Annotation(name=annotation_name, value=value, line_number=comment.line_number())
