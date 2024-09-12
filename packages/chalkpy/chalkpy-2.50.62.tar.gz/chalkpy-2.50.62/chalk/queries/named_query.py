from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Mapping, Sequence

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference


class NamedQuery:
    def __init__(
        self,
        *,
        name: str,
        version: str | None = None,
        input: Sequence[FeatureReference] | None = None,
        output: Sequence[FeatureReference] | None = None,
        tags: Sequence[str] | None = None,
        description: str | None = None,
        owner: str | None = None,
        meta: Mapping[str, str] | None = None,
        staleness: Mapping[FeatureReference, str] | None = None,
        planner_options: Mapping[str, str | int | bool] | None = None,
    ):
        """Create a named query.

        Named queries are aliases for specific queries that can be used by API clients.

        Parameters
        ----------
        name
            A name for the named query—this can be versioned with the version parameter, but
            must otherwise be unique. The name of the named query shows up in the dashboard and
            is used to specify the outputs for a query.
        version:
            A string specifying the version of the named query.
        input
            The features which will be provided by callers of this query.
            For example, `[User.id]`. Features can also be expressed as snakecased strings,
            e.g. `["user.id"]`.
        output:
            Outputs are the features that you'd like to compute from the inputs.
            For example, `[User.age, User.name, User.email]`.

            If an empty sequence, the output will be set to all features on the namespace
            of the query. For example, if you pass as input `{"user.id": 1234}`, then the query
            is defined on the `User` namespace, and all features on the `User` namespace
            (excluding has-one and has-many relationships) will be used as outputs.
        tags
            Allows selecting resolvers with these tags.
        description
            A description of the query. Rendered in the Chalk UI and used for search indexing.
        owner
            The owner of the query. This should be a Slack username or email address.
            This is used to notify the owner in case of incidents
        meta
            Additional metadata for the query.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        planner_options
            Dictionary of additional options to pass to the Chalk query engine.
            Values may be provided as part of conversations with Chalk support
            to enable or disable specific functionality.

        Returns
        -------
        NamedQuery
            A named query object.

        Examples
        --------
        >>> from chalk import NamedQuery
        >>> # this query's name and version can be used to specify query outputs in an API request.
        >>> NamedQuery(
        ...     name="user_age",
        ...     version="1.0.0",
        ...     input=[User.id],
        ...     output=[User.age],
        ... )
        """
        super().__init__()
        caller_filename = inspect.stack()[1].filename

        dup_nq = NAMED_QUERY_REGISTRY.get((name, version), None)
        if dup_nq is not None:
            raise ValueError(
                (
                    f"Named query must be distinct on name and version, but found two named queries with name '{name}' and "
                    f"version '{version} in files '{dup_nq.filename}' and '{caller_filename}'."
                )
            )

        self.name = name
        self.version = version
        self.input = [str(f) for f in input] if input else None
        self.output = [str(f) for f in output] if output else None
        self.tags = [str(t) for t in tags] if tags else None
        self.filename = caller_filename
        self.description = description
        self.owner = owner
        self.meta = meta
        self.staleness = {str(k): v for k, v in staleness.items()} if staleness else None
        self.planner_options = {k: str(v) for k, v in planner_options.items()} if planner_options else None

        NAMED_QUERY_REGISTRY[(name, version)] = self


NAMED_QUERY_REGISTRY: dict[tuple[str, str | None], NamedQuery] = {}
