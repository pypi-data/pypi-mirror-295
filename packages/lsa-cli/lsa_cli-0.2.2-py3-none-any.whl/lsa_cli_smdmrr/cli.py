import json
import logging
import os
from argparse import ArgumentParser, Namespace

import structlog

from lsa_cli_smdmrr.models import Entity, SourceFileAnnotations

from .annotation_parser import AnnotationParser
from .annotations_to_entities_converter import AnnotationsToEntitiesConverter
from .config import Config

logger: structlog.BoundLogger = structlog.get_logger()
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))


def _export_annotations_to_json(model: list[SourceFileAnnotations], file: str) -> None:
    with open(file, "w") as f:
        json.dump(
            {"filesAnnotations": [file_annotation.to_json() for file_annotation in model]},
            f,
            indent=4,
        )


def _export_entities_to_json(entities: list[Entity], file: str) -> None:
    with open(file, "w") as f:
        json.dump({"entities": [entity.to_json() for entity in entities]}, f, indent=4)


def _parse_and_convert(args: Namespace, config: Config) -> None:
    if not os.path.exists(args.path):
        logger.error(f"Path not found: '{args.path}'")
        return

    parser: AnnotationParser = AnnotationParser(
        config.parser_exclude, config.annotation_prefix, config.extensions_map
    )

    logger.info(f"Parsing all annotations from source code from '{args.path}'")
    model: list[SourceFileAnnotations] = parser.parse(args.path)
    if not model:
        logger.info("No annotations found...")
        return
    logger.info(f"Found {len(model)} files with annotations")

    if args.annotations:
        _export_annotations_to_json(model, config.output_annotations_file)
        logger.info(f"Annotations saved to '{config.output_annotations_file}'")

    logger.info("Converting annotations to entities")
    converter: AnnotationsToEntitiesConverter = AnnotationsToEntitiesConverter(
        config.annotations_markers_map
    )
    entities: list[Entity] = converter.convert(model)
    logger.info(f"Found {len(entities)} entities")
    _export_entities_to_json(entities, config.output_entities_file)
    logger.info(f"Entities saved to '{config.output_entities_file}'")

    logger.info("""
    You can use these entities/annotations to visualize them
    on the webpage: https://markseliverstov.github.io/MFF-bachelor-work
    """)


def run() -> None:
    parser: ArgumentParser = ArgumentParser(
        description="Parses annotations from source code and convert them to entities."
    )
    parser.add_argument("path", help="Path to file or directory to parse", type=str)
    parser.add_argument(
        "-c",
        "--config",
        help="Path to the configuration file",
        type=str,
    )
    parser.add_argument(
        "-a",
        "--annotations",
        help="Parsed annotations will be saved to file if this flag is set",
        action="store_true",
    )
    args: Namespace = parser.parse_args()
    config: Config = Config.from_file(args.config) if args.config else Config.from_default()
    _parse_and_convert(args, config)
