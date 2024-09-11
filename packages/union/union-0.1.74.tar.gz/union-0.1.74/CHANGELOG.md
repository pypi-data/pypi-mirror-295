# Changelog

## [Unreleased] - TBA

<!-- Add new features and bug fixes here -->

## [v0.1.74] - 2024-09-10

- Fix default workspace root
- Improve copy experience for union filesystem in developer mode

## [v0.1.73] - 2024-09-09

- Use `_UNION_CONFIG.config_obj` only when all other configuration are not found
- Follow `UNION_SERVERLESS_ENDPOINT` even for flytekit code path

## [v0.1.72] - 2024-09-09

- Fix byoc `create login`

## [v0.1.71] - 2024-08-30

- Include full flytekit config into _UNION_CONFIG singleton.
- Update default project for Serverless users to 'flytesnacks'
- Do not set org when it is None

## [v0.1.70] - 2024-08-27

- Do not record error from invalid configuration

## [v0.1.69] - 2024-08-23

- Adds conda support to image builder.
- Validation `ActorEnvironment` name.
- Show configuration source with `union info`
- Adds configuration info usage context

## [v0.1.68] - 2024-08-16

- Support python versions 3.8 to 3.12 in image builder.

## [v0.1.67] - 2024-08-16

- Give `UNION_SERVERLESS_ENDPOINT` a higher precedence

## [v0.1.66] - 2024-08-09

- Do not show warning for `pip_extra_index_url`.

## [v0.1.65] - 2024-08-09

- Add kubernetes to Dockerfile to be consistent with flytekit
- Remove print statement in unionfs implementation.
- Fix support for Python 3.8

## [v0.1.64] - 2024-08-06

- Add FLYTE_SDK_RICH_TRACEBACKS=0 to dockerfile
- Include better defaults for `ActorEnvironment`

## [v0.1.63] - 2024-08-05

- Fixes unionfs for nested subdirectories

## [v0.1.62] - 2024-08-03

- Be more careful to not register usage tracker at execution time.

## [v0.1.61] - 2024-08-03

- Fix usage tracking bug.

## [v0.1.60] - 2024-08-02

- Pass verbose into flytekit

## [v0.1.59] - 2024-08-02

- Adds `union` as a builder option

## [v0.1.58] - 2024-08-01

- Adds plain text keyring when there is no keyring available.
- Adds `union info` to give configuration information
- Adds `pip_extra_index_urls` to image builder.

## [v0.1.57] - 2024-07-30

- Allow `union create login --host` to be used regardless of `byoc` or serverless.

## [v0.1.56] - 2024-07-29

- Update flytekit dependency to 1.13.1

## [v0.1.55] - 2024-07-26

- Depend on flytekit 1.13.1a3

## [v0.1.54] - 2024-07-24

- Fixes middleware for `intercept_unary_stream`.

## [v0.1.53] - 2024-07-22

- Fix `union create login --host ___` for byoc.

## [v0.1.52] - 2024-07-19

- Use logging in middleware

## [v0.1.51] - 2024-07-18

- Adds `@actor.task` and removes `@actor`
- Adds `@actor.dynamic`
- Adds `UNION_API_KEY` as environment variable for the API key.

## [v0.1.50] - 2024-07-17

- Small fix for workspaces with GPUs

## [v0.1.49] - 2024-07-17

- Use `--host` for login to be consistent with uctl.
- Improve workspaces to make it easier to authenticate.

## [v0.1.48] - 2024-07-12

- Give `ttl_seconds` a non-zero value of 100

## [v0.1.47] - 2024-07-11

- Use cr.union.ai hostname for serverless images
- Adds `UNION_CONFIG` and `UNION_SERVERLESS_API_KEY`.
- Migrate to `UNION_SERVERLESS_ENDPOINT` and `UNION_ENABLE_REGISTER_IMAGE_BUILDER` for development.
- Simplify `union create login`
- Update all other `UNION_` environment variables.
- Adds `union create login --host`

## [v0.1.46] - 2024-07-05

- Only add `union` in image builder if it is not specified already

## [v0.1.45] - 2024-07-03

- First release of `union` SDK.

## [v0.1.44] - 2024-07-03

- Updates Actor definition

## [v0.1.43] - 2024-07-01

- Fixes MetadataFS for Artifacts

## [v0.1.42] - 2024-06-28

- Use home directory when installing code-sever manually

## [v0.1.41] - 2024-06-28

- Support `~` in `workspace_root`

## [v0.1.40] - 2024-06-27

- Enable binary file secrets

## [v0.1.39] - 2024-06-26

- Enable artifact triggers that bind to queries

## [v0.1.38] - 2024-06-25

- Add accelerator to `ActorEnvironment`.

## [v0.1.37] - 2024-06-25

- Use unionai version that is installed during registration in image builder

## [v0.1.36] - 2024-06-25

- Revert back to `~/.unionai/config.yaml` for standard configuration.

## [v0.1.35] - 2024-06-25

- `pyflyte` defaults to localhost for `byoc` to match with OSS.
- Improve image builder with flyte labels
- Update docstrings for classes and methods in `unionai`
- Adds `UNIONAI_ENABLE_REGISTER_IMAGE_BUILDER` to offline debugging.

## [v0.1.34] - 2024-06-24

- Send errors from flytekit.clients to sentry
- Image builder now ignores files from `.gitignore` and `.dockerignore`

## [v0.1.33] - 2024-06-21

- Fixes image builder execution id bug

## [v0.1.32] - 2024-06-20

- Fixes bug with CLI in workspaces.

## [v0.1.31] - 2024-06-18

- Makes the workspace root configurable.

## [v0.1.30] - 2024-06-18

- Change config directory to `~/.config/unionai/config.yaml`

## [v0.1.29] - 2024-06-18

- Make sure image build can recover from UI termination
- Error when the config is empty when using `~/.unionai/config`.
- Gives `UNIONAI_SERVERLESS_ENDPOINT` a high precedence than `~/.unionai/config`

## [v0.1.28] - 2024-06-13

- Ship with actors
- Use `UNIONAI_SDK_LOGGING_LEVEL` for controlling logging level.

## [v0.1.27] - 2024-06-11

- Fixes issue with `unionai[byoc]`

## [v0.1.26] - 2024-06-11

- Improves support for large dataframes
- Adds `pip install unionai[byoc]`
- Image builder skips building if the image is already built.
- Gives `UNIONAI_SERVERLESS_ENDPOINT` a high precedence than `~/.unionai/config`

## [v0.1.25] - 2024-06-05

- pin flytekit version >= 1.12.2

## [v0.1.24] - 2024-06-04

- pin flytekit version >= 1.12.1rc1
- Update to use vanity URLs when dumping console link

## [v0.1.23] - 2024-05-31

- Support `ImageSpec` in actors

## [v0.1.22] - 2024-05-29

- Update workspace idle time to 20 minutes.

## [v0.1.21] - 2024-05-28

- Fixes bug with workspaces

## [v0.1.20] - 2024-05-28

- Fixes project bug from CLI.

## [v0.1.19] - 2024-05-28

- Adds workspaces alpha feature.

## [v0.1.18] - 2024-05-21

- Disable fsspec caching to remove stderr from grpc.

## [v0.1.17] - 2024-05-14

- Allows FlyteDeck to appear without `flytekitplugins-deck-standard`

## [v0.1.16] - 2024-05-09

- Injects org into Artifact grpc calls.
- Update set_org to recurse maps as well.
- Ignore .git folder in image builder.

## [v0.1.15] - 2024-05-07

- Only show client_id when running `unionai get app`.
- Raises an error if `python_version` is not `"3.11"` in Image Builder.
- Add initial implementation for the actor decorator. Currently only works on functions

## [v0.1.14] - 2024-04-10

- Fixes FlyteDeck regression from fsspec
- Improve error message when image build fails
- Fixes regression in unionfs

## [v0.1.12] - 2024-04-04

- Adds support for `flytekit`'s StructuredDatasets
- Update to `serverless-1.us-east-2.s.union.ai` tenant
- Update HTML callback page.

## [v0.1.11] - 2024-03-29

- Changes image builder name to `unionai`.
- Fixes issue with multiple callbacks when authenticating.

## [v0.1.10] - 2024-03-26

- Fixes project issue when switching between `pyflyte` and `unionai`.

## [v0.1.9] - 2024-03-26

- Adds `verbose` and `x-request-id` for debugging.

## [v0.1.8] - 2024-03-25

- Install `unionai` by default in the image builder.

## [v0.1.7] - 2024-03-25

* Adds Image Build related mapping of Union serverless FQDN to Google Artifact registry base URLs.
- Adds `unionai create login device-flow` and `unionai delete login` to enable device flow authentication.
- `unionai` ignores `FLYTECTL_CONFIG`. Please use `UNIONAI_CONFIG` instead.
- Only require auth when running `unionai run --remote`.
- Make sure `project` is set to `"default"` for serverless.

## [v0.1.6] - 2024-03-13

- Updates Artifacts with `OnTrigger` and sync up with `flytekit`
- Adds Time Granularity
- Add model/data cards

## [v0.1.5] - 2024-02-29

- Fixes bug with `FlyteDirectory` such that multiple files can be downloaded

## [v0.1.4] - 2024-02-27

- Fixes circular reference issue when importing `UnionRemote`

## [v0.1.3] - 2024-02-27

- Adds support for `FlyteDirectory`

## [v0.1.2] - 2024-02-27

- Runs Image builder in the system project
- Adds `is_container()` to ImageSpec

## [v0.1.1] - 2024-02-16

- Fixes default images when passing `--config` in CLI
- Redesigned OAuth success HTML page: Requires `flytekit>=1.10.8`

## [v0.1.0] - 2024-02-15

- Adds UnionAI's ImageBuilder plugin for `ImageSpec`
- Adds Secrets CLI
- Adds Application management CLI
- Adds `--org` to configure the organization in every grpc request
- Adds Artifacts and Triggers (`unionai.artifacts`)
- Adds PersistentDirectory for on-node persistent storage (`unionai.persist`)
