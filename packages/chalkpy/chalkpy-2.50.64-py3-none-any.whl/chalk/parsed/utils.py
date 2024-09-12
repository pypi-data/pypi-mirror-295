from __future__ import annotations

from typing import Sequence

from chalk.features import Feature

# These are the maximum values that can be represented by a Duration proto.
MAX_DURATION_SECONDS = 315576000000
MAX_DURATION_NANOS = 999999999


def validate_namespaced_features(features: Sequence[str] | None):
    if features is None:
        return None

    unique_namespace = set()
    for string_feature in features:
        Feature.from_root_fqn(string_feature)
        unique_namespace.add(string_feature.split(".", maxsplit=1)[0])
    if len(unique_namespace) > 1:
        raise ValueError(f"Output features of named query must belong to the same namespace, but got: '{features}'.")
    return features
